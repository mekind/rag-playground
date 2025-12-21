# data/download_faq.py Documentation

## Purpose and Responsibility

The `download_faq.py` module handles downloading the Mental Health FAQ dataset from Kaggle. It manages Kaggle API authentication and downloads the dataset files to the local `data/raw/` directory. This module is responsible for the initial data acquisition step of the RAG pipeline.

## Main Components

### Module-Level Initialization (Import-Time)

Kaggle 라이브러리는 임포트 시점에 자격 증명 파일(`kaggle.json`)을 찾습니다. 따라서 모든 Kaggle 관련 설정은 `KaggleApi`를 임포트하기 **전에** 완료되어야 합니다.

**실행 순서:**

1. 프로젝트 루트를 `sys.path`에 추가 (직접 스크립트 실행 지원)
2. `dotenv`로 환경변수 로드 (`.env` 파일에서 `KAGGLE_USERNAME`, `KAGGLE_KEY` 읽기)
3. 프로젝트 루트의 `.data/` 디렉토리 생성
4. `kaggle.json`이 없으면 환경변수로부터 자동 생성
5. `KAGGLE_CONFIG_DIR` 환경변수를 `.data/` 경로로 설정
6. `KaggleApi` 임포트 수행

**자격 증명 자동 생성:**

```python
if not _kaggle_json.exists():
    _kaggle_username = os.getenv("KAGGLE_USERNAME")
    _kaggle_key = os.getenv("KAGGLE_KEY")
    
    if _kaggle_username and _kaggle_key:
        # kaggle.json 자동 생성
        ...
    else:
        raise ValueError("Kaggle credentials not found...")
```

### Function: `setup_kaggle_api()`

Kaggle API 클라이언트를 인증합니다.

**Returns:**
- `KaggleApi`: Authenticated Kaggle API client instance

**Behavior:**
- 현재 설정된 `KAGGLE_CONFIG_DIR` 경로 로깅
- `KaggleApi` 인스턴스 생성 및 인증
- 인증된 API 클라이언트 반환

### Function: `csv_to_json(csv_path, json_path)`

CSV 파일을 JSON 형식으로 변환합니다.

**Parameters:**
- `csv_path` (`Path`): 원본 CSV 파일 경로
- `json_path` (`Path`): 생성할 JSON 파일 경로

**Returns:**
- `Path`: 생성된 JSON 파일 경로

**Behavior:**
- CSV 파일을 읽어서 각 행을 딕셔너리로 변환
- JSON 파일로 저장 (UTF-8 인코딩, 들여쓰기 적용)
- 변환된 레코드 수를 로깅

### Function: `download_dataset()`

Downloads the Mental Health FAQ dataset from Kaggle and converts to JSON format.

**Returns:**
- `Path`: Path to the downloaded JSON file (`data/raw/Mental_Health_FAQ.json`)

**Behavior:**
- Creates `data/raw/` directory structure
- Authenticates with Kaggle API
- Downloads the specified dataset (narendrageek/mental-health-faq-for-chatbot)
- Unzips the downloaded files
- Converts CSV to JSON format using `csv_to_json()`
- Removes the original CSV file after conversion
- Returns the path to the JSON file
- Logs progress and errors

## Dependencies

- `kaggle`: Kaggle API client library
- `python-dotenv`: For loading environment variables from `.env` file
- `csv`: For reading CSV files (standard library)
- `json`: For writing JSON files (standard library)
- `pathlib.Path`: For path manipulation
- `config.Config`: For accessing configuration values
- `logging`: For progress and error logging

## Assumptions

- Kaggle credentials are available either via:
  - Existing `.data/kaggle.json` file (in project root), or
  - Environment variables `KAGGLE_USERNAME` and `KAGGLE_KEY` in `.env` file
- The dataset identifier is correct and accessible
- Sufficient disk space is available for the dataset

## Important Notes

### 환경변수 설정 및 kaggle.json 생성 순서

Kaggle 라이브러리의 특성상 다음 순서가 **반드시** 지켜져야 합니다:

1. `.env` 파일에서 환경변수 로드
2. `kaggle.json` 파일 생성 (없는 경우)
3. `KAGGLE_CONFIG_DIR` 환경변수 설정
4. `KaggleApi` 임포트

```python
# 올바른 순서
from dotenv import load_dotenv
load_dotenv()  # 1. 환경변수 로드

# 2. kaggle.json 생성 (생략)
# 3. KAGGLE_CONFIG_DIR 설정
os.environ["KAGGLE_CONFIG_DIR"] = str(kaggle_dir)

# 4. 이제 안전하게 임포트
from kaggle.api.kaggle_api_extended import KaggleApi
```

### 자격 증명 설정 방법

**방법 1: `.env` 파일 사용 (권장)**

프로젝트 루트의 `.env` 파일에 다음을 추가:

```
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

**방법 2: `kaggle.json` 직접 생성**

`.data/kaggle.json` 파일을 직접 생성:

```json
{
    "username": "your_kaggle_username",
    "key": "your_kaggle_api_key"
}
```

Kaggle API 키는 [Kaggle Account Settings](https://www.kaggle.com/settings)에서 생성할 수 있습니다.
