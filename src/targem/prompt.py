"""Prompt construction for Targem."""

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

    parts = [part for part in [examples_block, glossary_block, f"English: {query}\nEgyptian Arabic:"] if part]
    user_content = "\n\n".join(parts)

    return [
        {"role": "user", "content": f"{system_content}\n\n{user_content}"},
    ]
