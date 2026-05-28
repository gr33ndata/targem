import os

import pytest
from click import UsageError

from targem.cli import resolve_provider


def test_resolve_provider_auto_prefers_anthropic(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-test")
    monkeypatch.setenv("OPENAI_KEY", "openai-test")

    assert resolve_provider("auto") == "claude"


def test_resolve_provider_auto_uses_openai_when_only_openai_is_set(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_KEY", "openai-test")

    assert resolve_provider("auto") == "openai"


def test_resolve_provider_preserves_explicit_choice(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_KEY", raising=False)

    assert resolve_provider("openai") == "openai"


def test_resolve_provider_auto_requires_any_configured_provider(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_KEY", raising=False)

    with pytest.raises(UsageError):
        resolve_provider("auto")
