"""
Report generation for retrieval evaluation.

문서: docs/evaluation/retrieval_report.md
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Iterable


@dataclass(frozen=True)
class AggregateMetric:
    name: str
    avg: float
    std: float


def _safe_mean(values: list[float]) -> float:
    return 0.0 if len(values) == 0 else float(mean(values))


def _safe_std(values: list[float]) -> float:
    # population std; for 0/1 element lists return 0
    return 0.0 if len(values) <= 1 else float(pstdev(values))


def aggregate_metrics(per_sample: list[dict[str, Any]], metric_keys: list[str]) -> list[AggregateMetric]:
    metrics: list[AggregateMetric] = []
    for key in metric_keys:
        vals: list[float] = []
        for row in per_sample:
            v = row.get("metrics", {}).get(key)
            if isinstance(v, (int, float)):
                vals.append(float(v))
        metrics.append(AggregateMetric(name=key, avg=_safe_mean(vals), std=_safe_std(vals)))
    return metrics


def write_retrieval_report(
    *,
    per_sample: list[dict[str, Any]],
    out_dir: str | Path,
    metric_keys: list[str],
    top_n_failures: int = 20,
    sort_by: str | None = None,
) -> dict[str, Any]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    aggregates = aggregate_metrics(per_sample, metric_keys)

    # CSV summary
    csv_path = out / "report.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "avg", "std"])
        for m in aggregates:
            w.writerow([m.name, f"{m.avg:.6f}", f"{m.std:.6f}"])

    # Failures
    if sort_by is None:
        sort_by = metric_keys[0] if metric_keys else None

    failures = per_sample
    if sort_by:
        failures = sorted(
            per_sample,
            key=lambda r: float(r.get("metrics", {}).get(sort_by, 0.0)),
        )

    worst = failures[: max(0, top_n_failures)]

    md_path = out / "report.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Retrieval Eval Report\n\n")
        f.write(f"- samples: {len(per_sample)}\n\n")
        f.write("## Aggregate\n\n")
        f.write("| metric | avg | std |\n")
        f.write("|---|---:|---:|\n")
        for m in aggregates:
            f.write(f"| {m.name} | {m.avg:.6f} | {m.std:.6f} |\n")
        f.write("\n")

        if sort_by:
            f.write(f"## Worst samples (sorted by `{sort_by}`)\n\n")
        else:
            f.write("## Worst samples\n\n")

        for row in worst:
            qid = row.get("qid", "")
            query = row.get("query", "")
            gold_ids = row.get("gold_ids", [])
            retrieved_ids = row.get("retrieved_ids", [])
            metrics = row.get("metrics", {})
            f.write(f"### {qid}\n\n")
            f.write(f"- query: {query}\n")
            f.write(f"- gold_ids: {gold_ids}\n")
            f.write(f"- retrieved_ids: {retrieved_ids}\n")
            f.write(f"- metrics: {metrics}\n\n")

    return {
        "report_csv": str(csv_path),
        "report_md": str(md_path),
    }


