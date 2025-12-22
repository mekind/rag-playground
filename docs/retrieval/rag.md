# retrieval/rag.py Documentation

## Purpose and Responsibility

The `rag.py` module implements the RAG (Retrieval-Augmented Generation) pipeline that combines vector search with LLM-based answer generation. It retrieves relevant FAQ entries and uses them as context for generating grounded answers using OpenAI's chat completion API. This module is the core of the RAG system, orchestrating retrieval and generation.

## Main Components

### Class: `RAGPipeline`

A class that implements the complete RAG pipeline from query to generated answer.

#### Initialization: `__init__(collection_name=None)`

**Parameters:**
- `collection_name` (str | list[str] | None, optional): One collection name or multiple collection names to search.
  - If `None`, defaults to `Config.CHROMA_COLLECTION_NAME`.
  - If a list is provided, retrieval will search across multiple collections (embedding strategies) and merge results.

**Behavior:**
- Initializes VectorSearch instance for retrieval
- Initializes OpenAI client for generation
- Stores both for use in pipeline

#### Method: `format_context(search_results)`

Formats search results into a context string for the LLM.

**Parameters:**
- `search_results` (list[dict]): List of search result dictionaries

**Returns:**
- `str`: Formatted context string with numbered entries and similarity scores

**Behavior:**
- Iterates through search results
- Formats each result with number, similarity score, and text
- Combines into a single context string
- Returns formatted context

#### Method: `generate_prompt(query, context)`

Generates a prompt for the LLM with retrieved context.

**Parameters:**
- `query` (str): User query
- `context` (str): Formatted context from search results

**Returns:**
- `str`: Complete prompt string for LLM

**Behavior:**
- Constructs a structured prompt with:
  - System instructions for the assistant
  - Retrieved context from FAQ database
  - User question
  - Instructions for answering
- Returns formatted prompt

#### Method: `generate_answer(query, top_k=None, threshold=None, model=None)`

Generates an answer using the complete RAG pipeline.

**Parameters:**
- `query` (str): User query
- `top_k` (int, optional): Number of documents to retrieve
- `threshold` (float, optional): Similarity threshold for retrieval
- `model` (str, optional): LLM model name (defaults to Config.LLM_MODEL)

**Returns:**
- `dict`: Result dictionary containing:
  - `answer` (str): Generated answer text
  - `retrieved_context` (list[dict]): List of retrieved FAQ entries
  - `metadata` (dict): Metadata including:
    - `num_retrieved` (int): Number of retrieved documents
    - `model` (str): Model used for generation
    - `query` (str): Original query
    - `error` (str, optional): Error message if generation failed

**Behavior:**
1. Retrieves relevant documents using VectorSearch (single collection or multi-collection merged search)
2. If no results found, returns error message
3. Formats retrieved context
4. Generates prompt with context and query
5. Calls OpenAI chat completion API
6. Extracts and returns generated answer
7. Handles errors and returns error information
8. Logs each step of the process

**Prompt Structure:**
The prompt instructs the LLM to:
- Answer based on provided context
- Indicate when context is insufficient
- Be concise and helpful
- Synthesize information from multiple entries when needed

## Dependencies

- `openai`: OpenAI API client library
- `config.Config`: For configuration values
- `retrieval.search`: For vector search functionality
- `logging`: For operation logging

## Assumptions

- VectorSearch is properly initialized and connected to indexed collection
- OpenAI API key is configured and valid
- LLM model is available and accessible
- Retrieved context is relevant to the query
- Temperature and max_tokens settings are appropriate for the use case
