# data/download_faq.py Documentation

## Purpose and Responsibility

The `download_faq.py` module loads an FAQ-style dataset via Hugging Face Datasets and saves it into the local `data/raw/` directory. This module is responsible for the initial data acquisition step of the pipeline.

## Main Components

### Function: `download_dataset()`

Loads the dataset via Hugging Face Datasets and saves it as JSON under `data/raw/`.

**Returns:**
- `Path`: Path to the saved JSON file (e.g. `data/raw/webfaq_kor.json`)

**Behavior:**
- Creates `data/raw/` directory structure
- Loads the dataset using `datasets.load_dataset("PaDaS-Lab/webfaq", "kor")`
- Writes one JSON array file containing examples (optionally annotated with the split name)
- Returns the path to the JSON file
- Logs progress and errors

**Access note:**
Some datasets require authentication. If access is restricted, login first:
- `huggingface-cli login`

## Dependencies

- `datasets`: Hugging Face Datasets (for `load_dataset`)
- `json`: For writing JSON files (standard library)
- `pathlib.Path`: For path manipulation
- `config.Config`: For accessing configuration values
- `logging`: For progress and error logging

## Assumptions

- The dataset identifier/config is correct and accessible
- Sufficient disk space is available for the dataset

## Important Notes

- `data/preprocess.py` discovers raw data by scanning `data/raw/` for JSON/CSV files. This script therefore saves a JSON file (`*.json`) by default.
