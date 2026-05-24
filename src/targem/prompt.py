"""Prompt construction for Targem."""

from targem.corpus import CorpusPair
from targem.style_policy import STYLE_RULES, SYSTEM_HEADER


def build_messages(query: str, examples: list[CorpusPair]) -> list[dict]:
    """Build Claude messages for a translation request with few-shot exemplars."""
    system_content = f"{SYSTEM_HEADER}\n\n{STYLE_RULES}"

    example_lines = []
    for pair in examples:
        example_lines.append(f"English: {pair.english}")
        example_lines.append(f"Egyptian Arabic: {pair.egyptian_arabic}")
        example_lines.append("")

    examples_block = "\n".join(example_lines).strip()
    user_content = f"{examples_block}\n\nEnglish: {query}\nEgyptian Arabic:"

    return [
        {"role": "user", "content": f"{system_content}\n\n{user_content}"},
    ]
