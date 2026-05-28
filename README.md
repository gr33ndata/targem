# Targem

Ask an AI to translate something into Egyptian Arabic and you'll usually get one of two results: 
- Formal Fus'ha (or MSA) that no one actually speaks, 
- Or an over-corrected street dialect with inconsistent spelling that reads like a caricature. 

The middle ground — the educated, natural spoken Arabic spoken by well educated Egyptians   — rarely survives the translation.

**Targem solves this by steering the model with examples, i.e. Few-shot learning (FSL).** 

Before each translation, it retrieves the most relevant sentence pairs from a curated bilingual corpus and feeds them to the model as few-shot demonstrations. The model learns your register from the examples, not just from instructions, which keeps the output consistent and grounded.

This README translated into Egyptian Arabic using Targem: [README_ARZ.md](README_ARZ.md)

## Installation

Recommended: install with `uv` in editable mode from the `public/` repo root. That makes the `targem` command available outside this folder while still reflecting code changes you make locally.

```bash
cd Workshop/MyBiz/Products/Tarjim/public
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

- `targem` loads `.env` from the **current working directory** you call it from
- provider defaults to `auto`
- `auto` prefers Claude if both providers are configured; otherwise it uses whichever provider key is present
- supported keys:
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`
  - `OPENAI_KEY`
  - `OPENAI_ORG` (optional)

## Usage

```bash
# translate a string
targem "Life is a terminal disease."

# translate a file
targem --file essay.txt

# pipe input
cat article.txt | targem

# show which corpus examples were used
targem "Some text." --show-examples

# control how many examples to retrieve (default 5)
targem "Some text." --k 3

# let targem infer provider from your keys
targem "Some text."

# use OpenAI instead of Claude
targem "Some text." --provider openai

# override the model
targem "Some text." --provider openai --model gpt-4-turbo
```

API keys are read from a `.env` file in the working directory or from environment variables:

```
ANTHROPIC_API_KEY=...   # for --provider claude or auto
OPENAI_API_KEY=...      # for --provider openai or auto
OPENAI_KEY=...          # alias for OPENAI_API_KEY
OPENAI_ORG=...          # optional OpenAI org ID
```

## Layout

- `corpus/` — committed bilingual corpus assets
- `src/targem/` — package code
- `tests/` — automated tests
- `pyproject.toml` — package metadata

## Development Notes

- The editable install points at this working tree, so changes under `src/targem/` are reflected the next time you run `targem`.
- If you change dependencies, entry points, or package metadata in `pyproject.toml`, run `uv tool install --editable --reinstall .` again.
