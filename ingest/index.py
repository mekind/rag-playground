"""Index embeddings using Chroma."""
import chromadb
from chromadb.config import Settings
import json
from pathlib import Path
import logging

from config import Config
from ingest.embed import get_embeddings_batch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_chroma_client():
    """Create and return a Chroma client."""
    client = chromadb.PersistentClient(
        path=Config.CHROMA_PERSIST_DIRECTORY,
        settings=Settings(anonymized_telemetry=False)
    )
    return client


def create_collection(client, collection_name: str = None):
    """Create or get a Chroma collection."""
    if collection_name is None:
        collection_name = Config.CHROMA_COLLECTION_NAME
    
    try:
        collection = client.get_collection(name=collection_name)
        logger.info(f"Using existing collection: {collection_name}")
    except Exception:
        collection = client.create_collection(name=collection_name)
        logger.info(f"Created new collection: {collection_name}")
    
    return collection


def load_processed_data(data_path: str):
    """Load processed FAQ data from JSON file."""
    data_path = Path(data_path)
    
    if not data_path.exists():
        raise FileNotFoundError(
            f"Processed data file not found: {data_path}. "
            "Please run data/preprocess.py first."
        )
    
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    logger.info(f"Loaded {len(data)} FAQ entries from {data_path}")
    return data


def index_faq_data(collection, faq_data, batch_size: int = 100):
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
        logger.warning(f"Collection already contains {existing_count} items. Clearing...")
        # Note: Chroma doesn't have a direct clear method, so we'll delete and recreate
        # For now, we'll just add new items with unique IDs
    
    # Extract texts for embedding
    texts = [item["text"] for item in faq_data]
    ids = [f"faq_{item['id']}" for item in faq_data]
    metadatas = [
        {
            "question": item["question"],
            "answer": item["answer"],
            "id": item["id"]
        }
        for item in faq_data
    ]
    
    logger.info("Generating embeddings...")
    embeddings = get_embeddings_batch(texts, batch_size=batch_size)
    
    logger.info("Adding documents to Chroma collection...")
    
    # Add in batches to avoid memory issues
    for i in range(0, len(faq_data), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_embeddings = embeddings[i:i + batch_size]
        batch_texts = texts[i:i + batch_size]
        batch_metadatas = metadatas[i:i + batch_size]
        
        collection.add(
            ids=batch_ids,
            embeddings=batch_embeddings,
            documents=batch_texts,
            metadatas=batch_metadatas
        )
        
        logger.info(f"Indexed batch {i // batch_size + 1}/{(len(faq_data) + batch_size - 1) // batch_size}")
    
    logger.info(f"Successfully indexed {len(faq_data)} FAQ entries")


def main():
    """Main indexing pipeline."""
    Config.validate()
    
    # Load processed data
    processed_data_file = Path(Config.PROCESSED_DATA_DIR) / "faq_processed.json"
    faq_data = load_processed_data(processed_data_file)
    
    # Create Chroma client and collection
    client = create_chroma_client()
    collection = create_collection(client)
    
    # Index the data
    index_faq_data(collection, faq_data)
    
    logger.info("Indexing complete!")
    logger.info(f"Collection now contains {collection.count()} items")


if __name__ == "__main__":
    main()
