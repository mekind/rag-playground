# evaluation/retrieval_dataset.py Documentation

## Purpose and Responsibility

`retrieval_dataset.py` loads and validates a **labeled retrieval evaluation dataset (JSONL)**. Each sample contains a user query (`query`) and a list of labeled relevant document IDs (`gold_ids`).

## Main Components

### Data structure: `RetrievalEvalSample`

- **Purpose**: canonical representation of one evaluation sample
- **Recommended fields**
  - `qid` (`str | None`): sample ID (can be auto-generated)
  - `query` (`str`): user query text
  - `gold_ids` (`list[str]`): relevant document IDs (recommended: non-empty)
  - `tags` (`list[str] | None`): optional tags (domain, difficulty, etc.)

### Function: `load_retrieval_eval_jsonl(path)`

- **Input**: JSONL file path
- **Output**: `list[RetrievalEvalSample]`
- **Behavior**
  - Parses JSONL line-by-line
  - Validates required keys (`query`, `gold_ids`)
  - Normalizes `gold_ids` into a list of strings
  - Invalid samples raise by default (or can be skipped by runner/test policy)

## Dataset schema (example)

Example file: `data/eval/retrieval_eval.example.jsonl`

```json
{"qid":"q001","query":"What should I do when my anxiety feels overwhelming?","gold_ids":["12","58"],"tags":["anxiety"]}
```

## Dependencies and Assumptions

- File format is UTF-8 JSONL
- `gold_ids` must be comparable to retrieved `id` values produced by the retrieval layer
