"""Load and save FAQ-style datasets into data/raw/."""

import json
from pathlib import Path
import logging

from datasets import load_dataset

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_dataset():
    """
    Load the dataset via Hugging Face Datasets and save it to data/raw/ as JSON.

    Note:
      If the dataset requires access, login first (e.g. `huggingface-cli login`).
    """
    raw_data_dir = Path(Config.RAW_DATA_DIR)
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    dataset_id = "PaDaS-Lab/webfaq"
    dataset_config = "kor"
    out_path = raw_data_dir / "webfaq_kor.json"

    logger.info("Loading dataset via Hugging Face Datasets...")
    logger.info("Dataset: %s (%s)", dataset_id, dataset_config)
    ds = load_dataset(dataset_id, dataset_config)

    # Save as a single JSON array so data/preprocess.py can discover and load it.
    logger.info("Saving to: %s", out_path)
    num_rows = 0
    with out_path.open("w", encoding="utf-8") as f:
        f.write("[\n")
        first = True

        # ds is typically a DatasetDict (split -> Dataset). Handle both DatasetDict and Dataset.
        if hasattr(ds, "items"):
            split_items = list(ds.items())  # type: ignore[no-any-return]
        else:
            split_items = [("train", ds)]

        for split_name, split_ds in split_items:
            for row in split_ds:
                obj = dict(row)
                obj["_split"] = split_name

                if not first:
                    f.write(",\n")
                json.dump(obj, f, ensure_ascii=False)
                first = False
                num_rows += 1

        f.write("\n]\n")

    logger.info("Saved %s rows to %s", num_rows, out_path)
    return out_path


if __name__ == "__main__":
    download_dataset()
