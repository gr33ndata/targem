"""Model API wrappers for Targem."""

import os
import sys

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
    if not key:
        print("targem: no ANTHROPIC_API_KEY found in environment or .env", file=sys.stderr)
    try:
        client = anthropic.Anthropic(api_key=key)
        response = client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=messages,
        )
        return response.content[0].text.strip()
    except anthropic.AuthenticationError as e:
        raise SystemExit(f"targem: Anthropic authentication failed — check your ANTHROPIC_API_KEY\n  {e}") from None
    except anthropic.RateLimitError as e:
        raise SystemExit(f"targem: Anthropic rate limit or quota exceeded\n  {e}") from None
    except anthropic.APIError as e:
        raise SystemExit(f"targem: Anthropic API error ({type(e).__name__})\n  {e}") from None


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
    if not key:
        print("targem: no OPENAI_API_KEY or OPENAI_KEY found in environment or .env", file=sys.stderr)
    try:
        client = _openai.OpenAI(api_key=key, organization=org)
        response = client.chat.completions.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except _openai.AuthenticationError as e:
        raise SystemExit(f"targem: OpenAI authentication failed — check your OPENAI_KEY\n  {e}") from None
    except _openai.RateLimitError as e:
        raise SystemExit(f"targem: OpenAI rate limit or quota exceeded\n  details: {e.body}") from None
    except _openai.APIError as e:
        raise SystemExit(f"targem: OpenAI API error ({type(e).__name__})\n  {e}") from None


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
