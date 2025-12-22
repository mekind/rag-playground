# ingest/embed.py Documentation

## Purpose and Responsibility

The `embed.py` module provides functionality to generate text embeddings using the OpenAI Embedding API. It handles both single text and batch text embedding generation, managing API calls, error handling, and rate limiting. This module is a core component of the RAG pipeline, converting text into vector representations for semantic search.

## Main Components

### Function: `get_embedding(text, model=None)`

Generates an embedding vector for a single text string.

**Parameters:**
- `text` (str): Text to embed
- `model` (str, optional): Embedding model name (defaults to Config.EMBEDDING_MODEL)

**Returns:**
- `list[float]`: List of embedding values (vector representation)

**Type signature (Python):**

`get_embedding(text: str, model: str | None = None) -> list[float]`

**Behavior:**
- Uses OpenAI API to generate embeddings
- Handles API errors and logs them
- Returns the embedding vector from the API response

### Function: `get_embeddings_batch(texts, model=None, batch_size=100)`

Generates embeddings for multiple texts in batches.

**Parameters:**
- `texts` (list[str]): List of texts to embed
- `model` (str, optional): Embedding model name
- `batch_size` (int): Number of texts to process per batch (default: 100)

**Returns:**
- `list[list[float]]`: List of embedding vectors, one per input text

**Type signature (Python):**

`get_embeddings_batch(texts: list[str], model: str | None = None, batch_size: int = 100) -> list[list[float]]`

**Behavior:**
- Processes texts in batches to manage API rate limits
- Logs progress for each batch
- Adds small delays between batches to respect rate limits
- Handles errors per batch and raises exceptions
- Returns all embeddings in the same order as input texts

## Dependencies

- `openai`: OpenAI API client library
- `config.Config`: For accessing API key and model configuration
- `logging`: For progress and error logging
- `time`: For rate limiting delays

## Assumptions

- OpenAI API key is configured in Config.OPENAI_API_KEY
- OpenAI API is accessible and functional
- The specified embedding model is available
- Batch size of 100 is appropriate for rate limits (may need adjustment)
