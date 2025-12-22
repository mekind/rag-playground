# evaluation/cli.py 문서

## 목적/책임

`cli.py`는 retrieval 평가를 커맨드라인에서 실행할 수 있게 하는 진입점입니다. 평가셋(JSONL)을 입력으로 받아 검색을 수행하고, 메트릭을 계산한 뒤 결과 아티팩트와 리포트를 지정한 디렉토리에 저장합니다.

## 주요 커맨드

### `retrieval-eval`

- 기능: 라벨 기반 retrieval 평가 실행
- 주요 인자(예정)
  - `--eval`: 평가셋 JSONL 경로
  - `--top-k`: top-k (기본값 제공)
  - `--threshold`: 유사도 임계치 (기본값 제공)
  - `--out`: 출력 디렉토리(없으면 타임스탬프 기반 자동 생성 가능)
  - `--collection-name`: Chroma 컬렉션명(옵션)
  - `--fail-on-empty-gold`: gold_ids 누락 샘플을 에러로 처리할지(옵션)

## 출력

- `per_sample.jsonl`: 샘플별 검색 결과 및 메트릭
- `summary.json`: 집계 메트릭
- `report.csv`, `report.md`: 사람이 읽기 좋은 리포트

## 의존성/가정

- 검색 구현은 문서 [`docs/retrieval/search.md`](../retrieval/search.md)의 `VectorSearch.search()` 반환 형식을 따른다고 가정합니다.


