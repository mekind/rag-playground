"""Generate embeddings using OpenAI API."""

from __future__ import annotations

import openai
import logging
from typing import TypeAlias
import time

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai.api_key = Config.OPENAI_API_KEY


EmbeddingVector: TypeAlias = list[float]
EmbeddingMatrix: TypeAlias = list[EmbeddingVector]


def get_embedding(text: str, model: str | None = None) -> EmbeddingVector:
    """
    Generate embedding for a single text using OpenAI API.

    Args:
        text: Text to embed
        model: Embedding model name (defaults to Config.EMBEDDING_MODEL)

    Returns:
        List of embedding values
    """
    if model is None:
        model = Config.EMBEDDING_MODEL

    try:
        # Use OpenAI client
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.embeddings.create(model=model, input=text)
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise


def get_embeddings_batch(
    texts: list[str], model: str | None = None, batch_size: int = 100
) -> EmbeddingMatrix:
    """
    Generate embeddings for multiple texts in batches.

    Args:
        texts: List of texts to embed
        model: Embedding model name
        batch_size: Number of texts to process in each batch

    Returns:
        List of embedding vectors
    """
    if model is None:
        model = Config.EMBEDDING_MODEL

    all_embeddings = []
    total = len(texts)

    logger.info(f"Generating embeddings for {total} texts...")

    for i in range(0, total, batch_size):
        batch = texts[i : i + batch_size]
        logger.info(
            f"Processing batch {i // batch_size + 1}/{(total + batch_size - 1) // batch_size}"
        )

        try:
            client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            response = client.embeddings.create(model=model, input=batch)

            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

            # Rate limiting - small delay between batches
            if i + batch_size < total:
                time.sleep(0.1)

        except Exception as e:
            logger.error(
                f"Error generating embeddings for batch {i // batch_size + 1}: {e}"
            )
            raise

    logger.info(f"Generated {len(all_embeddings)} embeddings")
    return all_embeddings
