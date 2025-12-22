"""
Retrieval metrics for label-based evaluation.

문서: docs/evaluation/retrieval_metrics.md
"""

from __future__ import annotations

import math
from typing import Iterable


def _dcg_binary(rels: list[int]) -> float:
    # rank is 1-based; DCG uses log2(rank+1)
    dcg = 0.0
    for i, rel in enumerate(rels, start=1):
        if rel <= 0:
            continue
        dcg += float(rel) / math.log2(i + 1)
    return dcg


def compute_retrieval_metrics(
    retrieved_ids: list[str],
    gold_ids: Iterable[str],
    k: int,
) -> dict[str, float]:
    if k <= 0:
        raise ValueError("k must be > 0")

    gold_set = {str(x) for x in gold_ids}
    if len(gold_set) == 0:
        raise ValueError("gold_ids must be non-empty")

    topk = [str(x) for x in retrieved_ids[:k]]

    hits = [1 if doc_id in gold_set else 0 for doc_id in topk]
    hit_at_k = 1.0 if any(hits) else 0.0

    intersection = sum(hits)
    recall_at_k = float(intersection) / float(len(gold_set))
    precision_at_k = float(intersection) / float(k)

    mrr_at_k = 0.0
    for rank, doc_id in enumerate(topk, start=1):
        if doc_id in gold_set:
            mrr_at_k = 1.0 / float(rank)
            break

    dcg = _dcg_binary(hits)
    ideal_len = min(len(gold_set), k)
    idcg = _dcg_binary([1] * ideal_len)
    ndcg_at_k = 0.0 if idcg == 0.0 else (dcg / idcg)

    return {
        f"hit@{k}": hit_at_k,
        f"recall@{k}": recall_at_k,
        f"precision@{k}": precision_at_k,
        f"mrr@{k}": mrr_at_k,
        f"ndcg@{k}": ndcg_at_k,
    }


