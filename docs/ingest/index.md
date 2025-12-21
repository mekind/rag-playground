# ingest/index.py Documentation

## Purpose and Responsibility

The `index.py` module handles indexing FAQ data into a Chroma vector database. It loads processed FAQ data, generates embeddings, and stores them in Chroma with associated metadata. This module creates the searchable index that powers the retrieval system.

## Main Components

### Function: `create_chroma_client()`

Creates and returns a persistent Chroma client instance.

**Returns:**
- `chromadb.PersistentClient`: Chroma client configured for persistence

**Behavior:**
- Creates a persistent client using Config.CHROMA_PERSIST_DIRECTORY
- Disables telemetry for privacy

### Function: `create_collection(client, collection_name=None)`

Creates or retrieves a Chroma collection.

**Parameters:**
- `client`: Chroma client instance
- `collection_name` (str, optional): Name of collection (defaults to Config.CHROMA_COLLECTION_NAME)

**Returns:**
- `Collection`: Chroma collection object

**Behavior:**
- Attempts to get existing collection
- Creates new collection if it doesn't exist
- Logs the operation

### Function: `load_processed_data(data_path)`

Loads processed FAQ data from JSON file.

**Parameters:**
- `data_path` (str): Path to processed JSON file

**Returns:**
- `list[dict]`: List of FAQ entries with id, question, answer, text fields

**Behavior:**
- Validates file existence
- Loads JSON data
- Raises FileNotFoundError if file doesn't exist
- Logs the number of entries loaded

### Function: `index_faq_data(collection, faq_data, batch_size=100)`

Indexes FAQ data into Chroma collection.

**Parameters:**
- `collection`: Chroma collection object
- `faq_data` (list[dict]): FAQ data to index
- `batch_size` (int): Number of items to process per batch (default: 100)

**Behavior:**
- Checks for existing data in collection
- Extracts texts, IDs, and metadata from FAQ data
- Generates embeddings using `get_embeddings_batch()`
- Adds documents to Chroma in batches
- Logs progress for each batch
- Stores embeddings, documents, and metadata together

**Metadata Structure:**
Each FAQ entry is stored with metadata containing:
- `question`: Original question text
- `answer`: Original answer text
- `id`: FAQ entry ID

### Function: `main()`

Main indexing pipeline that orchestrates the entire indexing process.

**Behavior:**
- Validates configuration
- Loads processed FAQ data
- Creates Chroma client and collection
- Indexes all FAQ entries
- Logs completion and final count

## Dependencies

- `chromadb`: Chroma vector database library
- `json`: For loading processed data
- `pathlib.Path`: For path manipulation
- `config.Config`: For configuration values
- `ingest.embed`: For embedding generation
- `logging`: For progress logging

## Assumptions

- Processed FAQ data exists at `data/processed/faq_processed.json`
- Chroma database directory is writable
- Sufficient memory available for batch processing
- Embedding generation succeeds for all texts
