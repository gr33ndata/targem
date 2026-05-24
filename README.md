# Targem

Ask an AI to translate something into Egyptian Arabic and you'll usually get one of two results: 
- Formal Fus'ha (or MSA) that no one actually speaks, 
- Or an over-corrected street dialect with inconsistent spelling that reads like a caricature. 

The middle ground — the educated, natural spoken Arabic spoken by well educated Egyptians   — rarely survives the translation.

**Targem solves this by steering the model with examples, i.e. Few-shot learning (FSL).** 

Before each translation, it retrieves the most relevant sentence pairs from a curated bilingual corpus and feeds them to the model as few-shot demonstrations. The model learns your register from the examples, not just from instructions, which keeps the output consistent and grounded.

This README translated into Egyptian Arabic using Targem: [README_ARZ.md](README_ARZ.md)

## Layout

- `corpus/` — committed bilingual corpus assets
- `src/targem/` — package code
- `tests/` — automated tests
- `pyproject.toml` — package metadata
