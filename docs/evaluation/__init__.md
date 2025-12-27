# evaluation package Documentation

## Purpose and Responsibility

`evaluation/` is a collection of modules for **offline evaluation** of the RAG system (especially retrieval quality). The package scores retrieval outputs against a labeled dataset (`query` + `gold_ids`), writes evaluation artifacts and summary reports, and supports regression checks via `pytest`.

## Main Components

- `evaluation.retrieval_dataset`
  - loads/validates the JSONL evaluation dataset
- `evaluation.retrieval_metrics`
  - computes Hit@k, Recall@k, Precision@k, MRR@k, nDCG@k
- `evaluation.retrieval_runner`
  - runs retrieval (via `retrieval.search.VectorSearch`) and writes per-sample + aggregate results
- `evaluation.retrieval_report`
  - generates CSV/Markdown reports
- `evaluation.cli`
  - command-line entry point for running evaluation

## Inputs/Outputs (summary)

- Input: evaluation datasets in `data/eval/*.jsonl`
- Output: results JSONL + summary reports (CSV/MD) under `runs/eval_.../`

## Dependencies and Assumptions

- The retrieval API follows [`docs/retrieval/search.md`](../retrieval/search.md).
- A Chroma DB/collection must exist for end-to-end retrieval evaluation.
