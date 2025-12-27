"""Vector search functionality."""

import chromadb
from chromadb.config import Settings
import logging
from collections.abc import Sequence
from functools import lru_cache
from typing import Any

import openai

from config import Config
from ingest.embed import get_embedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _rewrite_query_as_question_heuristic(query: str) -> str:
    """
    Rewrite/normalize a user query into a question-shaped string.

    This is a lightweight heuristic step intended to improve retrieval alignment,
    especially for question-only embedding strategies, without adding extra network calls.
    """
    q = (query or "").strip()
    if not q:
        return q

    # If it already looks like a question, keep it.
    if q.endswith("?") or "?" in q:
        return q

    # Normalize common punctuation.
    if q.endswith("."):
        q = q[:-1].rstrip()

    # Simple Korean-friendly heuristics for declarative endings.
    if q.endswith("입니다"):
        return q[: -len("입니다")].rstrip() + "인가요?"
    if q.endswith("이다"):
        return q[: -len("이다")].rstrip() + "인가요?"
    if q.endswith("다"):
        # Avoid aggressively changing the ending; just add a question mark.
        return q + "?"

    return q + "?"


@lru_cache(maxsize=2048)
def _rewrite_query_as_question_openai_cached(query: str) -> str:
    """
    Rewrite the query into a single Korean question using OpenAI.

    Returns the rewritten question. Raises on API failure so callers can fall back.
    """
    q = (query or "").strip()
    if not q:
        return q

    if not Config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    model = Config.LLM_MODEL

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You rewrite user inputs into a single natural Korean question.\n"
                    "Rules:\n"
                    "- Preserve the original meaning.\n"
                    "- Output ONLY the rewritten question, nothing else.\n"
                    "- Do NOT answer.\n"
                    "- Keep it to one sentence.\n"
                    "- Ensure it ends with a question mark '?'."
                ),
            },
            {"role": "user", "content": q},
        ],
        temperature=0.0,
        max_completion_tokens=80,
    )

    text = (resp.choices[0].message.content or "").strip()
    # Defensive normalization: take first non-empty line only.
    text = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not text:
        return ""
    if not text.endswith("?"):
        text = text.rstrip(".") + "?"
    return text


def _rewrite_query_as_question(query: str) -> str:
    """
    Rewrite the user query into a question-shaped string (OpenAI-first).

    Falls back to a heuristic rewrite when OpenAI is unavailable or fails.
    """
    q = (query or "").strip()
    if not q:
        return q

    try:
        return _rewrite_query_as_question_openai_cached(q)
    except Exception as e:
        logger.debug("Query rewrite via OpenAI failed; falling back. err=%s", e)
        return _rewrite_query_as_question_heuristic(q)


