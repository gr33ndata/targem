"""Tests for glossary loading and matching."""

from pathlib import Path

from targem.glossary import GlossaryEntry, load_glossary, match_glossary

GLOSSARY_PATH = Path(__file__).parent.parent / "corpus" / "Targem.glossary.yaml"


def test_load_glossary_returns_entries():
    entries = load_glossary(GLOSSARY_PATH)
    assert len(entries) > 0
    assert all(isinstance(entry, GlossaryEntry) for entry in entries)


def test_match_glossary_handles_simple_inflection():
    entries = load_glossary(GLOSSARY_PATH)
    matches = match_glossary("Can you recommended a book for me?", entries)
    assert any(entry.source == "recommend" for entry in matches)


def test_match_glossary_handles_plural_matching():
    entries = load_glossary(GLOSSARY_PATH)
    matches = match_glossary("How were the pyramids built?", entries)
    assert any(entry.source == "pyramids" for entry in matches)


def test_match_glossary_only_returns_relevant_entries():
    entries = load_glossary(GLOSSARY_PATH)
    matches = match_glossary("The weather is nice today.", entries)
    assert matches == []


def test_match_glossary_prioritizes_phrase_entry():
    entries = [
        GlossaryEntry(source="book", target="كتاب", variants=[], priority=10),
        GlossaryEntry(source="put down", target="يسيب", variants=[], kind="phrase", priority=50),
    ]
    matches = match_glossary("I could not put down the book.", entries, max_matches=2)
    assert matches[0].source == "put down"
