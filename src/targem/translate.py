"""Core translation pipeline for Targem."""

from pathlib import Path

from targem.corpus import CorpusPair, load_corpus
from targem.glossary import load_glossary, match_glossary
from targem.model import translate_with_model
from targem.prompt import build_messages
from targem.retrieval import TFIDFRetriever


def translate(
    text: str,
    corpus_path: Path,
    glossary_path: Path | None = None,
    k: int = 5,
    api_key: str | None = None,
    provider: str = "claude",
    model: str | None = None,
) -> tuple[str, list[CorpusPair]]:
    """Translate English text to educated spoken Egyptian Arabic.

    Returns:
        A tuple of (translated_text, exemplars_used).
    """
    pairs = load_corpus(corpus_path)
    retriever = TFIDFRetriever(pairs)
    exemplars = retriever.retrieve(text, k=k)
    glossary_entries = load_glossary(glossary_path) if glossary_path and glossary_path.exists() else []
    matched_glossary = match_glossary(text, glossary_entries)
    messages = build_messages(text, exemplars, glossary_entries=matched_glossary)
    translation = translate_with_model(messages, provider=provider, model=model, api_key=api_key)
    return translation, exemplars
