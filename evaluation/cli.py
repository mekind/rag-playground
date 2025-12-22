"""
CLI entrypoint for evaluation.

문서: docs/evaluation/cli.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from evaluation.retrieval_runner import run_retrieval_eval


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="evaluation")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("retrieval-eval", help="Run label-based retrieval evaluation")
    r.add_argument("--eval", dest="eval_path", required=True, help="Path to eval JSONL")
    r.add_argument("--top-k", dest="top_k", type=int, default=5, help="Top-k for retrieval")
    r.add_argument("--threshold", dest="threshold", type=float, default=0.0, help="Similarity threshold")
    r.add_argument("--out", dest="out_dir", default=None, help="Output directory (default: runs/retrieval_eval_...)")
    r.add_argument("--collection-name", dest="collection_name", default=None, help="Chroma collection name")
    r.add_argument("--top-n-failures", dest="top_n_failures", type=int, default=20, help="Worst samples to list")

    return p


def main(argv: list[str] | None = None) -> int:
    p = _build_parser()
    args = p.parse_args(argv)

    if args.command == "retrieval-eval":
        summary = run_retrieval_eval(
            eval_path=Path(args.eval_path),
            top_k=int(args.top_k),
            threshold=float(args.threshold),
            out_dir=None if args.out_dir is None else Path(args.out_dir),
            collection_name=None if args.collection_name in (None, "") else str(args.collection_name),
            top_n_failures=int(args.top_n_failures),
        )
        print(f"out_dir={summary.out_dir}")
        print(f"num_samples={summary.num_samples}")
        for k, v in summary.metric_avgs.items():
            print(f"{k}={v:.6f}")
        return 0

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())


