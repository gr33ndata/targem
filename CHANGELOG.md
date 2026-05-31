# Changelog

## 2026-05-31

### Added glossary-aware prompt injection

- Introduced a separate glossary layer in `corpus/Targem.glossary.yaml` for preferred lexical choices such as `passport -> باسبور` and `calendar -> أجندة`.
- Added `src/targem/glossary.py` to load glossary entries and match only the relevant ones against the current English input.
- Kept glossary injection separate from few-shot retrieval so sentence examples continue to teach style, while glossary entries enforce lexical consistency.
- Added lightweight English morphology handling so entries can still match simple inflections such as `recommend`, `recommended`, `recommending`, and plurals like `books`.
- Wired the glossary into the CLI and debug prompt flow, including a `--glossary` option and visibility into matched entries during `--debug-prompt`.

Why this matters:

- Before this change, Targem had only sentence-level few-shot control. That helped with register, but it was weak at consistently preferring specific Egyptian lexical choices.
- After this change, Targem can inject only the vocabulary that matters for the current sentence, which improves consistency without wasting prompt space on irrelevant terms.

### Added conditional numeral hinting

- Updated prompt construction so if the English source contains digits, the prompt adds an explicit reminder to prefer Eastern Arabic numerals like `١٢٣`.
- Kept this conditional instead of global in the user block, so the prompt stays cleaner when numbers are not present.

Why this matters:

- The style policy already preferred Eastern Arabic numerals, but the model benefits from a stronger local reminder exactly when numeric fidelity matters.
- This reduces drift back to `123` in otherwise Egyptian output.

### Added Obsidian wikilink handling

- Updated prompt construction so when the input contains Obsidian wikilinks like `[[target|label]]`, the prompt adds a markup-preservation rule.
- The rule tells the model to preserve the wikilink syntax exactly, keep the `target` side unchanged, and translate only the `label`.
- For proper names in link labels, the rule tells the model to transliterate rather than translate.
- Added corpus examples for both a normal translated label and a proper-name label:
  - `[[theInternet|The Internet]] -> [[theInternet|الإنترنت]]`
  - `[[NaguibMahfouz|Naguib Mahfouz]] -> [[NaguibMahfouz|نجيب محفوظ]]`

Why this matters:

- Wikilinks are structured markup, not just text style. Few-shot examples alone are not reliable enough to preserve the syntax and semantics consistently.
- This keeps Obsidian links usable after translation instead of corrupting the `target` side or translating the wrong segment.

### Expanded corpus coverage

- Added new English -> Egyptian Arabic pairs covering:
  - short conversational phrases
  - explanatory and reflective sentences
  - Dutch politics/government examples
  - simple question forms
  - wikilink examples
- Avoided duplicate English entries where male/female Arabic variants would have reduced retrieval diversity.

Why this matters:

- The corpus now covers more of the register Targem is actually meant to translate, while preserving better few-shot variety.

