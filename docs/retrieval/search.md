# retrieval/search.py Documentation

## Purpose and Responsibility

The `search.py` module implements vector search functionality using Chroma. It provides a `VectorSearch` class that handles query embedding generation and similarity search in the indexed FAQ database. This module is responsible for finding relevant FAQ entries based on semantic similarity to user queries.

## Main Components

### Class: `VectorSearch`

A class that encapsulates vector search operations using Chroma.

#### Initialization: `__init__(collection_name=None)`

**Parameters:**
- `collection_name` (str | list[str] | None, optional): One collection name or multiple collection names.
  - If `None`, defaults to `Config.CHROMA_COLLECTION_NAME`.
  - If a list is provided, the instance will search across **multiple collections** and merge the results.

**Behavior:**
- Initializes Chroma persistent client
- Retrieves or creates the specified collection(s)
- Stores collection reference(s) for search operations

**Embedding strategy and collections (from `docs/ingest/index.md`):**
Indexing can create multiple Chroma collections for different embedding strategies, such as:
- question-only embeddings
- answer-only embeddings
- question+answer combined embeddings

When `collection_name` is a list, `VectorSearch` will query each collection (same query embedding) and then merge results into a single ranked list.

#### Method: `search(query, top_k=None, threshold=None)`

Searches for similar FAQ entries based on query text.

**Parameters:**
- `query` (str): Search query text
- `top_k` (int, optional): Number of results to return (defaults to Config.TOP_K)
- `threshold` (float, optional): Minimum similarity threshold (defaults to Config.SIMILARITY_THRESHOLD)

**Returns:**
- `list[dict]`: List of search results, each containing:
  - `id` (str): Document ID
  - `text` (str): Document text
  - `metadata` (dict): Document metadata (question, answer, id)
  - `distance` (float): Distance score from Chroma
  - `similarity` (float): Converted similarity score (1 - distance)
  - `collection_name` (str, optional): Which collection the hit came from (present when searching multiple collections)

**Behavior:**
- Generates embedding for query using `get_embedding()`
- Queries the configured Chroma collection(s) with the query embedding
- Converts Chroma distance scores to similarity scores
- Filters results by similarity threshold
- When multiple collections are configured:
  - Merges results from all collections into a single list
  - De-duplicates by FAQ identity (prefers higher similarity when duplicates occur)
  - Sorts by similarity descending and returns the top `top_k`
- Formats and returns results with metadata
- Logs search operation

#### Method: `get_all_documents()`

Retrieves all documents from the collection (for debugging purposes).

**Returns:**
- `list[dict]`: List of all documents with id, text, and metadata

**Behavior:**
- Retrieves all documents from collection
- Formats them into dictionaries
- Returns complete document list

## Dependencies

- `chromadb`: Chroma vector database library
- `config.Config`: For configuration values
- `ingest.embed`: For query embedding generation
- `logging`: For operation logging

## Assumptions

- Chroma collection exists and is properly indexed
- Collection contains FAQ entries with embeddings
- Query text is valid and can be embedded
- Similarity threshold is between 0 and 1
