"""Glossary loading and lightweight lexical matching for Targem."""

from dataclasses import dataclass
from pathlib import Path
import re

import yaml


WORD_RE = re.compile(r"[a-z0-9']+")


@dataclass
class GlossaryEntry:
    source: str
    target: str
    variants: list[str]
    kind: str = "lexical"
    priority: int = 0


def load_glossary(path: Path) -> list[GlossaryEntry]:
    """Load glossary entries from a Targem YAML glossary file."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entries = []
    for item in data.get("entries", []):
        source = item["source"].strip()
        target = item["target"].strip()
        variants = [v.strip() for v in item.get("variants", []) if v.strip()]
        kind = item.get("kind", "lexical").strip()
        priority = int(item.get("priority", 0))
        entries.append(
            GlossaryEntry(
                source=source,
                target=target,
                variants=variants,
                kind=kind,
                priority=priority,
            )
        )
    return entries


def _normalize_text(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def _token_forms(token: str) -> set[str]:
    forms = {token}

    if len(token) > 4 and token.endswith("ies"):
        forms.add(token[:-3] + "y")

    if len(token) > 3 and token.endswith("es"):
        forms.add(token[:-2])

    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        forms.add(token[:-1])

    if len(token) > 4 and token.endswith("ing"):
        base = token[:-3]
        forms.add(base)
        if len(base) > 2 and base[-1:] == base[-2:-1]:
            forms.add(base[:-1])
        if base and not base.endswith("e"):
            forms.add(base + "e")

    if len(token) > 3 and token.endswith("ed"):
        base = token[:-2]
        forms.add(base)
        if base and not base.endswith("e"):
            forms.add(base + "e")

    if len(token) > 2 and token.endswith("'s"):
        forms.add(token[:-2])

    return {form for form in forms if form}


def _phrase_matches(phrase: str, query: str) -> bool:
    phrase_tokens = _normalize_text(phrase)
    query_tokens = _normalize_text(query)

    if not phrase_tokens or not query_tokens or len(phrase_tokens) > len(query_tokens):
        return False

    query_forms = [_token_forms(token) for token in query_tokens]
    width = len(phrase_tokens)
    for start in range(len(query_tokens) - width + 1):
        if all(phrase_tokens[offset] in query_forms[start + offset] for offset in range(width)):
            return True
    return False


def match_glossary(
    query: str,
    entries: list[GlossaryEntry],
    max_matches: int = 5,
) -> list[GlossaryEntry]:
    """Return glossary entries relevant to the current query.

    Matching is phrase-based over the English input with lightweight inflection
    handling for plural and common verb forms.
    """
    matched = []
    seen = set()

    for entry in entries:
        forms = [entry.source, *entry.variants]
        if any(_phrase_matches(form, query) for form in forms):
            key = (entry.source.lower(), entry.target)
            if key in seen:
                continue
            seen.add(key)
            matched.append(entry)

    matched.sort(
        key=lambda entry: (
            -entry.priority,
            -max(len(_normalize_text(form)) for form in [entry.source, *entry.variants]),
            entry.source.lower(),
        )
    )
    return matched[:max_matches]
