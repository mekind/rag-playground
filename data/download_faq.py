"""Download Mental Health FAQ dataset from Kaggle."""

import os
import json
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
import logging

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_kaggle_api():
    """Setup Kaggle API credentials."""
    # Use .data folder in project root instead of ~/.kaggle
    project_root = Path(__file__).parent.parent
    kaggle_dir = project_root / ".data"
    kaggle_dir.mkdir(exist_ok=True)

    kaggle_json = kaggle_dir / "kaggle.json"

    if not kaggle_json.exists():
        if Config.KAGGLE_USERNAME and Config.KAGGLE_KEY:
            # Create kaggle.json from environment variables
            kaggle_credentials = {
                "username": Config.KAGGLE_USERNAME,
                "key": Config.KAGGLE_KEY,
            }
            with open(kaggle_json, "w") as f:
                json.dump(kaggle_credentials, f)
            os.chmod(kaggle_json, 0o600)
            logger.info("Created kaggle.json from environment variables")
        else:
            raise ValueError(
                "Kaggle credentials not found. "
                "Please set KAGGLE_USERNAME and KAGGLE_KEY in .env file, "
                f"or place kaggle.json in {kaggle_dir}/"
            )

    # Set KAGGLE_CONFIG_DIR environment variable to use custom path
    os.environ["KAGGLE_CONFIG_DIR"] = str(kaggle_dir)
    
    api = KaggleApi()
    api.authenticate()
    return api


def download_dataset():
    """Download Mental Health FAQ dataset from Kaggle."""
    # Create data directories
    raw_data_dir = Path(Config.RAW_DATA_DIR)
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Setting up Kaggle API...")
    api = setup_kaggle_api()

    # Dataset identifier (you may need to update this based on actual Kaggle dataset)
    dataset = "narendrageek/mental-health-faq-for-chatbot"

    logger.info(f"Downloading dataset: {dataset}")
    logger.info(f"Destination: {raw_data_dir}")

    try:
        api.dataset_download_files(dataset, path=str(raw_data_dir), unzip=True)
        logger.info("Dataset downloaded successfully!")
        return raw_data_dir
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        logger.info(
            "Note: You may need to manually download the dataset from Kaggle "
            "and place it in the data/raw/ directory"
        )
        raise


if __name__ == "__main__":
    download_dataset()
