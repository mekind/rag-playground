"""Vector search functionality."""

import chromadb
from chromadb.config import Settings
import logging
from collections.abc import Sequence
from typing import Any

from config import Config
from ingest.embed import get_embedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorSearch:
    """Vector search using Chroma."""

    def __init__(self, collection_name: str | Sequence[str] | None = None):
        """
        Initialize vector search.

        Args:
            collection_name: Name(s) of Chroma collection(s) (defaults to Config value).
                If multiple names are provided, search will be executed across all collections
                and results will be merged.
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
    ) -> list[dict[str, Any]]:
        """
        Search for similar FAQ entries.

        Args:
            query: Search query text
            top_k: Number of results to return (defaults to Config.TOP_K)
            threshold: Minimum similarity threshold (defaults to Config.SIMILARITY_THRESHOLD)

        Returns:
            List of search results with metadata
        """
        if top_k is None:
            top_k = Config.TOP_K
        if threshold is None:
            threshold = Config.SIMILARITY_THRESHOLD

        # Generate query embedding
        query_embedding = get_embedding(query)

        # Search in Chroma (single or multiple collections) and merge results.
        merged: dict[str, dict[str, Any]] = {}
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
            f"Found {len(formatted_results)} results for query: {query[:50]}... (collections={self.collection_names})"
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
