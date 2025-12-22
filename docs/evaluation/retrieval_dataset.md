# evaluation/retrieval_dataset.py 문서

## 목적/책임

`retrieval_dataset.py`는 라벨 기반 retrieval 평가를 위한 **평가셋(JSONL)**을 로딩하고 스키마를 검증합니다. 평가셋은 사용자 질문(`query`)과 사용자가 라벨링한 정답 문서 ID 목록(`gold_ids`)을 포함합니다.

## 주요 컴포넌트

### 데이터 구조: `RetrievalEvalSample`

- 목적: 평가 샘플 1개의 표준 표현
- 필드(권장)
  - `qid` (str|None): 샘플 ID(없으면 자동 생성 가능)
  - `query` (str): 사용자 질문
  - `gold_ids` (list[str]): 정답 문서 ID 목록(1개 이상 권장)
  - `tags` (list[str]|None): 선택 태그(도메인/난이도 등)

### 함수: `load_retrieval_eval_jsonl(path)`

- 입력: JSONL 파일 경로
- 출력: `list[RetrievalEvalSample]`
- 동작:
  - JSONL 라인을 순회하며 파싱
  - 필수 키(`query`, `gold_ids`) 검증
  - `gold_ids`는 문자열 리스트로 정규화
  - 비정상 샘플은 기본적으로 예외 발생(또는 runner에서 스킵 정책 적용)

## 평가셋 스키마(예시)

예시 파일: `data/eval/retrieval_eval.example.jsonl`

```json
{"qid":"q001","query":"불안이 심할 때 어떻게 해야 하나요?","gold_ids":["12","58"],"tags":["anxiety"]}
```

## 의존성/가정

- 파일은 UTF-8 JSONL 형식
- `gold_ids`는 검색 결과의 `id`와 비교 가능한 값이어야 함


