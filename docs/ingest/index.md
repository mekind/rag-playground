# ingest/index.py Documentation

## Purpose and Responsibility

The `index.py` module handles indexing FAQ data into a Chroma vector database. It loads processed FAQ data, generates embeddings, and stores them in Chroma with associated metadata. This module creates the searchable index that powers the retrieval system.

## Main Components

### Function: `create_chroma_client()`

Creates and returns a persistent Chroma client instance.

**Returns:**
- `chromadb.PersistentClient`: Chroma client configured for persistence

**Type signature (Python):**

`create_chroma_client() -> chromadb.api.ClientAPI`

**Behavior:**
- Creates a persistent client using Config.CHROMA_PERSIST_DIRECTORY
- Disables telemetry for privacy

### Function: `create_collection(client, collection_name=None)`
Creates or retrieves a Chroma collection.

**Note:** The current implementation performs "get-or-create" logic directly in `main()` rather than exposing a separate `create_collection()` helper.

### Function: `recreate_collection(client, collection_name=None)`

Deletes an existing Chroma collection (if present) and creates a fresh one.

**Parameters:**
- `client`: Chroma client instance
- `collection_name` (str, optional): Name of collection (defaults to Config.CHROMA_COLLECTION_NAME)

**Returns:**
- `Collection`: Newly created Chroma collection object

**Type signature (Python):**

`recreate_collection(client: chromadb.api.ClientAPI, collection_name: str | None = None) -> chromadb.api.models.Collection.Collection`

**Behavior:**
- Attempts to delete the existing collection by name
- Creates a new collection with the same name
- Logs the operation

### Function: `load_processed_data(data_path)`

Loads processed FAQ data from JSON file.

**Parameters:**
- `data_path` (str): Path to processed JSON file

**Returns:**
- `list[dict]`: List of FAQ entries with id, question, answer, text fields

**Type signature (Python):**

`load_processed_data(data_path: str | pathlib.Path) -> list[FAQEntry]`

**Data shape (TypedDict):**

`FAQEntry = TypedDict("FAQEntry", {"id": int, "question": str, "answer": str, "text": NotRequired[str]})`

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

**Type signature (Python):**

`index_faq_data(collection: chromadb.api.models.Collection.Collection, faq_data: collections.abc.Sequence[FAQEntry], batch_size: int = 100) -> None`

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

**Type signature (Python):**

`main() -> None`

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
