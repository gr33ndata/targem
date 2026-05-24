# Tarjim

Python software project for translating English opinion / newsletter writing into educated spoken Egyptian Arabic.

The product thesis is simple:

- existing models are good enough at adequacy
- they are not good enough at Egyptian naturalness, register control, and anti-MSA drift
- the real asset is the corpus, style policy, retrieval strategy, and evaluation harness

## Current Scope

This repo is intentionally scaffolded before implementation.

Included now:

- product docs
- corpus storage
- Python project layout
- test folder
- Git repo boundary

Not included yet:

- model-calling code
- retrieval code
- evaluation code
- CLI or API surface

## Layout

- `PRD.md` — product requirements and staged plan
- `Tarjim.md` — original project thesis / working concept note
- `corpus/` — hand-curated bilingual assets committed with the repo
- `src/tarjim/` — future package code
- `tests/` — future automated tests
- `pyproject.toml` — Python package metadata

## Git Boundary

This project should be treated as its own repo.

If it is linked back into the larger PKM vault later, the right model is **submodule**, not **subtree**:

- `submodule` fits because Tarjim should own its own history, releases, and GitHub remote
- `subtree` is for copying another repo into this repo, which is not the shape here

For now, the practical setup is:

- Tarjim is initialized as its own Git repo
- the parent vault should ignore this folder

## Corpus

The corpus is part of the software asset, not an external afterthought.

Current corpus location:

- `corpus/Tarjim.corpus.yaml`
