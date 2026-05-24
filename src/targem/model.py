"""Model API wrappers for Targem."""

import os

import anthropic

CLAUDE_DEFAULT = "claude-sonnet-4-6"
OPENAI_DEFAULT = "gpt-4o"
MAX_TOKENS = 1024


def translate_with_claude(
    messages: list[dict],
    api_key: str | None = None,
    model: str = CLAUDE_DEFAULT,
) -> str:
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=key)
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        messages=messages,
    )
    return response.content[0].text.strip()


def translate_with_openai(
    messages: list[dict],
    api_key: str | None = None,
    model: str = OPENAI_DEFAULT,
) -> str:
    try:
        import openai as _openai
    except ImportError as e:
        raise ImportError("Install the openai extra: pip install 'targem[openai]'") from e

    key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY")
    org = os.environ.get("OPENAI_ORG")
    client = _openai.OpenAI(api_key=key, organization=org)
    response = client.chat.completions.create(
        model=model,
        max_tokens=MAX_TOKENS,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def translate_with_model(
    messages: list[dict],
    provider: str = "claude",
    model: str | None = None,
    api_key: str | None = None,
) -> str:
    if provider == "claude":
        return translate_with_claude(messages, api_key=api_key, model=model or CLAUDE_DEFAULT)
    elif provider == "openai":
        return translate_with_openai(messages, api_key=api_key, model=model or OPENAI_DEFAULT)
    else:
        raise ValueError(f"Unknown provider '{provider}'. Choose 'claude' or 'openai'.")
