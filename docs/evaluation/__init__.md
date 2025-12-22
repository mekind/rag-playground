# evaluation 패키지 문서

## 목적/책임

`evaluation/`은 RAG 시스템의 **오프라인 평가(특히 retrieval 품질 평가)**를 수행하기 위한 모듈 모음입니다. 본 패키지는 사용자 질문셋과 사용자가 라벨링한 정답 문서 ID(`gold_ids`)를 기반으로 검색 결과를 채점하고, 결과 아티팩트와 요약 리포트를 생성하며, `pytest`를 통해 회귀(품질 하락) 여부를 검증할 수 있도록 합니다.

## 주요 컴포넌트

- `evaluation.retrieval_dataset`
  - JSONL 평가셋 로딩/검증
- `evaluation.retrieval_metrics`
  - Hit@k, Recall@k, Precision@k, MRR@k, nDCG@k 계산
- `evaluation.retrieval_runner`
  - `retrieval.search.VectorSearch`를 호출하여 검색을 수행하고, per-sample 결과/집계 결과를 생성
- `evaluation.retrieval_report`
  - CSV/Markdown 리포트 생성
- `evaluation.cli`
  - 커맨드라인에서 평가 실행

## 입력/출력(요약)

- 입력: `data/eval/*.jsonl` 형태의 평가셋
- 출력: `runs/eval_.../` 아래에 결과 JSONL 및 요약 리포트(CSV/MD)

## 의존성/가정

- retrieval 검색 API는 문서 [`docs/retrieval/search.md`](../retrieval/search.md)를 따릅니다.
- Chroma DB/컬렉션이 준비되어 있어야 실제 검색 평가가 가능합니다.


