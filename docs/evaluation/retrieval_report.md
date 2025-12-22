# evaluation/retrieval_report.py 문서

## 목적/책임

`retrieval_report.py`는 retrieval 평가 결과(샘플별 메트릭 및 집계값)를 사람이 읽기 좋은 형태로 요약합니다. 기본 출력은 CSV 및 Markdown이며, 실패 케이스(낮은 점수 샘플)도 함께 제공합니다.

## 주요 컴포넌트

### 함수: `write_retrieval_report(...)`

- 입력
  - per-sample 결과 리스트(또는 per-sample JSONL 경로)
  - 출력 디렉토리
  - `k` (컷오프)
  - `top_n_failures` (옵션)
- 출력
  - `report.csv`: aggregate 메트릭(평균/표준편차/샘플 수 등)
  - `report.md`: 요약 + 실패 케이스 리스트

## 리포트 내용(권장)

- Overall(평균): `Hit@k`, `Recall@k`, `MRR@k`, `nDCG@k`
- 샘플 수/스킵 수
- Worst samples: `mrr@k` 또는 `recall@k`가 낮은 순 상위 N개

## 출력 파일(권장)

- `report.csv`
  - 집계 메트릭(평균/표준편차), 샘플 수, 스킵 수
- `report.md`
  - 요약 테이블 + 실패 케이스 목록(질문, gold_ids, retrieved_ids, 주요 메트릭)

## 의존성/가정

- runner가 생성한 per-sample 결과(메트릭 포함)를 입력으로 받는다고 가정합니다.

