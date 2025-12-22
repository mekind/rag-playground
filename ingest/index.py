"""Index embeddings using Chroma."""

from __future__ import annotations

import chromadb
from chromadb.config import Settings
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection
from chromadb.api.types import Metadata
import json
from pathlib import Path
import logging
from collections.abc import Sequence
from typing import Literal, TypedDict, NotRequired, cast

from config import Config
from ingest.embed import get_embeddings_batch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FAQEntry(TypedDict):
    id: int
    question: str
    answer: str
    text: NotRequired[str]


class FAQMetadata(TypedDict):
    question: str
    answer: str
    id: int


FAQColumn = Literal["question", "answer"]


def create_chroma_client() -> ClientAPI:
    """Create and return a Chroma client."""
    client = chromadb.PersistentClient(
        path=Config.CHROMA_PERSIST_DIRECTORY,
        settings=Settings(anonymized_telemetry=False),
    )
    return cast(ClientAPI, client)


def recreate_collection(
    client: ClientAPI, collection_name: str | None = None
) -> Collection:
    """Delete an existing collection (if present) and create a new one."""
    if collection_name is None:
        collection_name = Config.CHROMA_COLLECTION_NAME

    try:
        client.delete_collection(name=collection_name)
        logger.info(f"Deleted existing collection: {collection_name}")
    except Exception:
        # Collection might not exist; continue to create.
        logger.info(f"No existing collection to delete: {collection_name}")

    collection = cast(Collection, client.create_collection(name=collection_name))
    logger.info(f"Created new collection: {collection_name}")
    return collection


def load_processed_data(data_path: str | Path) -> list[FAQEntry]:
    """Load processed FAQ data from JSON file."""
    data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Processed data file not found: {data_path}. "
            "Please run data/preprocess.py first."
        )

    with open(data_path, "r", encoding="utf-8") as f:
        data = cast(list[FAQEntry], json.load(f))

    logger.info(f"Loaded {len(data)} FAQ entries from {data_path}")
    return data


def build_embedding_text(item: FAQEntry, columns: Sequence[FAQColumn]) -> str:
    """Build the text that will be embedded from the given FAQ entry."""
    if not columns:
        raise ValueError("columns must not be empty")

    parts = [item[col] for col in columns]
    # Keep a stable separator so q+a is deterministic.
    return "\n\n".join(parts)


def collection_name_for(columns: Sequence[FAQColumn]) -> str:
    """Derive a collection name suffix based on embedding strategy."""
    key = "_".join(columns)
    return f"{Config.CHROMA_COLLECTION_NAME}__{key}"


def index_faq_data(
    collection: Collection,
    faq_data: Sequence[FAQEntry],
    columns: Sequence[FAQColumn],
    batch_size: int = 100,
) -> None:
    """
    Index FAQ data into Chroma collection.

    Args:
        collection: Chroma collection object
        faq_data: List of FAQ dictionaries with 'id', 'question', 'answer', 'text'
        batch_size: Number of items to process in each batch
    """
    # Check if collection already has data
    existing_count = collection.count()
    if existing_count > 0:
        logger.warning(
            f"Collection already contains {existing_count} items. Clearing..."
        )
        # Note: Chroma doesn't have a direct clear method, so we'll delete and recreate
        # For now, we'll just add new items with unique IDs

    # Build texts for embedding based on selected columns
    texts = [build_embedding_text(item, columns) for item in faq_data]
    ids = [f"faq_{item['id']}" for item in faq_data]
    metadatas: list[Metadata] = [
        cast(
            Metadata,
            {
                "question": item["question"],
                "answer": item["answer"],
                "id": item["id"],
                "embedding_columns": "+".join(columns),
            },
        )
        for item in faq_data
    ]

    logger.info("Generating embeddings...")
    embeddings = get_embeddings_batch(texts, batch_size=batch_size)

    logger.info("Adding documents to Chroma collection...")

    # Add in batches to avoid memory issues
    for i in range(0, len(faq_data), batch_size):
        batch_ids = ids[i : i + batch_size]
        batch_embeddings = embeddings[i : i + batch_size]
        batch_texts = texts[i : i + batch_size]
        batch_metadatas = metadatas[i : i + batch_size]

        collection.add(
            ids=batch_ids,
            embeddings=cast(list[Sequence[float]], batch_embeddings),
            documents=batch_texts,
            metadatas=batch_metadatas,
        )

        logger.info(
            f"Indexed batch {i // batch_size + 1}/{(len(faq_data) + batch_size - 1) // batch_size}"
        )

    logger.info(f"Successfully indexed {len(faq_data)} FAQ entries")


def main() -> None:
    """Main indexing pipeline."""
    Config.validate()

    # Load processed data
    processed_data_file = Path(Config.PROCESSED_DATA_DIR) / "faq_processed.json"
    faq_data = load_processed_data(processed_data_file)

    # Create Chroma client
    client = create_chroma_client()
    strategies: list[list[FAQColumn]] = [
        ["question"],
        ["answer"],
        ["question", "answer"],
    ]

    for columns in strategies:
        name = collection_name_for(columns)
        collection = recreate_collection(client, collection_name=name)
        index_faq_data(collection, faq_data, columns=columns)
        logger.info(
            f"Collection {name} now contains {collection.count()} items (columns={'+'.join(columns)})"
        )

    logger.info("Indexing complete!")


if __name__ == "__main__":
    main()
