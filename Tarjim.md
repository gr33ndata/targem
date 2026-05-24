---
status: exploring
domain: AI / Translation / Arabic NLP
date: 2026-05-17
tags: [mybiz, ai, translation, arabic, dialect, llm]
---

# Tarjim

CLI-first translation system for turning English opinion / newsletter writing into educated spoken Egyptian Arabic, where current LLMs drift into [[Modern Standard Arabic]] or bland pan-Arabic mush.

The real IP is not the wrapper around [[Claude Sonnet]] or [[GPT-4o]]. It is the curated corpus plus the style guide: paired English ↔ educated spoken Egyptian examples in the right register, with explicit spelling and anti-[[Modern Standard Arabic]] rules. Best path looks staged: retrieval-based few-shot first, then [[LoRA]] fine-tuning once the corpus and eval set are real.

## Why this matters

- Native-speaker naturalness is the real gap, not raw translation adequacy.
- Existing models are optimized for [[Modern Standard Arabic]] and generic Arabic, not "how an educated Egyptian would actually say this."
- There is a concrete first use case: translating blog posts and [[Ochtendflits]]-style writing for publication.

## Sharpened thesis from research

- Start with a small, high-quality, human-written parallel corpus in the exact target register.
- Use dynamic few-shot retrieval as the MVP because it is fast, inspectable, and teaches the failure modes.
- Add an orthography / leakage checker early, because standard metrics will miss when outputs slide back into [[Modern Standard Arabic]].
- Fine-tune only after the corpus and eval harness are good enough to tell whether the model truly improved.
- Multi-dialect training may help shared Arabic substrate learning, but the product must still preserve explicitly Egyptian output at inference time.

## MVP

- local JSONL corpus of `30` hand-written English ↔ educated spoken Egyptian pairs
- retrieval of top `3` exemplars
- structured prompt with:
  - target dialect and register
  - spelling conventions
  - forbidden MSA leakage patterns
  - exemplar pairs
- model call to Claude Sonnet or GPT-4o
- output plus a simple leakage report

Current seed corpus file:

- `Workshop/MyBiz/Software/Tarjim/corpus/Tarjim.corpus.yaml`

## Why not jump straight to fine-tuning

- you still need the corpus
- you still need eval
- you still need to know what "good Egyptian" means in operational terms
- a bad fine-tune can make output more rigid without making it more natural

## Research-backed product choices

- Retrieval matters more as the corpus grows; at `30` examples it may not beat simple selection by much, but it becomes strategic later.
- Domain match matters more than generic corpus size.
- Human-translated pairs beat machine-translated / post-edited corpora on idiomaticity.
- BLEU can reward MSA-ish smoothing, so evaluation needs human review and dialect-specific checks.
- Bad-example banks may be useful product assets: contrastive prompting / tuning seems to help models learn what "wrong dialect output" looks like, not only what good output looks like.

## Open questions

- [ ] How much does retrieval beat random selection at the 30-pair MVP stage?
- [ ] Should the first corpus be strictly one register, or should it intentionally mix `TV-intellectual`, `essay`, and `newsletter` styles?
- [ ] Is a wordlist-based MSA leakage checker enough, or do we need a second-pass verifier model?
- [ ] Should the first fine-tune be Egyptian-only, or joint Arabic-dialect training with Egyptian-tagged inference?
- [ ] Is the right first product a private writing tool for Tarek, a translation service, or a reusable dialect-translation engine?

## Related

- [[AI-ML/Study/Arabic Dialect Translation Needs Retrieval, Steerability, and Dialect-Sensitive Evaluation]]
- [[Modern Standard Arabic]]
- [[Egyptian Arabic]]
- [[Dialect Erasure]]
- [[Ochtendflits]]
