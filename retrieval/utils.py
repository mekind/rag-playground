"""Utility functions for retrieval."""
import numpy as np
from typing import List, Tuple


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
    
    Returns:
        Cosine similarity score between -1 and 1
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def filter_by_threshold(results: List[dict], threshold: float) -> List[dict]:
    """
    Filter search results by similarity threshold.
    
    Args:
        results: List of search result dictionaries with 'distance' or 'score'
        threshold: Minimum similarity threshold
    
    Returns:
        Filtered list of results
    """
    filtered = []
    for result in results:
        # Chroma returns 'distance' (lower is better), convert to similarity
        if 'distance' in result:
            # Convert distance to similarity (assuming cosine distance)
            similarity = 1 - result['distance']
        elif 'score' in result:
            similarity = result['score']
        else:
            continue
        
        if similarity >= threshold:
            filtered.append(result)
    
    return filtered
