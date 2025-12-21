"""Preprocess Mental Health FAQ dataset into Q-A pairs."""

import json
import pandas as pd
from pathlib import Path
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_raw_data(raw_data_dir):
    """Load raw dataset files."""
    raw_data_path = Path(raw_data_dir)

    # Try to find CSV or JSON files
    csv_files = list(raw_data_path.glob("*.csv"))
    json_files = list(raw_data_path.glob("*.json"))

    if csv_files:
        logger.info(f"Found CSV file: {csv_files[0]}")
        return pd.read_csv(csv_files[0])
    elif json_files:
        logger.info(f"Found JSON file: {json_files[0]}")
        with open(json_files[0], "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(
            f"No CSV or JSON files found in {raw_data_dir}. "
            "Please ensure the dataset is downloaded."
        )


def preprocess_faq_data(raw_data):
    """Convert raw data into standardized Q-A pairs."""
    processed_data = []

    if isinstance(raw_data, pd.DataFrame):
        # Handle CSV format
        # Common column names for FAQ datasets
        question_col = None
        answer_col = None

        for col in raw_data.columns:
            col_lower = col.lower()
            if "question" in col_lower or "q" == col_lower:
                question_col = col
            elif "answer" in col_lower or "a" == col_lower or "response" in col_lower:
                answer_col = col

        if question_col and answer_col:
            for _, row in raw_data.iterrows():
                question = str(row[question_col]).strip()
                answer = str(row[answer_col]).strip()

                if question and answer and question != "nan" and answer != "nan":
                    processed_data.append(
                        {
                            "id": len(processed_data),
                            "question": question,
                            "answer": answer,
                            "text": f"Q: {question}\nA: {answer}",  # Combined text for embedding
                        }
                    )
        else:
            logger.warning(
                "Could not find question/answer columns. Using first two columns."
            )
            for idx, row in raw_data.iterrows():
                if len(row) >= 2:
                    processed_data.append(
                        {
                            "id": idx,
                            "question": str(row.iloc[0]).strip(),
                            "answer": str(row.iloc[1]).strip(),
                            "text": f"Q: {row.iloc[0]}\nA: {row.iloc[1]}",
                        }
                    )

    elif isinstance(raw_data, (list, dict)):
        # Handle JSON format
        if isinstance(raw_data, dict):
            raw_data = [raw_data]

        for idx, item in enumerate(raw_data):
            if isinstance(item, dict):
                # Try to extract question and answer with various key names
                # Mental Health FAQ dataset uses "Questions" and "Answers" (plural)
                question = (
                    item.get("Questions")
                    or item.get("Question")
                    or item.get("question")
                    or item.get("q")
                )
                answer = (
                    item.get("Answers")
                    or item.get("Answer")
                    or item.get("answer")
                    or item.get("a")
                    or item.get("response")
                )
                # Use Question_ID if available, otherwise use index
                question_id = item.get("Question_ID") or str(idx)

                if question and answer:
                    processed_data.append(
                        {
                            "id": question_id,
                            "question": str(question).strip(),
                            "answer": str(answer).strip(),
                            "text": f"Q: {question}\nA: {answer}",
                        }
                    )

    logger.info(f"Processed {len(processed_data)} FAQ entries")
    return processed_data


def save_processed_data(processed_data, output_path):
    """Save processed data to JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved processed data to {output_path}")


def main():
    """Main preprocessing pipeline."""
    raw_data_dir = Config.RAW_DATA_DIR
    processed_data_dir = Path(Config.PROCESSED_DATA_DIR)
    processed_data_dir.mkdir(parents=True, exist_ok=True)

    output_file = processed_data_dir / "faq_processed.json"

    logger.info("Loading raw data...")
    raw_data = load_raw_data(raw_data_dir)

    logger.info("Preprocessing data...")
    processed_data = preprocess_faq_data(raw_data)

    logger.info(f"Saving processed data to {output_file}...")
    save_processed_data(processed_data, output_file)

    logger.info("Preprocessing complete!")
    return processed_data


if __name__ == "__main__":
    main()
