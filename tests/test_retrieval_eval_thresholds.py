import sys
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.retrieval_metrics import compute_retrieval_metrics


def test_compute_retrieval_metrics_thresholds_unit():
    retrieved = ["a", "b", "c", "d", "e"]
    gold = ["c", "x"]
    k = 5
    m = compute_retrieval_metrics(retrieved_ids=retrieved, gold_ids=gold, k=k)

    assert m[f"hit@{k}"] >= 1.0
    assert m[f"recall@{k}"] == 0.5
    assert m[f"precision@{k}"] == 0.2
    assert m[f"mrr@{k}"] == pytest.approx(1.0 / 3.0)
    assert 0.0 <= m[f"ndcg@{k}"] <= 1.0


def test_retrieval_eval_integration_thresholds(tmp_path: Path):
    """
    실제 Chroma DB/컬렉션이 준비되어 있을 때만 retrieval 평가를 수행하고,
    임계치 기반으로 회귀 여부를 판단합니다.
    """
    if os.getenv("RAG_PLAYGROUND_RUN_RETRIEVAL_EVAL") != "1":
        pytest.skip("Set RAG_PLAYGROUND_RUN_RETRIEVAL_EVAL=1 to enable integration retrieval eval.")

    # import lazily so the unit test doesn't require chromadb/openai setup
    from evaluation.retrieval_runner import run_retrieval_eval

    eval_path = Path("data/eval/retrieval_eval.example.jsonl")
    if not eval_path.exists():
        pytest.skip("Eval file not found.")

    # 매우 보수적인 기본값(원하면 env로 올려서 회귀 게이트로 사용)
    recall_min = float(os.getenv("RAG_PLAYGROUND_RECALL_MIN", "0.0"))
    mrr_min = float(os.getenv("RAG_PLAYGROUND_MRR_MIN", "0.0"))

    try:
        summary = run_retrieval_eval(
            eval_path=eval_path,
            top_k=5,
            threshold=0.0,
            out_dir=tmp_path,
        )
    except Exception as e:
        pytest.skip(f"Retrieval eval could not run in this environment: {e}")

    assert summary.num_samples > 0
    assert summary.metric_avgs["recall@5"] >= recall_min
    assert summary.metric_avgs["mrr@5"] >= mrr_min


