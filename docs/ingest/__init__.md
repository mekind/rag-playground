# ingest/__init__.py Documentation

## Purpose and Responsibility

`ingest/__init__.py` declares the `ingest` directory as a Python package and (optionally) defines the package-level public API by re-exporting commonly used functions.

Based on existing module documentation, the `ingest` package centers around:

- `ingest/embed.py`: Generate embeddings for text (single and batch).
- `ingest/index.py`: Index processed FAQ data into a Chroma vector database.

## Main Components

### Package initializer: `ingest/__init__.py`

**Typical responsibilities:**

- Mark `ingest` as a package
- Optionally re-export selected symbols for ergonomic imports (e.g., `from ingest import get_embedding`)
- Optionally define metadata such as `__all__` and `__version__`

## Public API Policy (Decision Needed)

Choose one of the following and keep `__init__.py` and this document aligned:

- **Policy A (explicit module imports)**: Users import directly from submodules, e.g. `from ingest.embed import get_embedding`.
- **Policy B (package-level re-exports)**: `ingest/__init__.py` re-exports key functions so users can do `from ingest import get_embedding`.

> If you tell me whether you prefer Policy A or B, I will update this document (and `ingest/__init__.py` if needed) to match.


