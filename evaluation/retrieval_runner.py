"""
Runner for label-based retrieval evaluation.

문서: docs/evaluation/retrieval_runner.md
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from evaluation.retrieval_dataset import RetrievalEvalSample, load_retrieval_eval_jsonl
from evaluation.retrieval_metrics import compute_retrieval_metrics
from evaluation.retrieval_report import write_retrieval_report
from retrieval.search import VectorSearch


@dataclass(frozen=True)
class RetrievalEvalSummary:
    k: int
    threshold: float
    num_samples: int
    metric_avgs: dict[str, float]
    out_dir: str


def _now_ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def run_retrieval_eval(
    *,
    eval_path: str | Path,
    top_k: int,
    threshold: float,
    out_dir: str | Path | None = None,
    collection_name: str | None = None,
    top_n_failures: int = 20,
) -> RetrievalEvalSummary:
    samples = load_retrieval_eval_jsonl(eval_path)

    out = (
        Path(out_dir)
        if out_dir is not None
        else Path("runs") / f"retrieval_eval_{_now_ts()}"
    )
    out.mkdir(parents=True, exist_ok=True)

    vs = VectorSearch(collection_name=collection_name)

    per_sample_path = out / "per_sample.jsonl"
    per_sample_rows: list[dict[str, Any]] = []

    metric_keys = [
        f"hit@{top_k}",
        f"recall@{top_k}",
        f"precision@{top_k}",
        f"mrr@{top_k}",
        f"ndcg@{top_k}",
    ]

    with per_sample_path.open("w", encoding="utf-8") as f:
        for s in samples:
            t0 = time.perf_counter()
            results = vs.search_merged(s.query, top_k=top_k, threshold=threshold)
            dt_ms = (time.perf_counter() - t0) * 1000.0

            retrieved_ids: list[str] = [str(r.get("id")) for r in results if "id" in r]
            metrics = compute_retrieval_metrics(
                retrieved_ids=retrieved_ids, gold_ids=s.gold_ids, k=top_k
            )

            retrieved_compact = [
                {"id": str(r.get("id")), "similarity": float(r.get("similarity", 0.0))}
                for r in results
                if "id" in r
            ]

            row = {
                "qid": s.qid,
                "query": s.query,
                "gold_ids": list(s.gold_ids),
                "tags": list(s.tags),
                "retrieved_ids": retrieved_ids[:top_k],
                "retrieved": retrieved_compact[:top_k],
                "metrics": metrics,
                "latency_ms": dt_ms,
            }
            per_sample_rows.append(row)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # summary.json
    metric_avgs: dict[str, float] = {}
    for key in metric_keys:
        vals = [float(r["metrics"].get(key, 0.0)) for r in per_sample_rows]
        metric_avgs[key] = sum(vals) / float(len(vals)) if vals else 0.0

    summary_obj = {
        "k": top_k,
        "threshold": threshold,
        "num_samples": len(per_sample_rows),
        "metric_avgs": metric_avgs,
        "per_sample_path": str(per_sample_path),
    }
    (out / "summary.json").write_text(
        json.dumps(summary_obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # report
    write_retrieval_report(
        per_sample=per_sample_rows,
        out_dir=out,
        metric_keys=metric_keys,
        top_n_failures=top_n_failures,
        sort_by=f"mrr@{top_k}",
    )

    return RetrievalEvalSummary(
        k=top_k,
        threshold=threshold,
        num_samples=len(per_sample_rows),
        metric_avgs=metric_avgs,
        out_dir=str(out),
    )
