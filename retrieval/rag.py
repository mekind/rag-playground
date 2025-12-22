"""RAG pipeline: Retrieve and generate answers."""

import openai
import logging
from collections.abc import Sequence
from typing import Any

from config import Config
from retrieval.search import VectorSearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai.api_key = Config.OPENAI_API_KEY


class RAGPipeline:
    """RAG pipeline combining retrieval and generation."""

    def __init__(self, collection_name: str | Sequence[str] | None = None):
        """
        Initialize RAG pipeline.

        Args:
            collection_name: Name(s) of Chroma collection(s)
        """
        self.search = VectorSearch(collection_name=collection_name)
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

    def format_context(self, search_results: list[dict[str, Any]]) -> str:
        """
        Format search results into context string for LLM.

        Args:
            search_results: List of search result dictionaries

        Returns:
            Formatted context string
        """
        context_parts = []
        for i, result in enumerate(search_results, 1):
            text = result.get("text", "")
            similarity = result.get("similarity", 0.0)
            collection_name = result.get("collection_name")
            collection_suffix = (
                f", Collection: {collection_name}"
                if isinstance(collection_name, str)
                else ""
            )
            context_parts.append(
                f"[{i}] (Similarity: {similarity:.3f}{collection_suffix})\n{text}\n"
            )

        return "\n".join(context_parts)

    def generate_prompt(self, query: str, context: str) -> str:
        """
        Generate prompt for LLM with retrieved context.

        Args:
            query: User query
            context: Retrieved context from search

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a helpful assistant that answers questions based on the provided context from a mental health FAQ database.

Context from FAQ database:
{context}

User Question: {query}

Instructions:
1. Answer the question based on the provided context.
2. If the context doesn't contain relevant information, say "I don't have enough information to answer this question accurately."
3. Be concise and helpful.
4. If multiple relevant FAQ entries are provided, synthesize the information appropriately.

Answer:"""
        return prompt

    def generate_answer(
        self,
        query: str,
        top_k: int | None = None,
        threshold: float | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate answer using RAG pipeline.

        Args:
            query: User query
            top_k: Number of documents to retrieve
            threshold: Similarity threshold for retrieval
            model: LLM model name (defaults to Config.LLM_MODEL)

        Returns:
            Dictionary with answer, retrieved context, and metadata
        """
        if model is None:
            model = Config.LLM_MODEL

        # Step 1: Retrieve relevant documents
        logger.info(f"Retrieving documents for query: {query}")
        search_results = self.search.search(query, top_k=top_k, threshold=threshold)

        if not search_results:
            return {
                "answer": "I couldn't find relevant information in the FAQ database to answer your question.",
                "retrieved_context": [],
                "metadata": {"num_retrieved": 0, "model": model},
            }

        # Step 2: Format context
        context = self.format_context(search_results)

        # Step 3: Generate prompt
        prompt = self.generate_prompt(query, context)

        # Step 4: Call LLM
        logger.info(f"Generating answer using {model}...")
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions based on provided context.",
                    },
                    {"role": "user", "content": prompt},
                ],
                # temperature=0.7,
                max_completion_tokens=500,
            )

            answer = response.choices[0].message.content.strip()

            return {
                "answer": answer,
                "retrieved_context": search_results,
                "metadata": {
                    "num_retrieved": len(search_results),
                    "model": model,
                    "query": query,
                },
            }

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "retrieved_context": search_results,
                "metadata": {
                    "num_retrieved": len(search_results),
                    "model": model,
                    "error": str(e),
                },
            }
