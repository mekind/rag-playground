"""
evaluation package

라벨 기반 retrieval 평가 및 리포트 생성을 위한 패키지.
문서: docs/evaluation/__init__.md
"""

from .retrieval_dataset import RetrievalEvalSample, load_retrieval_eval_jsonl
from .retrieval_metrics import compute_retrieval_metrics

__all__ = [
    "RetrievalEvalSample",
    "load_retrieval_eval_jsonl",
    "compute_retrieval_metrics",
]


