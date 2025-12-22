"""
Retrieval evaluation dataset loader.

문서: docs/evaluation/retrieval_dataset.md
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class RetrievalEvalSample:
    qid: str
    query: str
    gold_ids: tuple[str, ...]
    tags: tuple[str, ...] = ()


def _normalize_str_list(value: object, field_name: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if item is None:
                continue
            out.append(str(item))
        return out
    raise ValueError(f"{field_name} must be a list, got {type(value).__name__}")


def load_retrieval_eval_jsonl(path: str | Path) -> list[RetrievalEvalSample]:
    """
    Load retrieval eval samples from JSONL.

    Required keys per line: query, gold_ids
    Optional keys: qid, tags
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    samples: list[RetrievalEvalSample] = []
    with p.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            raw = line.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {idx + 1}: {e}") from e

            if not isinstance(obj, dict):
                raise ValueError(f"Line {idx + 1} must be a JSON object")

            query = obj.get("query")
            if not isinstance(query, str) or not query.strip():
                raise ValueError(f"Line {idx + 1}: query must be a non-empty string")

            gold_ids_list = _normalize_str_list(obj.get("gold_ids"), "gold_ids")
            if len(gold_ids_list) == 0:
                raise ValueError(f"Line {idx + 1}: gold_ids must be a non-empty list")

            qid = obj.get("qid")
            if qid is None:
                qid = f"line_{idx + 1}"
            else:
                qid = str(qid)

            tags_list = _normalize_str_list(obj.get("tags"), "tags")

            samples.append(
                RetrievalEvalSample(
                    qid=qid,
                    query=query.strip(),
                    gold_ids=tuple(gold_ids_list),
                    tags=tuple(tags_list),
                )
            )

    return samples


def iter_jsonl_lines(path: str | Path) -> Iterable[dict]:
    """
    Utility generator used by runner/report when streaming JSONL.
    """
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            raw = line.strip()
            if not raw:
                continue
            obj = json.loads(raw)
            if not isinstance(obj, dict):
                raise ValueError(f"Line {idx + 1} must be a JSON object")
            yield obj


