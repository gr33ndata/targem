# Tarjim

Public code-and-corpus repository for Tarjim.

Tarjim is a Python project for translating English writing into educated spoken Egyptian Arabic with better control over:

- dialect fidelity
- register
- anti-MSA drift
- corpus-driven few-shot behavior

## Scope

This repo contains only the publishable software layer and product assets that should live with it:

- Python package scaffold
- tests scaffold
- committed translation corpus

It intentionally does **not** contain private workspace documents such as the PRD or vault-native project notes.

## Layout

- `corpus/` — committed bilingual corpus assets
- `src/tarjim/` — package code
- `tests/` — automated tests
- `pyproject.toml` — package metadata

## Git Model

This folder is the repository boundary.

Inside the larger vault, the right long-term relationship is:

- parent vault project folder outside
- this `public/` folder as the separately versioned repo

If the parent vault ever tracks the public repo formally, the right model is **submodule**, not **subtree**, because this repo should own its own history and remote.
