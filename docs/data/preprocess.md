# data/preprocess.py Documentation

## Purpose and Responsibility

The `preprocess.py` module processes raw FAQ dataset files into a standardized JSON format with Q-A pairs. It handles multiple input formats (CSV, JSON) and extracts question-answer pairs, creating a unified structure suitable for embedding and indexing. This module prepares the data for the ingestion pipeline.

## Main Components

### Function: `load_raw_data(raw_data_dir)`

Loads raw dataset files from the specified directory.

**Parameters:**
- `raw_data_dir` (str): Path to directory containing raw data files

**Returns:**
- `pd.DataFrame` or `dict/list`: Raw data in pandas DataFrame (for CSV) or dict/list (for JSON)

**Behavior:**
- Searches for CSV or JSON files in the directory
- Loads CSV files using pandas
- Loads JSON files using json module
- Raises FileNotFoundError if no valid files are found

### Function: `preprocess_faq_data(raw_data)`

Converts raw data into standardized Q-A pairs.

**Parameters:**
- `raw_data`: Raw data (DataFrame, list, or dict)

**Returns:**
- `list[dict]`: List of processed FAQ entries, each containing:
  - `id` (int): Unique identifier
  - `question` (str): Question text
  - `answer` (str): Answer text
  - `text` (str): Combined "Q: {question}\nA: {answer}" format for embedding

**Behavior:**
- Handles pandas DataFrame format:
  - Attempts to identify question/answer columns by name
  - Falls back to using first two columns if not found
- Handles JSON format:
  - Supports both list and single dict formats
  - Extracts question/answer from various key name variations
- Filters out empty or invalid entries
- Creates combined text field for embedding

### Function: `save_processed_data(processed_data, output_path)`

Saves processed data to a JSON file.

**Parameters:**
- `processed_data` (list[dict]): Processed FAQ data
- `output_path` (str): Path to output JSON file

**Behavior:**
- Creates parent directories if needed
- Saves data as formatted JSON with UTF-8 encoding
- Logs the save operation

### Function: `main()`

Main preprocessing pipeline that orchestrates the entire process.

**Returns:**
- `list[dict]`: Processed FAQ data

**Behavior:**
- Loads raw data from `data/raw/`
- Preprocesses into Q-A pairs
- Saves to `data/processed/faq_processed.json`
- Returns processed data

## Dependencies

- `pandas`: For CSV file handling
- `json`: For JSON file operations
- `pathlib.Path`: For path manipulation
- `config.Config`: For accessing data directory paths
- `logging`: For progress logging

## Assumptions

- Raw data files exist in `data/raw/` directory
- Data contains question-answer pairs in some recognizable format
- Column names or keys follow common naming patterns (question, answer, q, a, etc.)
