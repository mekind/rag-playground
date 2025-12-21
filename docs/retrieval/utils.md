# retrieval/utils.py Documentation

## Purpose and Responsibility

The `utils.py` module provides utility functions for retrieval operations, including similarity calculations and result filtering. These are helper functions used by the search and RAG modules to process and filter search results.

## Main Components

### Function: `cosine_similarity(vec1, vec2)`

Calculates cosine similarity between two vectors.

**Parameters:**
- `vec1` (list[float]): First vector
- `vec2` (list[float]): Second vector

**Returns:**
- `float`: Cosine similarity score between -1 and 1

**Behavior:**
- Converts inputs to numpy arrays
- Calculates dot product and vector norms
- Returns normalized cosine similarity
- Returns 0.0 if either vector has zero norm

### Function: `filter_by_threshold(results, threshold)`

Filters search results by similarity threshold.

**Parameters:**
- `results` (list[dict]): List of search result dictionaries
- `threshold` (float): Minimum similarity threshold

**Returns:**
- `list[dict]`: Filtered list of results meeting the threshold

**Behavior:**
- Iterates through results
- Extracts similarity score from either 'distance' or 'score' field
- Converts distance to similarity if needed (assuming cosine distance: similarity = 1 - distance)
- Filters results where similarity >= threshold
- Returns filtered list

**Result Dictionary Structure:**
Results should contain either:
- `distance`: Distance value (lower is better, will be converted to similarity)
- `score`: Direct similarity score

## Dependencies

- `numpy`: For vector operations and mathematical calculations

## Assumptions

- Input vectors are valid numerical lists of the same length
- Results contain either 'distance' or 'score' fields
- Distance values represent cosine distance (convertible to similarity)
