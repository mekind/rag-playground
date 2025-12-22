# retrieval/__init__.py Documentation

## Purpose and Responsibility

The `retrieval` package groups retrieval-related modules used by the project’s RAG system. It provides:

- Vector search capabilities (via `retrieval.search`)
- RAG orchestration (via `retrieval.rag`)
- Shared helper utilities for retrieval operations (via `retrieval.utils`)

This `__init__.py` file exists to mark `retrieval/` as a Python package and (optionally) define a stable public API via re-exports.

## Main Components

### Package-level responsibilities

- Defines the `retrieval` package boundary for imports.
- Optionally re-exports key classes/functions (if maintained as part of the public API).

### Related modules

- `retrieval.search`: Implements `VectorSearch` for querying the Chroma collection.
- `retrieval.rag`: Implements `RAGPipeline` to combine retrieval + LLM generation.
- `retrieval.utils`: Utility functions such as similarity calculations and threshold filtering.

## Assumptions

- The package’s public API (if any) should be documented and kept stable to avoid breaking downstream imports.


