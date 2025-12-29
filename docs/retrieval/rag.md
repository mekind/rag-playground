# retrieval/rag.py Documentation

## Purpose and Responsibility

The `rag.py` module implements the RAG (Retrieval-Augmented Generation) pipeline that combines vector search with LLM-based answer generation. It retrieves relevant FAQ entries and uses them as context for generating grounded answers using OpenAI's chat completion API. This module is the core of the RAG system, orchestrating retrieval and generation.

## Main Components

### Class: `RAGPipeline`

A class that implements the complete RAG pipeline from query to generated answer.

#### Initialization: `__init__(collection_name=None)`

**Parameters:**
- `collection_name` (str | list[str] | None, optional): One collection name or multiple collection names to search.
  - If `None`, defaults to `Config.CHROMA_COLLECTION_NAME`.
  - If a list is provided, retrieval can search across multiple collections (embedding strategies).

**Behavior:**
- Initializes VectorSearch instance for retrieval
- Initializes OpenAI client for generation
- Stores both for use in pipeline

#### Method: `format_context(search_results)`

Formats search results into a context string for the LLM.

**Parameters:**
- `search_results` (list[dict]): List of search result dictionaries

**Returns:**
- `str`: Formatted context string with numbered entries and similarity scores

**Behavior:**
- Iterates through search results
- Formats each result with number, similarity score, and text
- Combines into a single context string
- Returns formatted context

#### Method: `generate_prompt(query, context)`

Generates a prompt for the LLM with retrieved context.

**Parameters:**
- `query` (str): User query
- `context` (str): Formatted context from search results

**Returns:**
- `str`: Complete prompt string for LLM

**Behavior:**
- Constructs a structured prompt with:
  - System instructions for the assistant
  - Retrieved context from FAQ database
  - User question
  - Instructions for answering
- Returns formatted prompt

#### Method: `generate_answer(query, top_k=None, threshold=None, model=None)`

Generates an answer using the complete RAG pipeline.

**Parameters:**
- `query` (str): User query
- `top_k` (int, optional): Number of documents to retrieve
- `threshold` (float, optional): Similarity threshold for retrieval
- `model` (str, optional): LLM model name (defaults to Config.LLM_MODEL)

**Returns:**
- `dict`: Result dictionary containing:
  - `answer` (str): Generated answer text
  - `retrieved_context` (list[dict]): List of retrieved FAQ entries
  - `metadata` (dict): Metadata including:
    - `num_retrieved` (int): Number of retrieved documents
    - `model` (str): Model used for generation
    - `query` (str): Original query
    - `error` (str, optional): Error message if generation failed

**Behavior:**
1. Retrieves relevant documents using VectorSearch
   - In multi-collection setups, the pipeline uses a **merged** retrieval view (e.g. `VectorSearch.search_merged()`) to build a single unified context for the LLM.
2. If no results found, returns error message
3. Formats retrieved context
4. Generates prompt with context and query
5. Calls OpenAI chat completion API
6. Extracts and returns generated answer
7. Handles errors and returns error information
8. Logs each step of the process

## OpenAI 응답 파싱 규약 (중요)

`generate_answer()`는 OpenAI **Chat Completions** 응답에서 최종 답변 텍스트를 추출합니다.
구현 및 디버깅 시 아래 규약을 따릅니다.

### 기본 추출 경로

- 기본적으로 답변 텍스트는 `choices[0].message.content`에서 추출합니다.
- `content`가 `None`일 수 있으므로, `.strip()` 호출 전 **None 방어**가 필요합니다.

### `content`가 비어 있을 수 있는 대표 원인

- **tool 호출 경로**: 모델이 `message.tool_calls`로 응답하는 경우, `message.content`는 빈 문자열/None일 수 있습니다.
- **거절/필터링 경로**: 안전 정책에 의해 `message.refusal`이 채워지고 `content`가 비어 있을 수 있습니다.
- **종료 사유(finish_reason) 영향**: `choices[0].finish_reason`가 `tool_calls`, `content_filter`, `length` 등일 때 콘텐츠가 비거나 기대보다 짧을 수 있습니다.

### 권장 로그 (원인 규명용)

`content`가 비어 있거나 예상과 다를 때 아래 값을 함께 로깅합니다.

- `model`
- `choices[0].finish_reason`
- `choices[0].message.content` (길이/None 여부)
- `choices[0].message.tool_calls` 존재 여부
- `choices[0].message.refusal` 존재 여부

이 로그만 있으면 “왜 content가 비었는지”를 대부분 즉시 구분할 수 있습니다.

**Prompt Structure:**
The prompt instructs the LLM to:
- Answer based on provided context
- Indicate when context is insufficient
- Be concise and helpful
- Synthesize information from multiple entries when needed

## Dependencies

- `openai`: OpenAI API client library
- `config.Config`: For configuration values
- `retrieval.search`: For vector search functionality
- `logging`: For operation logging

## Assumptions

- VectorSearch is properly initialized and connected to indexed collection
- OpenAI API key is configured and valid
- LLM model is available and accessible
- Retrieved context is relevant to the query
- Temperature and max_tokens settings are appropriate for the use case
