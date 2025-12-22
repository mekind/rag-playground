# evaluation/retrieval_metrics.py 문서

## 목적/책임

`retrieval_metrics.py`는 라벨 기반 retrieval 평가를 위한 **표준 랭킹 메트릭**을 계산합니다. 입력은 `retrieved_ids`(검색 결과 순서)와 `gold_ids`(정답 문서 ID 집합/리스트)이며, 출력은 per-sample 메트릭 딕셔너리입니다.

## 주요 컴포넌트

### 함수: `compute_retrieval_metrics(retrieved_ids, gold_ids, k)`

- 입력
  - `retrieved_ids` (list[str]): 검색 결과 문서 ID (rank 순서)
  - `gold_ids` (list[str]|set[str]): 정답 문서 ID
  - `k` (int): 컷오프
- 출력: `dict[str, float]` (예: `hit@k`, `recall@k`, `precision@k`, `mrr@k`, `ndcg@k`)

### 메트릭 정의

- Hit@k: top-k 안에 gold가 1개라도 있으면 1, 아니면 0
- Recall@k: \(|retrieved@k ∩ gold| / |gold|\)
- Precision@k: \(|retrieved@k ∩ gold| / k\)
- MRR@k: top-k 내 첫 정답의 rank \(r\)에 대해 \(1/r\), 없으면 0
- nDCG@k: binary relevance(정답이면 1) 기준 DCG/IDCG

## 가정/주의

- `retrieved_ids`는 중복이 없다고 가정(중복이 있을 경우 first occurrence 기준으로 계산)
- `gold_ids`가 비어 있으면 메트릭이 정의되지 않으므로 상위 레이어에서 스킵 또는 예외 처리 권장


