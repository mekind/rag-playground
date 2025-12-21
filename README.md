# RAG Lab

This repository is a personal lab for studying and experimenting with
Retrieval-Augmented Generation (RAG) systems.

The goal of this project is not to build a single chatbot,
but to understand how retrieval, embeddings, chunking strategies,
and evaluation methods affect the quality and reliability of LLM-based systems.

This repository serves as:
- a learning space for RAG fundamentals
- an experimental playground for retrieval strategies
- a technical portfolio demonstrating system-level thinking around RAG

---

## Why RAG?

Large Language Models are powerful at generating fluent text,
but they have fundamental limitations:
- knowledge is frozen at training time
- hallucinations occur when reliable grounding is missing
- long or domain-specific documents are difficult to handle accurately

RAG addresses these issues by separating **knowledge retrieval**
from **language generation**, allowing models to reason over
external, up-to-date, and verifiable sources.

This project focuses on understanding **how well RAG actually works**
and **where it fails**.

---

## First Experiment: Mental Health FAQ RAG

The first experiment in this repository uses a public FAQ dataset:

- Dataset: *Mental Health FAQ for Chatbot* (Kaggle)
- Domain: Mental health informational FAQs
- Structure: Question–Answer pairs

This dataset was chosen because:
- it is small enough for rapid experimentation
- it clearly exposes retrieval quality issues
- it allows comparison between retrieval-only and RAG-based approaches

⚠️ Disclaimer:
This project is for **educational and research purposes only**.
It is not intended to provide medical or mental health advice.
For serious mental health concerns, professional help should be sought.

---

## System Overview

The current system follows a simple RAG pipeline:

1. User query is converted into an embedding
2. Relevant FAQ entries are retrieved via semantic search
3. Retrieved content is provided to an LLM as context
4. The model generates a grounded answer based on retrieved information

The system is intentionally kept simple at first,
so that each component can be evaluated and replaced independently.

---

## Project Structure

```
rag-lab/
├─ data/ # Dataset references and preprocessing scripts
├─ ingest/ # Embedding generation and indexing
├─ retrieval/ # Vector search and retrieval logic
├─ app/ # Demo application (Streamlit / CLI)
├─ eval/ # Evaluation notebooks and scripts
├─ experiments/ # Chunking, retrieval, and ranking experiments
└─ README.md
```


(Structure may evolve as experiments grow.)

---

## Getting Started

### Prerequisites

- Python 3.12 or higher
- OpenAI API key
- (Optional) Kaggle API credentials for dataset download

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd rag-playground
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env  # If .env.example exists
   ```
   
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   EMBEDDING_MODEL=text-embedding-ada-002
   LLM_MODEL=gpt-3.5-turbo
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   CHROMA_COLLECTION_NAME=mental_health_faq
   TOP_K=5
   SIMILARITY_THRESHOLD=0.7
   ```
   
   For Kaggle dataset download (optional):
   ```env
   KAGGLE_USERNAME=your_kaggle_username
   KAGGLE_KEY=your_kaggle_key
   ```

### Data Setup

1. **Download the dataset**:
   ```bash
   python data/download_faq.py
   ```
   
   Alternatively, manually download the Mental Health FAQ dataset from Kaggle and place it in `data/raw/`.

2. **Preprocess the data**:
   ```bash
   python data/preprocess.py
   ```
   
   This will create `data/processed/faq_processed.json`.

3. **Generate embeddings and index**:
   ```bash
   python ingest/index.py
   ```
   
   This will create embeddings for all FAQ entries and store them in Chroma database.

### Running the Application

**Start the Streamlit web application**:
```bash
streamlit run app/main.py
```

The application will open in your browser at `http://localhost:8501`.

### Usage

1. **Enter a question** in the query input field
2. **Choose a mode**:
   - **RAG (Retrieval + Generation)**: Uses LLM to generate answers based on retrieved context
   - **Retrieval Only**: Shows only the raw search results
3. **Adjust settings** (optional):
   - Top-K: Number of results to retrieve
   - Similarity Threshold: Minimum similarity score for results
4. **View results**: See the generated answer (RAG mode) or search results (Retrieval Only mode)

---

## Key Topics Explored

- Semantic search vs keyword search
- Embeddings and cosine similarity
- Retrieval quality and failure modes
- Top-k and similarity threshold tuning
- RAG vs retrieval-only baselines
- Groundedness and hallucination reduction
- Practical trade-offs in vector storage

---

## Evaluation Approach

Evaluation in this project focuses on:
- whether the correct information is retrieved (retrieval quality)
- whether generated answers are grounded in retrieved content
- when the system should refuse to answer due to low confidence

Quantitative metrics are combined with qualitative analysis,
as RAG performance cannot be fully captured by a single score.

---

## Future Directions

Planned experiments include:
- alternative embedding models
- hybrid search (keyword + vector)
- reranking strategies
- different chunking approaches
- expanding to other document-based domains

---

## Motivation

This repository exists to move beyond "RAG tutorials"
and towards a deeper understanding of retrieval-augmented systems.

The emphasis is on **reasoning about system behavior**,
not just making the system work.

---

## License

GNU Affero General Public License v3.0 


