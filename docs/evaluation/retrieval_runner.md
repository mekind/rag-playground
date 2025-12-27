# evaluation/retrieval_runner.py Documentation

## Purpose and Responsibility

`retrieval_runner.py` iterates over a labeled retrieval evaluation dataset, runs retrieval, scores each sample using `evaluation.retrieval_metrics`, and writes evaluation artifacts (JSONL) plus a summary report.

Because evaluation typically needs a **single merged ranked list**, the runner uses `retrieval.search.VectorSearch.search_merged()` by default. (`VectorSearch.search()` returns results separated by embedding strategy/collection and is therefore not the default shape for evaluation outputs.)

## Main Components

### Function: `run_retrieval_eval(...)`

- **Inputs (core)**
  - `eval_path`: path to the evaluation JSONL
  - `top_k`: retrieval top-k
  - `threshold`: similarity threshold
  - `out_dir`: output directory (optional)
  - `collection_name`: Chroma collection name (optional)
- **Outputs**
  - `RetrievalEvalSummary` (or a dict): aggregate metrics and counts
  - Files written:
    - `per_sample.jsonl`: per-sample retrieved IDs and metrics
    - `summary.json`: aggregated metrics

### Per-sample output schema (example)

```json
{
  "qid": "q001",
  "query": "...",
  "gold_ids": ["12", "58"],
  "retrieved_ids": ["58", "91", "12", "..."],
  "metrics": {"recall@5": 1.0, "mrr@5": 1.0, "ndcg@5": 1.0},
  "retrieved": [{"id": "58", "similarity": 0.82}, {"id": "91", "similarity": 0.71}]
}
```

## Dependencies and Assumptions

- The retrieval API follows the contract documented in [`docs/retrieval/search.md`](../retrieval/search.md).
- A Chroma DB/collection must exist for retrieval to run.
- Skip policies (e.g., missing `gold_ids`) can be controlled by runner/test settings.
