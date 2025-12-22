# evaluation/retrieval_runner.py 문서

## 목적/책임

`retrieval_runner.py`는 평가셋을 순회하며 retrieval 결과를 수집하고, `evaluation.retrieval_metrics`로 채점한 뒤 결과 아티팩트(JSONL)와 요약 리포트를 생성합니다.

검색 호출은 기본적으로 **단일 병합 랭킹**이 필요한 평가 목적에 맞춰 `retrieval.search.VectorSearch.search_merged()`를 사용합니다. (`VectorSearch.search()`는 임베딩 전략(컬렉션)별 결과를 분리 반환하는 형태이므로, 평가 러너의 기본 출력과는 맞지 않습니다.)

## 주요 컴포넌트

### 함수: `run_retrieval_eval(...)`

- 입력(핵심)
  - `eval_path`: 평가셋 JSONL 경로
  - `top_k`: 검색 top-k
  - `threshold`: 유사도 임계치
  - `out_dir`: 결과 저장 디렉토리
  - `collection_name`(옵션): Chroma 컬렉션명
- 출력
  - `RetrievalEvalSummary`(또는 dict): aggregate 지표 및 샘플 수, 실패/스킵 수 등
  - 파일 출력:
    - `per_sample.jsonl`: 샘플별 검색 결과 ID/메트릭
    - `summary.json`: 집계 메트릭

### per-sample 결과 스키마(예시)

```json
{
  "qid": "q001",
  "query": "...",
  "gold_ids": ["12","58"],
  "retrieved_ids": ["58","91","12","..."],
  "metrics": {"recall@5": 1.0, "mrr@5": 1.0, "ndcg@5": 1.0},
  "retrieved": [{"id":"58","similarity":0.82},{"id":"91","similarity":0.71}]
}
```

## 의존성/가정

- 검색 API는 문서 [`docs/retrieval/search.md`](../retrieval/search.md) 반환 스키마를 따름
- Chroma DB가 준비되어 있어야 검색이 실제로 수행됨
- 스킵 정책(예: gold_ids 누락)은 runner 옵션으로 제어 가능


