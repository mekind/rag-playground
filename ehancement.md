
# Retrieval-Focused RAG Enhancement Notes (FAQ Chatbot)

## Current State
- Built a simple FAQ chatbot using RAG.
- Next focus: improve **retrieval quality and reliability** (dense vector search only).
- Evaluation preference: **offline evaluation** (labeled dataset, automated metrics).

## What to Try (Dense-Only → Practical Improvements)
### 1) Chunking / Index Unit Design (highest priority)
- FAQ data is structured (Question/Answer/Category/Tags). Retrieval quality heavily depends on the indexing unit.
- Try indexing variants:
  - **Q-only** (often best for matching user queries)
  - **A-only**
  - **Q+A** combined
- Keep attributes like category/product/version/channel as **metadata**, not mixed into the main text, and test their impact.

### 2) Metadata Filtering (precision boost)
- Use metadata filters (e.g., product, language, channel, version) to narrow candidates before similarity search.
- This often improves accuracy more than model changes when metadata is reliable.

### 3) Query Normalization & Expansion (recall boost)
- Handle common FAQ issues:
  - Synonyms/aliases (e.g., refund/cancel/return)
  - Abbreviations
  - Typos
  - Korean text normalization (spacing, morphology-aware normalization if applicable)
- Add lightweight query expansion rules or a small synonym dictionary.

### 4) Multi-Query / Query Decomposition (for complex questions)
- For multi-intent questions, generate 2–4 paraphrases/sub-queries, retrieve for each, then merge results.
- Improves recall without immediately introducing new infrastructure.

### 5) Diversity in Retrieval (reduce duplicates)
- Apply diversity-aware selection (e.g., MMR) so top-k is not filled with near-duplicates.
- Useful when the knowledge base has many similar FAQ entries.

### 6) Embedding Model & Similarity Settings (foundational check)
- Validate:
  - Korean / multilingual embedding suitability
  - cosine vs inner product behavior
  - preprocessing consistency (special chars, whitespace, boilerplate removal)

### 7) Next-Step Upgrades (after metrics are in place)
- **Hybrid retrieval (BM25 + dense)** to improve recall.
- **Cross-encoder reranking** to improve precision/ordering.

## How to Measure (Offline Retrieval Metrics)
### Core Metrics (recommended)
- **Recall@k (HitRate@k)**: whether the gold item appears in top-k (very intuitive for FAQ).
- **MRR@k**: emphasizes ranking quality (gold appearing earlier is better).
- **nDCG@k**: best when you can assign graded relevance (partial matches, multiple correct answers).

### Supporting Metrics (operations & debugging)
- **Precision@k**: useful if multiple gold items exist.
- **No-hit rate / Coverage**: fraction of queries with no relevant candidates retrieved.
- **Latency (p50/p95)**: measure speed alongside quality.

### Choosing k
- Fix k based on how many candidates you pass downstream (reranker/LLM context).
- Example: if you plan to use 4–8 contexts, track Recall@5/10 and MRR@10.

## Offline Evaluation Dataset (Labeling Strategy)
- Minimal format: (query, gold_doc_id or gold_chunk_id)
- For FAQ, labeling can be simple:
  - Use the **FAQ entry ID** as gold.
  - Compare indexing strategies (Q vs A vs Q+A) using the same labeled set.

## Recommended Next Steps
1. Build/confirm a labeled offline eval set (even small, e.g., 50–200 queries).
2. Baseline retrieval: current dense-only setup → record Recall@k, MRR@k, latency.
3. Run controlled experiments:
   - chunking variants
   - metadata filtering
   - query normalization/expansion
   - multi-query
   - diversity (MMR)
4. Only then move to hybrid retrieval and reranking.

