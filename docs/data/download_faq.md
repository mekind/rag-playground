# data/download_faq.py Documentation

## Purpose and Responsibility

The `download_faq.py` module handles downloading the Mental Health FAQ dataset from Kaggle. It manages Kaggle API authentication and downloads the dataset files to the local `data/raw/` directory. This module is responsible for the initial data acquisition step of the RAG pipeline.

## Main Components

### Function: `setup_kaggle_api()`

Sets up and authenticates the Kaggle API client.

**Returns:**
- `KaggleApi`: Authenticated Kaggle API client instance

**Behavior:**
- Creates `~/.kaggle/` directory if it doesn't exist
- Checks for existing `kaggle.json` credentials file
- If not found, creates it from environment variables (KAGGLE_USERNAME, KAGGLE_KEY)
- Authenticates the API client
- Raises ValueError if credentials are not available

### Function: `download_dataset()`

Downloads the Mental Health FAQ dataset from Kaggle.

**Returns:**
- `Path`: Path to the directory containing downloaded data files

**Behavior:**
- Creates `data/raw/` directory structure
- Authenticates with Kaggle API
- Downloads the specified dataset (thedatascientist/mental-health-faq-for-chatbot)
- Unzips the downloaded files
- Returns the path to downloaded data
- Logs progress and errors

## Dependencies

- `kaggle`: Kaggle API client library
- `pathlib.Path`: For path manipulation
- `config.Config`: For accessing configuration values
- `logging`: For progress and error logging

## Assumptions

- Kaggle credentials are available either via:
  - Existing `~/.kaggle/kaggle.json` file, or
  - Environment variables KAGGLE_USERNAME and KAGGLE_KEY
- The dataset identifier is correct and accessible
- Sufficient disk space is available for the dataset
