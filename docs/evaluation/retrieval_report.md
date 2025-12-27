# evaluation/retrieval_report.py Documentation

## Purpose and Responsibility

`retrieval_report.py` summarizes retrieval evaluation results (per-sample metrics and aggregates) in a human-readable form. Default outputs are CSV and Markdown, and it can also include a list of failure cases (low-scoring samples).

## Main Components

### Function: `write_retrieval_report(...)`

- **Inputs**
  - per-sample results list (or a per-sample JSONL path)
  - output directory
  - `k` (cutoff)
  - `top_n_failures` (optional)
- **Outputs**
  - `report.csv`: aggregate metrics (mean/stddev, sample counts, etc.)
  - `report.md`: summary plus failure-case list

## Suggested report contents

- Overall averages: `Hit@k`, `Recall@k`, `MRR@k`, `nDCG@k`
- Sample count / skipped count
- Worst samples: top N by lowest `mrr@k` or `recall@k`

## Suggested output files

- `report.csv`
  - aggregate metrics (mean/stddev), sample counts, skipped counts
- `report.md`
  - summary table + failure-case list (query, `gold_ids`, `retrieved_ids`, key metrics)

## Dependencies and Assumptions

- Assumes inputs are per-sample results produced by the runner (including computed metrics).