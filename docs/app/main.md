# app/main.py Documentation

## Purpose and Responsibility

The `main.py` module implements the Streamlit web application interface for the RAG Lab system. It provides a user-friendly web UI for interacting with the RAG pipeline, allowing users to enter queries, view retrieval results, and see generated answers. The application supports both RAG mode (retrieval + generation) and retrieval-only mode for comparison.

## Main Components

### Page Configuration

**Function:** `st.set_page_config()`

Configures the Streamlit page with:
- Page title: "RAG Lab - Mental Health FAQ"
- Page icon: 🧠
- Layout: wide

### Session State Initialization

**Components:**
- `search_engine`: VectorSearch instance for retrieval operations
- `rag_pipeline`: RAGPipeline instance for RAG operations

**Behavior:**
- Initializes on first page load
- Stores in session state for persistence across interactions
- Handles initialization errors gracefully
- Stops application if initialization fails

### UI Components

#### Header Section
- Title and description
- Educational disclaimer about medical advice

#### Sidebar Configuration
- **Mode Selection**: Radio button to choose between:
  - "RAG (Retrieval + Generation)": Full RAG pipeline
  - "Retrieval Only": Shows only search results
- **Top-K Slider**: Adjusts number of results (1-10, default from Config)
- **Similarity Threshold Slider**: Adjusts minimum similarity (0.0-1.0, default from Config)

#### Main Content Area
- **Query Input**: Text input field for user questions
- **Search Button**: Triggers search/RAG operation
- **Results Display**: Shows results based on selected mode

#### Results Display (RAG Mode)
- **Generated Answer**: Displays LLM-generated answer
- **Retrieved Context**: Expandable sections showing:
  - Number of retrieved entries
  - Each FAQ entry with similarity score
  - Entry text and metadata

#### Results Display (Retrieval Only Mode)
- **Search Results**: List of retrieved FAQ entries
- Each result shows:
  - Similarity score
  - Full text
  - Question and ID from metadata

#### Footer
- Information about the RAG system
- Technologies used

### User Interaction Flow

1. User enters query in text input
2. User clicks "Search" button or presses Enter
3. Application validates query
4. Based on selected mode:
   - **RAG Mode**: Calls `rag_pipeline.generate_answer()`
   - **Retrieval Only**: Calls `search_engine.search()`
5. Displays results with appropriate formatting
6. Handles errors and displays error messages

## Dependencies

- `streamlit`: Web application framework
- `sys`, `pathlib.Path`: For path manipulation and imports
- `config.Config`: For configuration values
- `retrieval.search.VectorSearch`: For retrieval operations
- `retrieval.rag.RAGPipeline`: For RAG operations

## Assumptions

- Streamlit is installed and accessible
- Search engine and RAG pipeline are properly initialized
- User has valid queries to test
- Configuration values are appropriate for the use case
- Error handling covers common failure scenarios
