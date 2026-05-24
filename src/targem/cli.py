"""CLI entry point for Targem."""

import sys
from pathlib import Path

import click

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from targem.translate import translate

DEFAULT_CORPUS = Path(__file__).parent.parent.parent.parent / "corpus" / "Targem.corpus.yaml"


@click.command()
@click.argument("text", required=False)
@click.option("--file", "-f", "input_file", type=click.Path(exists=True, path_type=Path), help="Read input text from a file.")
@click.option("--corpus", type=click.Path(exists=True, path_type=Path), default=None, help="Path to corpus YAML. Defaults to bundled corpus.")
@click.option("--k", default=5, show_default=True, help="Number of exemplars to retrieve.")
@click.option("--provider", default="claude", show_default=True, type=click.Choice(["claude", "openai"]), help="Model provider.")
@click.option("--model", default=None, help="Model name override (e.g. gpt-4o, claude-opus-4-7).")
@click.option("--show-examples", is_flag=True, help="Print retrieved exemplars after translation.")
@click.option("--verbose", is_flag=True, help="Print exemplars and full prompt before translating.")
def cli(
    text: str | None,
    input_file: Path | None,
    corpus: Path | None,
    k: int,
    provider: str,
    model: str | None,
    show_examples: bool,
    verbose: bool,
) -> None:
    """Targem — translate English to educated spoken Egyptian Arabic."""
    if input_file:
        source = input_file.read_text(encoding="utf-8").strip()
    elif text:
        source = text
    elif not sys.stdin.isatty():
        source = sys.stdin.read().strip()
    else:
        raise click.UsageError("Provide TEXT, --file, or pipe input via stdin.")

    corpus_path = corpus or DEFAULT_CORPUS

    if verbose:
        from targem.corpus import load_corpus
        from targem.prompt import build_messages
        from targem.retrieval import TFIDFRetriever

        pairs = load_corpus(corpus_path)
        retriever = TFIDFRetriever(pairs)
        exemplars = retriever.retrieve(source, k=k)
        messages = build_messages(source, exemplars)
        click.echo("── Retrieved exemplars ──", err=True)
        for ex in exemplars:
            click.echo(f"  EN: {ex.english[:80]}", err=True)
            click.echo(f"  AR: {ex.egyptian_arabic[:80]}", err=True)
        click.echo("── Prompt ──", err=True)
        click.echo(messages[0]["content"], err=True)
        click.echo("── Translation ──", err=True)

    translation, exemplars = translate(source, corpus_path=corpus_path, k=k, provider=provider, model=model)

    click.echo(translation)

    if show_examples and not verbose:
        click.echo("\n── Retrieved exemplars ──", err=True)
        for ex in exemplars:
            click.echo(f"  EN: {ex.english[:80]}", err=True)
            click.echo(f"  AR: {ex.egyptian_arabic[:80]}", err=True)
