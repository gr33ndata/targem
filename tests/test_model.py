import pytest

from targem.model import translate_with_claude, translate_with_openai


def test_translate_with_claude_fails_cleanly_without_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(SystemExit, match="no ANTHROPIC_API_KEY"):
        translate_with_claude(messages=[])


def test_translate_with_openai_fails_cleanly_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(SystemExit, match="no OPENAI_API_KEY"):
        translate_with_openai(messages=[])
