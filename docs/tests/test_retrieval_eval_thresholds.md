# tests/test_retrieval_eval_thresholds.py Documentation

## Purpose and Responsibility

`test_retrieval_eval_thresholds.py` verifies that the retrieval evaluation pipeline behaves as expected and supports **threshold-based regression checks** (guardrails against quality degradation).

## Main tests

### 1) Metric unit tests (always run)

- Validates that `evaluation.retrieval_metrics.compute_retrieval_metrics()` computes the defined metrics correctly.
- Pure function tests that do not depend on external DB/network resources.

### 2) Retrieval integration test (conditionally run)

- Runs only when a Chroma DB/collection is available and the user explicitly enables it.
- Calls `evaluation.retrieval_runner.run_retrieval_eval()` on an evaluation dataset (JSONL) and scores real retrieval outputs.
- Thresholds are controlled via environment variables (defaults are intentionally conservative to avoid unnecessary failures in basic CI runs).

## Environment variables (recommended)

- `RAG_PLAYGROUND_RUN_RETRIEVAL_EVAL=1`
  - whether to run the integration test
- `RAG_PLAYGROUND_RECALL_MIN`
- `RAG_PLAYGROUND_MRR_MIN`
  - minimum thresholds used by the integration test (e.g. `0.7`, `0.4`)
