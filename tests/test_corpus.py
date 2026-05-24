"""Tests for corpus loading."""

from pathlib import Path

import pytest

from targem.corpus import CorpusPair, load_corpus

CORPUS_PATH = Path(__file__).parent.parent / "corpus" / "Targem.corpus.yaml"


def test_load_corpus_returns_pairs():
    pairs = load_corpus(CORPUS_PATH)
    assert len(pairs) > 0
    assert all(isinstance(p, CorpusPair) for p in pairs)


def test_corpus_pairs_have_content():
    pairs = load_corpus(CORPUS_PATH)
    for pair in pairs:
        assert pair.english.strip()
        assert pair.egyptian_arabic.strip()


def test_corpus_no_trailing_whitespace():
    pairs = load_corpus(CORPUS_PATH)
    for pair in pairs:
        assert pair.english == pair.english.strip()
        assert pair.egyptian_arabic == pair.egyptian_arabic.strip()


def test_load_corpus_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_corpus(Path("/nonexistent/path.yaml"))
