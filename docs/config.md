# config.py Documentation

## Purpose and Responsibility

The `config.py` module manages application configuration for the RAG Lab project. It centralizes all configuration settings, including API keys, model names, database settings, and retrieval parameters. This module serves as the single source of truth for configuration values, loading them from environment variables via the `.env` file.

## Main Components

### Class: `Config`

A class-based configuration manager that provides static access to all application settings.

#### Attributes

- **OPENAI_API_KEY** (str): OpenAI API key for embedding and LLM services
- **EMBEDDING_MODEL** (str): Name of the embedding model to use (default: "text-embedding-ada-002")
- **LLM_MODEL** (str): Name of the LLM model to use (default: "gpt-3.5-turbo")
- **CHROMA_PERSIST_DIRECTORY** (str): Directory path for Chroma database persistence (default: "./chroma_db")
- **CHROMA_COLLECTION_NAME** (str): Name of the Chroma collection (default: "mental_health_faq")
- **TOP_K** (int): Number of top results to retrieve (default: 5)
- **SIMILARITY_THRESHOLD** (float): Minimum similarity score for retrieval (default: 0.7)
- **KAGGLE_USERNAME** (str, optional): Kaggle username for dataset download
- **KAGGLE_KEY** (str, optional): Kaggle API key for dataset download
- **DATA_DIR** (str): Base directory for data files (default: "data")
- **RAW_DATA_DIR** (str): Directory for raw dataset files
- **PROCESSED_DATA_DIR** (str): Directory for processed dataset files

#### Methods

- **validate()** (classmethod): Validates that required configuration (OPENAI_API_KEY) is present. Raises ValueError if missing.

## Dependencies

- `os`: For accessing environment variables
- `dotenv`: For loading environment variables from `.env` file

## Assumptions

- A `.env` file exists in the project root with required environment variables
- Environment variables use the naming convention shown in `.env.example`
- Default values are provided for non-critical configuration options
