# evaluation/retrieval_metrics.py Documentation

## Purpose and Responsibility

`retrieval_metrics.py` computes standard ranking metrics for labeled retrieval evaluation. Inputs are `retrieved_ids` (ranked list of retrieved document IDs) and `gold_ids` (set/list of relevant document IDs). Output is a per-sample metrics dictionary.

## Main Components

### Function: `compute_retrieval_metrics(retrieved_ids, gold_ids, k)`

- **Inputs**
  - `retrieved_ids` (`list[str]`): ranked retrieved document IDs
  - `gold_ids` (`list[str] | set[str]`): relevant (gold) document IDs
  - `k` (`int`): cutoff
- **Output**: `dict[str, float]` (e.g. `hit@k`, `recall@k`, `precision@k`, `mrr@k`, `ndcg@k`)

### Metric definitions

- **Hit@k**: 1 if at least one relevant item appears in the top-k, else 0
- **Recall@k**: \(|retrieved@k \cap gold| / |gold|\)
- **Precision@k**: \(|retrieved@k \cap gold| / k\)
- **MRR@k**: \(1/r\) where \(r\) is the rank of the first relevant item within top-k; 0 if none
- **nDCG@k**: DCG/IDCG under binary relevance (relevant=1, non-relevant=0)

## Assumptions and Notes

- `retrieved_ids` is assumed to be de-duplicated. If duplicates exist, metrics should use the first occurrence.
- If `gold_ids` is empty, metrics are undefined; the caller should skip the sample or raise an error.
