# Targem

Ask an AI to translate something into Egyptian Arabic and you'll usually get one of two results: formal Fus'ha that no one actually speaks, or an over-corrected street dialect with inconsistent spelling that reads like a caricature. The middle ground — the educated, natural spoken Arabic used in essays, newsletters, and everyday conversation — rarely survives the translation.

Targem solves this by steering the model with examples. Before each translation, it retrieves the most relevant sentence pairs from a curated bilingual corpus and feeds them to the model as few-shot demonstrations. The model learns your register from the examples, not just from instructions, which keeps the output consistent and grounded.

## Layout

- `corpus/` — committed bilingual corpus assets
- `src/targem/` — package code
- `tests/` — automated tests
- `pyproject.toml` — package metadata
