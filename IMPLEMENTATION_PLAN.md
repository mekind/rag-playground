# RAG Lab Implementation Plan

## Project Overview

This plan outlines the implementation of a minimal RAG (Retrieval-Augmented Generation) system using the Mental Health FAQ dataset. The implementation will be done from scratch (custom approach) to ensure a clear understanding of each component's behavior.

## Technology Stack

- **Python**: 3.12
- **Embedding Model**: OpenAI API (text-embedding-ada-002 or text-embedding-3)
- **Vector Database**: Chroma (local, simple to start)
- **LLM**: OpenAI API (gpt-3.5-turbo or gpt-4)
- **Application Interface**: Streamlit (web UI)
- **Dependency Management**: requirements.txt
- **Environment Variables**: .env file (python-dotenv)

## Implementation Steps

### 1. Project Structure and Basic Setup

Create the directory structure as specified in the README:
- `data/` - Dataset and preprocessing scripts
- `ingest/` - Embedding generation and indexing
- `retrieval/` - Vector search and retrieval logic
- `app/` - Streamlit demo application
- `eval/` - Evaluation notebooks and scripts
- `experiments/` - Chunking, retrieval, and ranking experiments

Create configuration files:
- `requirements.txt` - Required Python packages
- `.env.example` - API key template
- `.gitignore` - Git ignore rules

### 2. Dataset Download and Preprocessing

- `data/download_faq.py`: Script to download the Kaggle Mental Health FAQ dataset
- `data/preprocess.py`: Script to clean and organize FAQ data into Q-A pairs
- Save the dataset in JSON or CSV format

### 3. Basic Search System Implementation

- `ingest/embed.py`: Convert text to vectors using OpenAI embedding API
- `ingest/index.py`: Index and store embeddings using Chroma
- `retrieval/search.py`: Generate query embeddings and search for similar FAQs in Chroma
- `retrieval/utils.py`: Utility functions (cosine similarity calculation, etc.)

### 4. Simple RAG Pipeline

- `retrieval/rag.py`: Construct prompts for LLM using retrieved FAQs as context
- Call OpenAI API to generate answers based on retrieved information
- Implement basic prompt templates

### 5. Streamlit Application

- `app/main.py`: Streamlit web interface
  - Query input field
  - Display search results (retrieval-only mode)
  - Display RAG answers
  - Highlight retrieved FAQ items
  - Show similarity scores

### 6. Basic Configuration and Documentation

- Manage API keys and settings via `config.py` or environment variables
- Add execution instructions to README
- Include basic usage examples

## File Structure

```
rag-lab/
├── data/
│   ├── download_faq.py
│   ├── preprocess.py
│   └── (downloaded data files)
├── ingest/
│   ├── embed.py
│   └── index.py
├── retrieval/
│   ├── search.py
│   ├── rag.py
│   └── utils.py
├── app/
│   └── main.py
├── eval/
│   └── (to be added later)
├── experiments/
│   └── (to be added later)
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── IMPLEMENTATION_PLAN.md
```

## Key Implementation Points

1. **Modularity**: Separate each component so they can be tested independently
2. **Error Handling**: Handle exception cases such as API call failures, missing data, etc.
3. **Logging**: Record progress at each step with logs
4. **Configuration Management**: Avoid hardcoding, use configuration files or environment variables

## Implementation Priority

Start with minimal functionality:
1. Basic search system (embedding + retrieval)
2. Simple RAG (retrieval → LLM generation)
3. Expand with additional features

## Next Steps (Future Expansion)

- Implement evaluation metrics (`eval/`)
- Experiment with different chunking strategies
- Hybrid search (keyword + vector)
- Reranking strategies
- Compare different embedding models

## Tasks

- [ ] Setup project structure and configuration files (.gitignore, .env.example, requirements.txt)
- [ ] Implement dataset download and preprocessing scripts (data/download_faq.py, data/preprocess.py)
- [ ] Implement OpenAI embedding generation and Chroma indexing (ingest/embed.py, ingest/index.py)
- [ ] Implement vector search system (retrieval/search.py, retrieval/utils.py)
- [ ] Implement RAG pipeline - use search results as LLM context (retrieval/rag.py)
- [ ] Implement Streamlit web app - query input, search results, RAG answers display (app/main.py)
