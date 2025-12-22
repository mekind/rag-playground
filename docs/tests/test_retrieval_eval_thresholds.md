# tests/test_retrieval_eval_thresholds.py 문서

## 목적/책임

`test_retrieval_eval_thresholds.py`는 retrieval 평가 파이프라인이 기대한 형태로 동작하는지, 그리고 **임계치(threshold) 기반 회귀 검증**을 수행할 수 있는지 확인합니다.

## 주요 테스트

### 1) 메트릭 단위 테스트(항상 실행)

- `evaluation.retrieval_metrics.compute_retrieval_metrics()`가 정의된 메트릭을 정확히 계산하는지 검증합니다.
- 외부 DB/네트워크에 의존하지 않는 순수 함수 테스트입니다.

### 2) 검색 통합 테스트(조건부 실행)

- 환경에 Chroma DB/컬렉션이 준비되어 있고 사용자가 실행을 허용한 경우에만 실행됩니다.
- 평가셋(JSONL)을 입력으로 `evaluation.retrieval_runner.run_retrieval_eval()`을 호출해 실제 검색 결과를 채점합니다.
- 임계치 값은 환경변수로 제어할 수 있습니다(기본값은 보수적으로 낮게 설정하여 기본 CI에서 불필요한 실패를 피함).

## 환경변수(권장)

- `RAG_PLAYGROUND_RUN_RETRIEVAL_EVAL=1`
  - 통합 테스트 실행 여부
- `RAG_PLAYGROUND_RECALL_MIN`
- `RAG_PLAYGROUND_MRR_MIN`
  - 통합 테스트에서 사용할 최소 임계치(예: `0.7`, `0.4`)


