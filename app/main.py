"""Streamlit web application for RAG Lab."""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config import Config
from retrieval.search import VectorSearch
from retrieval.rag import RAGPipeline


def embedding_strategy_collections(base: str) -> list[str]:
    """Collections created by the indexing pipeline for embedding-strategy comparison."""
    return [
        f"{base}__question",
        f"{base}__answer",
        f"{base}__question_answer",
    ]


def collection_title(collection_name: str) -> str:
    """Human-friendly label for a strategy collection name."""
    if "__" not in collection_name:
        return collection_name
    suffix = collection_name.split("__", 1)[1]
    if suffix == "question":
        return "질문"
    if suffix == "answer":
        return "답변"
    if suffix == "question_answer":
        return "질문+답변"
    return suffix


# Page configuration
st.set_page_config(
    page_title="RAG Lab - Mental Health FAQ", page_icon="🧠", layout="wide"
)

# Initialize session state
if "search_engine" not in st.session_state:
    try:
        collections = embedding_strategy_collections(Config.CHROMA_COLLECTION_NAME)
        st.session_state.search_engine = VectorSearch(collection_name=collections)
        st.session_state.rag_pipeline = RAGPipeline(collection_name=collections)
    except Exception as e:
        st.error(f"Error initializing search engine: {e}")
        st.stop()

# Header
st.title("🧠 RAG Lab - Mental Health FAQ")
st.markdown(
    """
This is an experimental RAG (Retrieval-Augmented Generation) system for exploring 
how retrieval, embeddings, and LLM generation work together.

**⚠️ Disclaimer**: This project is for educational and research purposes only. 
It is not intended to provide medical or mental health advice.
"""
)

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")

    mode = st.radio(
        "Mode",
        ["RAG (Retrieval + Generation)", "Retrieval Only"],
        help="RAG mode uses LLM to generate answers. Retrieval Only shows raw search results.",
    )

    top_k = st.slider(
        "Number of results (Top-K)",
        min_value=1,
        max_value=10,
        value=Config.TOP_K,
        help="Number of FAQ entries to retrieve",
    )

    similarity_threshold = st.slider(
        "Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=Config.SIMILARITY_THRESHOLD,
        step=0.05,
        help="Minimum similarity score for results",
    )

# Main content
query = st.text_input(
    "Enter your question:",
    placeholder="e.g., What are the symptoms of anxiety?",
    key="query_input",
)

if st.button("Search", type="primary") or query:
    if not query:
        st.warning("Please enter a question.")
    else:
        try:
            if mode == "RAG (Retrieval + Generation)":
                # RAG mode
                with st.spinner("Generating answer..."):
                    result = st.session_state.rag_pipeline.generate_answer(
                        query, top_k=top_k, threshold=similarity_threshold
                    )

                # Display answer
                st.subheader("🤖 Generated Answer")
                st.write(result["answer"])

                # Display retrieved context
                if result["retrieved_context"]:
                    st.subheader("📚 Retrieved Context")
                    st.info(
                        f"Retrieved {result['metadata']['num_retrieved']} relevant FAQ entries"
                    )

                    for i, context_item in enumerate(result["retrieved_context"], 1):
                        with st.expander(
                            f"FAQ Entry {i} (Similarity: {context_item['similarity']:.3f})"
                        ):
                            st.write(context_item["text"])
                            if "metadata" in context_item:
                                st.caption(
                                    f"ID: {context_item['metadata'].get('id', 'N/A')}"
                                )
                else:
                    st.warning("No relevant context was retrieved.")

            else:
                # Retrieval only mode
                with st.spinner("Searching..."):
                    results = st.session_state.search_engine.search(
                        query, top_k=top_k, threshold=similarity_threshold
                    )

                # Backward-compatible normalization: support older list-style results too.
                if isinstance(results, list):
                    results_by_collection: dict[str, list[dict]] = {}
                    for item in results:
                        name = (
                            item.get("collection_name") or Config.CHROMA_COLLECTION_NAME
                        )
                        results_by_collection.setdefault(str(name), []).append(item)
                else:
                    results_by_collection = results

                total_found = sum(len(v) for v in results_by_collection.values())
                st.subheader(
                    f"🔍 Search Results ({total_found} found across {len(results_by_collection)} strategies)"
                )

                if total_found == 0:
                    st.warning(
                        "No results found. Try adjusting the similarity threshold or rephrasing your query."
                    )
                else:
                    collections = list(results_by_collection.keys())
                    tab_labels = [
                        f"{collection_title(name)} ({len(results_by_collection[name])})"
                        for name in collections
                    ]
                    tabs = st.tabs(tab_labels)
                    for tab, name in zip(tabs, collections):
                        with tab:
                            items = results_by_collection.get(name, [])
                            if not items:
                                st.info("No results for this strategy.")
                                continue
                            for i, item in enumerate(items, 1):
                                with st.expander(
                                    f"Result {i} - Similarity: {item['similarity']:.3f}"
                                ):
                                    st.write(item["text"])
                                    if "metadata" in item:
                                        st.caption(
                                            f"ID: {item['metadata'].get('id', 'N/A')}"
                                        )
                                        st.caption(
                                            f"Question: {item['metadata'].get('question', 'N/A')}"
                                        )
                                        st.caption(
                                            f"Answer: {item['metadata'].get('answer', 'N/A')}"
                                        )
                                    st.caption(f"Collection: {name}")

        except Exception as e:
            st.error(f"Error: {e}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    """
### About
This RAG system demonstrates:
- **Semantic Search**: Finding relevant information using embeddings
- **Retrieval-Augmented Generation**: Using retrieved context to generate grounded answers
- **Evaluation**: Understanding when the system works and when it fails

Built with OpenAI embeddings, Chroma vector database, and Streamlit.
"""
)
