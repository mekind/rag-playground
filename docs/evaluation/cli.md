# evaluation/cli.py Documentation

## Purpose and Responsibility

`cli.py` is the command-line entry point for running retrieval evaluation. It loads an evaluation dataset (JSONL), runs retrieval, computes metrics, and writes evaluation artifacts and human-readable reports to an output directory.

## Commands

### `retrieval-eval`

- **What it does**: runs labeled retrieval evaluation
- **Key arguments (typical)**
  - `--eval`: evaluation JSONL path
  - `--top-k`: top-k (defaults provided)
  - `--threshold`: similarity threshold (defaults provided)
  - `--out`: output directory (optional; can be timestamped)
  - `--collection-name`: Chroma collection name (optional)
  - `--fail-on-empty-gold`: whether to treat missing `gold_ids` as an error (optional)

## Outputs

- `per_sample.jsonl`: per-sample retrieval results and metrics
- `summary.json`: aggregated metrics
- `report.csv`, `report.md`: human-readable reports

## Dependencies and Assumptions

- The retrieval implementation follows the contract documented in [`docs/retrieval/search.md`](../retrieval/search.md).
