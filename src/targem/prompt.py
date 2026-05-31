"""Prompt construction for Targem."""

import re

from targem.corpus import CorpusPair
from targem.glossary import GlossaryEntry
from targem.style_policy import STYLE_RULES, SYSTEM_HEADER


def build_messages(
    query: str,
    examples: list[CorpusPair],
    glossary_entries: list[GlossaryEntry] | None = None,
) -> list[dict]:
    """Build Claude messages for a translation request with few-shot exemplars."""
    system_content = f"{SYSTEM_HEADER}\n\n{STYLE_RULES}"

    example_lines = []
    for pair in examples:
        example_lines.append(f"English: {pair.english}")
        example_lines.append(f"Egyptian Arabic: {pair.egyptian_arabic}")
        example_lines.append("")

    examples_block = "\n".join(example_lines).strip()
    glossary_block = ""
    if glossary_entries:
        glossary_lines = ["Preferred vocabulary (use only when relevant):"]
        for entry in glossary_entries:
            glossary_lines.append(f"- {entry.source} -> {entry.target}")
        glossary_block = "\n".join(glossary_lines)

    numerals_block = ""
    if re.search(r"\d", query):
        numerals_block = "Numerals: if the source contains numbers, prefer Eastern Arabic numerals like ١٢٣."

    wikilink_block = ""
    if "[[" in query and "]]" in query:
        wikilink_block = (
            "Wikilinks: preserve Obsidian wikilink markup exactly. In [[target|label]], keep the target "
            "part exactly as written and only translate the label part. If the label is a proper name, "
            "transliterate it instead of translating it."
        )

    parts = [
        part
        for part in [
            examples_block,
            glossary_block,
            numerals_block,
            wikilink_block,
            f"English: {query}\nEgyptian Arabic:",
        ]
        if part
    ]
    user_content = "\n\n".join(parts)

    return [
        {"role": "user", "content": f"{system_content}\n\n{user_content}"},
    ]