class VectorSearch:
    """Vector search using Chroma."""

    def __init__(self, collection_name: str | Sequence[str] | None = None):
        """
        Initialize vector search.

        Args:
            collection_name: Name(s) of Chroma collection(s) (defaults to Config value).
                If multiple names are provided, search can be executed across all collections.
        """
        if collection_name is None:
            collection_names = [Config.CHROMA_COLLECTION_NAME]
        elif isinstance(collection_name, str):
            collection_names = [collection_name]
        else:
            collection_names = list(collection_name)

        if not collection_names:
            raise ValueError("collection_name must not be an empty list")

        self.collection_names: list[str] = collection_names
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collections = {
            name: self.client.get_or_create_collection(name=name)
            for name in self.collection_names
        }

        # Backward-compatible single-collection attribute
        self.collection_name = self.collection_names[0]
        self.collection = self.collections[self.collection_name]

    def search(
        self, query: str, top_k: int | None = None, threshold: float | None = None
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Search for similar FAQ entries.

        Args:
            query: Search query text
            top_k: Number of results to return (defaults to Config.TOP_K)
            threshold: Minimum similarity threshold (defaults to Config.SIMILARITY_THRESHOLD)

        Returns:
            Mapping from collection name to a list of search results with metadata
        """
        if top_k is None:
            top_k = Config.TOP_K
        if threshold is None:
            threshold = Config.SIMILARITY_THRESHOLD

        # Rewrite query into a question-shaped string before embedding.
        rewritten_query = _rewrite_query_as_question(query)

        # Generate query embedding
        query_embedding = get_embedding(rewritten_query)

        # Search in Chroma per collection (embedding strategy).
        per_collection: dict[str, list[dict[str, Any]]] = {
            name: [] for name in self.collections.keys()
        }
        for collection_name, collection in self.collections.items():
            results = collection.query(
                query_embeddings=[query_embedding], n_results=top_k
            )

            if not results.get("ids") or not results["ids"][0]:
                continue

            for i in range(len(results["ids"][0])):
                # Convert distance to similarity score
                distance = results["distances"][0][i]
                similarity = 1 - distance  # Assuming cosine distance

                # if similarity < threshold:
                #     continue

                metadata = results["metadatas"][0][i]
                doc_id = results["ids"][0][i]

                candidate: dict[str, Any] = {
                    "id": doc_id,
                    "text": results["documents"][0][i],
                    "metadata": metadata,
                    "distance": distance,
                    "similarity": similarity,
                    "collection_name": collection_name,
                }

                per_collection[collection_name].append(candidate)

        # Sort and clip per collection.
        for name, items in per_collection.items():
            items.sort(key=lambda r: float(r.get("similarity", 0.0)), reverse=True)
            per_collection[name] = items[:top_k]

        logger.info(
            "Searched query: %s... (collections=%s)",
            rewritten_query[:50],
            self.collection_names,
        )
        return per_collection

    def search_merged(
        self, query: str, top_k: int | None = None, threshold: float | None = None
    ) -> list[dict[str, Any]]:
        """
        Search across one or more collections and return a single merged ranked list.

        This is useful for pipelines (e.g. RAG) that want a unified context rather than
        comparing embedding strategies side-by-side.
        """
        if top_k is None:
            top_k = Config.TOP_K
        if threshold is None:
            threshold = Config.SIMILARITY_THRESHOLD

        rewritten_query = _rewrite_query_as_question(query)
        query_embedding = get_embedding(rewritten_query)

        merged: dict[str, dict[str, Any]] = {}
        for collection_name, collection in self.collections.items():
            results = collection.query(
                query_embeddings=[query_embedding], n_results=top_k
            )

            if not results.get("ids") or not results["ids"][0]:
                continue

            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                similarity = 1 - distance  # Assuming cosine distance

                if similarity < threshold:
                    continue

                metadata = results["metadatas"][0][i]
                doc_id = results["ids"][0][i]

                # Prefer de-duplication by FAQ identity (metadata["id"]) when present.
                dedupe_key = (
                    str(metadata.get("id", doc_id))
                    if isinstance(metadata, dict)
                    else str(doc_id)
                )

                candidate: dict[str, Any] = {
                    "id": doc_id,
                    "text": results["documents"][0][i],
                    "metadata": metadata,
                    "distance": distance,
                    "similarity": similarity,
                    "collection_name": collection_name,
                }

                prev = merged.get(dedupe_key)
                if prev is None or float(candidate["similarity"]) > float(
                    prev["similarity"]
                ):
                    merged[dedupe_key] = candidate

        formatted_results = sorted(
            merged.values(), key=lambda r: float(r.get("similarity", 0.0)), reverse=True
        )[:top_k]

        logger.info(
            "Merged-search found %s results for query: %s... (collections=%s)",
            len(formatted_results),
            rewritten_query[:50],
            self.collection_names,
        )
        return formatted_results

    def get_all_documents(self) -> list[dict[str, Any]]:
        """Get all documents from the configured collection(s) (for debugging)."""
        documents: list[dict[str, Any]] = []
        for collection_name, collection in self.collections.items():
            results = collection.get()
            for i in range(len(results["ids"])):
                documents.append(
                    {
                        "id": results["ids"][i],
                        "text": results["documents"][i],
                        "metadata": results["metadatas"][i],
                        "collection_name": collection_name,
                    }
                )

        return documents
