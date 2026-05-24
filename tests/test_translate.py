"""Integration tests for the translate pipeline (model call mocked)."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from targem.translate import translate

CORPUS_PATH = Path(__file__).parent.parent / "corpus" / "Targem.corpus.yaml"
MOCK_TRANSLATION = "ده ترجمة تجريبية بالمصري."


def _mock_translate_with_model(messages, provider="claude", model=None, api_key=None, **kwargs):
    return MOCK_TRANSLATION


def test_translate_returns_string():
    with patch("targem.translate.translate_with_model", side_effect=_mock_translate_with_model):
        result, _ = translate("Hello world.", corpus_path=CORPUS_PATH)
    assert isinstance(result, str)
    assert len(result) > 0


def test_translate_returns_exemplars():
    with patch("targem.translate.translate_with_model", side_effect=_mock_translate_with_model):
        _, exemplars = translate("Hello world.", corpus_path=CORPUS_PATH, k=3)
    assert len(exemplars) == 3


def test_translate_k_controls_exemplar_count():
    with patch("targem.translate.translate_with_model", side_effect=_mock_translate_with_model):
        _, exemplars = translate("Hello world.", corpus_path=CORPUS_PATH, k=2)
    assert len(exemplars) == 2


def test_translate_uses_mock_translation():
    with patch("targem.translate.translate_with_model", side_effect=_mock_translate_with_model):
        result, _ = translate("Some English text.", corpus_path=CORPUS_PATH)
    assert result == MOCK_TRANSLATION


def test_translate_passes_messages_to_model():
    captured = {}

    def capture(messages, **kwargs):
        captured["messages"] = messages
        return MOCK_TRANSLATION

    with patch("targem.translate.translate_with_model", side_effect=capture):
        translate("Test sentence.", corpus_path=CORPUS_PATH, k=2)

    assert "messages" in captured
    assert len(captured["messages"]) == 1
    assert "Egyptian Arabic" in captured["messages"][0]["content"]


def test_translate_passes_provider_to_model():
    captured = {}

    def capture(messages, provider="claude", **kwargs):
        captured["provider"] = provider
        return MOCK_TRANSLATION

    with patch("targem.translate.translate_with_model", side_effect=capture):
        translate("Test sentence.", corpus_path=CORPUS_PATH, provider="openai")

    assert captured.get("provider") == "openai"
