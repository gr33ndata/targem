"""Core translation pipeline for Targem."""

from pathlib import Path

from targem.corpus import CorpusPair, load_corpus
from targem.model import translate_with_model
from targem.prompt import build_messages
from targem.retrieval import TFIDFRetriever


def translate(
    text: str,
    corpus_path: Path,
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
    messages = build_messages(text, exemplars)
    translation = translate_with_model(messages, provider=provider, model=model, api_key=api_key)
    return translation, exemplars
