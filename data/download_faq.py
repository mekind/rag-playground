"""Download Mental Health FAQ dataset from Kaggle."""

import os
import sys
import csv
import json
from pathlib import Path
import logging

from kaggle.api.kaggle_api_extended import KaggleApi

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_kaggle_api():
    """Setup and authenticate Kaggle API client."""

    _kaggle_json = Path(__file__).parent.parent / ".data" / "kaggle.json"
    if not _kaggle_json.exists():
        raise FileNotFoundError(f"kaggle.json not found at {_kaggle_json}")
    return KaggleApi(str(_kaggle_json))


def csv_to_json(csv_path: Path, json_path: Path) -> Path:
    """Convert CSV file to JSON format.

    Args:
        csv_path: Path to the source CSV file
        json_path: Path to the destination JSON file

    Returns:
        Path to the created JSON file
    """
    data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Converted {csv_path} to {json_path} ({len(data)} records)")
    return json_path


def download_dataset():
    """Download Mental Health FAQ dataset from Kaggle and convert to JSON."""
    # Create data directories
    raw_data_dir = Path(Config.RAW_DATA_DIR)
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Setting up Kaggle API...")
    api = setup_kaggle_api()

    # Dataset identifier
    dataset = "narendrageek/mental-health-faq-for-chatbot"

    logger.info(f"Downloading dataset: {dataset}")
    logger.info(f"Destination: {raw_data_dir}")

    try:
        api.dataset_download_files(dataset, path=str(raw_data_dir), unzip=True)
        logger.info("Dataset downloaded successfully!")

        # Convert CSV to JSON
        csv_file = raw_data_dir / "Mental_Health_FAQ.csv"
        json_file = raw_data_dir / "Mental_Health_FAQ.json"

        if csv_file.exists():
            csv_to_json(csv_file, json_file)
            # Remove the original CSV file
            csv_file.unlink()
            logger.info(f"Removed original CSV file: {csv_file}")
        else:
            logger.warning(f"CSV file not found: {csv_file}")

        return json_file
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        logger.info(
            "Note: You may need to manually download the dataset from Kaggle "
            "and place it in the data/raw/ directory"
        )
        raise e


if __name__ == "__main__":
    download_dataset()
