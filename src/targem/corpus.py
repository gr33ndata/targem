"""Corpus loading for Targem."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class CorpusPair:
    english: str
    egyptian_arabic: str


def load_corpus(path: Path) -> list[CorpusPair]:
    """Load translation pairs from a Targem YAML corpus file."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    pairs = []
    for item in data.get("pairs", []):
        english = item["english"].strip()
        arabic = item["egyptian_arabic"].strip()
        pairs.append(CorpusPair(english=english, egyptian_arabic=arabic))
    return pairs
