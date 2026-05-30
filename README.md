# Targem

Ask an AI to translate something into Egyptian Arabic and you'll usually get one of two results: 
- Formal Fus'ha (or MSA) that no one actually speaks, 
- Or an over-corrected street dialect with inconsistent spelling that reads like a caricature. 

The middle ground — the educated, natural spoken Arabic spoken by well educated Egyptians   — rarely survives the translation.

**Targem solves this by steering the model with examples, i.e. Few-shot learning (FSL).** 

Before each translation, it retrieves the most relevant sentence pairs from a curated bilingual corpus and feeds them to the model as few-shot demonstrations. The model learns your register from the examples, not just from instructions, which keeps the output consistent and grounded.

This README translated into Egyptian Arabic using Targem: [README_ARZ.md](README_ARZ.md)

## Why Targem Helps

A plain prompt like `Translate this to Egyptian Arabic` often gets you Arabic that is understandable but still drifts toward `MSA`.

Example input:

```text
The Dutch department store that sells everything — and somehow feels like home
```

Typical vanilla LLM output:

```text
المتجر الهولندي الذي يبيع كل شيء ويمنحك بطريقة ما شعور المنزل
```

Targem-style output:

```text
المحل الهولندي اللي بيبيع كل حاجة وبيحسسك إنك في بيتك
```

Why the second one is better:

- `اللي` instead of `الذي`
- `كل حاجة` instead of `كل شيء`
- `بيحسسك` instead of the stiffer `يمنحك شعور`
- overall rhythm sounds like educated spoken Egyptian, not cleaned-up formal Arabic

That difference is the whole point of `targem`: not just translating the meaning, but pulling the register toward the Egyptian Arabic you actually want.

## Installation

Recommended: install with `uv` in editable mode from the repo root. That makes the `targem` command available anywhere on your machine while still reflecting local code changes. The default install includes both Claude and OpenAI support.

```bash
# after cloning the repo
cd /path/to/targem
uv tool install --editable .
```

If `uv`'s bin directory is not already on your `PATH`, add it once:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Useful maintenance commands:

```bash
# reinstall / refresh after dependency or metadata changes
uv tool install --editable --reinstall .

# remove the global command
uv tool uninstall targem
```

You can also run it without a global install from the repo root:

```bash
uv run targem "Life is a terminal disease."
```

Environment loading behavior:

- `targem` first respects existing environment variables
- then loads `~/.targem`
- provider defaults to `auto`
- `auto` prefers Claude if both providers are configured; otherwise it uses whichever provider key is present
- supported keys:
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`

## Usage

```bash
# translate a string
targem "Life is a terminal disease."

# translate a file
targem --in essay.txt

# pipe input
cat article.txt | targem

# write translation directly to a file
targem "Some text." --out translation.txt

# file-to-file translation
targem --in article.txt --out translation.txt

# show which corpus examples were used
targem "Some text." --show-examples

# print retrieved exemplars and full prompt
targem "Some text." --debug-prompt

# control how many examples to retrieve (default 5)
targem "Some text." --k 3

# let targem infer provider from your keys
targem "Some text."

# use OpenAI instead of Claude
targem "Some text." --provider openai

# override the model
targem "Some text." --provider openai --model gpt-4-turbo

# run provider/network/model diagnostics
targem --doctor --provider openai
```

Recommended setup: fill in the repo template file `.targem`, then copy it to your home directory as `~/.targem`.

```bash
cp .targem ~/.targem
```

Example `~/.targem`:

```env
ANTHROPIC_API_KEY=...   # for --provider claude or auto
OPENAI_API_KEY=...      # for --provider openai or auto
```

Resolution order:

1. existing environment variables
2. `~/.targem`

That keeps credentials out of the repo and makes `targem` work from any folder on the machine.

Supported keys:

```env
ANTHROPIC_API_KEY=...   # for --provider claude or auto
OPENAI_API_KEY=...      # for --provider openai or auto
```

## Layout

- `corpus/` — committed bilingual corpus assets
- `src/targem/` — package code
- `tests/` — automated tests
- `pyproject.toml` — package metadata

## Development Notes

- The editable install points at this working tree, so changes under `src/targem/` are reflected the next time you run `targem`.
- If you change dependencies, entry points, or package metadata in `pyproject.toml`, run `uv tool install --editable --reinstall .` again.

## Doctor

Use `--doctor` when you want diagnostics without mixing them into translation workflows.

Checks include:

- provider selected
- key present
- package installed
- DNS works
- HTTPS connection works
- model call works

Example:

```bash
targem --doctor --provider openai
```
