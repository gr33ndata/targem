# Tarjim PRD

## Goal

Build a translation tool that turns English text into educated spoken Egyptian Arabic with much better control over:

- dialect fidelity
- register
- orthography policy
- resistance to [[Modern Standard Arabic]] drift

## Why This Exists

Current large language models can often preserve meaning, but they frequently fail on the thing that actually matters for publishing-quality Egyptian output:

- the sentence sounds like generic Arabic, not Egyptian
- the rhythm is off
- the wording is too formal
- the dialect gets blended
- the output is usable but culturally dead

## Initial User

Primary user:

- Tarek, translating English opinion / newsletter / explanatory prose into educated spoken Egyptian Arabic

Likely future users:

- bilingual writers
- translators
- Arabic-language creators
- editorial or media teams with dialect-specific needs

## Product Asset Thesis

The moat is not the wrapper around a frontier model.

The moat is:

- the curated corpus
- the style policy
- the retrieval logic
- the evaluation harness
- the error bank for MSA leakage and wrong-dialect output

## MVP

### Inputs

- source English text
- optional style hint

### Core behavior

- retrieve the most relevant bilingual examples from the corpus
- construct a constrained prompt for educated spoken Egyptian
- generate a candidate translation
- run lightweight checks for obvious MSA leakage or style violations

### Outputs

- translation
- optional warning flags
- optional retrieved exemplars used

## Repo-Phase Scope

This repo phase is about creating the project chassis, not implementation.

Needed before real coding:

- stable corpus location
- Python package shape
- test location
- clear product docs
- independent Git boundary

## Planned Phases

### Phase 0

- corpus curation
- style policy
- eval rubric
- software scaffold

### Phase 1

- simple CLI
- YAML corpus loading
- exemplar retrieval baseline
- model call wrapper
- translation output

### Phase 2

- stronger retrieval
- leakage checks
- eval command
- prompt variants

### Phase 3

- fine-tuning experiments
- contrastive bad-example bank
- benchmark set

## Git Decision

Tarjim should be its own repository.

Why:

- the corpus is part of the product asset
- the software will likely be published to GitHub separately from the vault
- the release cadence and history should belong to the project, not to the PKM vault

Between `subtree` and `submodule`, the more suitable model is **submodule** if the parent vault later wants to reference this repo. A subtree would blur repo ownership and make the parent vault unnecessarily responsible for Tarjim's code history.
