"""CLI entry point for Targem."""

import importlib.util
import os
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path

import click

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from targem.model import CLAUDE_DEFAULT, OPENAI_DEFAULT
from targem.translate import translate

DEFAULT_CORPUS = Path(__file__).parent.parent.parent / "corpus" / "Targem.corpus.yaml"
DEFAULT_GLOSSARY = Path(__file__).parent.parent.parent / "corpus" / "Targem.glossary.yaml"
USER_ENV_FILE = Path.home() / ".targem"
PROVIDER_PACKAGE = {"claude": "anthropic", "openai": "openai"}
PROVIDER_KEY = {"claude": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}
PROVIDER_HOST = {"claude": "api.anthropic.com", "openai": "api.openai.com"}
PROVIDER_URL = {"claude": "https://api.anthropic.com/", "openai": "https://api.openai.com/"}
PROVIDER_DEFAULT_MODEL = {"claude": CLAUDE_DEFAULT, "openai": OPENAI_DEFAULT}


class DefaultCommandGroup(click.Group):
    """Click group that routes bare invocations to a default subcommand."""

    def __init__(self, *args, default_cmd_name: str, **kwargs):
        self.default_cmd_name = default_cmd_name
        super().__init__(*args, **kwargs)

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        if not args or args[0] not in self.commands:
            args.insert(0, self.default_cmd_name)
        return super().parse_args(ctx, args)


def load_runtime_env() -> None:
    """Load user-level env file without overriding existing env vars."""
    if not load_dotenv:
        return

    user_env_path = Path.home() / ".targem"
    if user_env_path.is_file():
        load_dotenv(user_env_path, override=False)


def resolve_provider(provider: str) -> str:
    """Pick a provider explicitly or infer it from available environment keys."""
    load_runtime_env()

    if provider != "auto":
        return provider

    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_openai = bool(os.environ.get("OPENAI_API_KEY"))

    if has_anthropic:
        return "claude"
    if has_openai:
        return "openai"

    raise click.UsageError(
        "No provider configured. Set ANTHROPIC_API_KEY for Claude or "
        "OPENAI_API_KEY for OpenAI, or pass --provider explicitly."
    )


def is_key_present(provider: str) -> bool:
    return bool(os.environ.get(PROVIDER_KEY[provider]))


def is_package_installed(provider: str) -> bool:
    return importlib.util.find_spec(PROVIDER_PACKAGE[provider]) is not None


def check_dns(host: str) -> tuple[bool, str]:
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        addresses = []
        for info in infos:
            address = info[4][0]
            if address not in addresses:
                addresses.append(address)
        if not addresses:
            return False, "no addresses returned"
        return True, ", ".join(addresses[:2])
    except OSError as e:
        return False, str(e)


def check_https(url: str, timeout: float = 5.0) -> tuple[bool, str]:
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return True, f"HTTP {response.status}"
    except urllib.error.HTTPError as e:
        return True, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", e)
        return False, str(reason)


def emit_check(label: str, ok: bool, detail: str) -> None:
    status = "ok" if ok else "fail"
    suffix = f" ({detail})" if detail else ""
    click.echo(f"{label}: {status}{suffix}", err=True)


def run_preflight_checks(provider: str, model: str | None = None) -> None:
    selected_model = model or PROVIDER_DEFAULT_MODEL[provider]
    click.echo("── Targem diagnostics ──", err=True)
    emit_check("provider selected", True, f"{provider} / {selected_model}")

    emit_check("key present", is_key_present(provider), "")

    package_name = PROVIDER_PACKAGE[provider]
    emit_check("package installed", is_package_installed(provider), package_name)

    host = PROVIDER_HOST[provider]
    dns_ok, dns_detail = check_dns(host)
    emit_check("DNS works", dns_ok, f"{host} -> {dns_detail}")

    url = PROVIDER_URL[provider]
    https_ok, https_detail = check_https(url)
    emit_check("HTTPS connection works", https_ok, f"{url} -> {https_detail}")


def emit_model_call_result(provider: str, model: str | None, ok: bool, detail: str) -> None:
    selected_model = model or PROVIDER_DEFAULT_MODEL[provider]
    emit_check("model call works", ok, f"{selected_model} / {detail}")


@click.group(cls=DefaultCommandGroup, default_cmd_name="translate")
def cli() -> None:
    """Targem command line interface."""


@cli.command(name="translate")
@click.argument("text", required=False)
@click.option("--in", "--file", "-f", "input_file", type=click.Path(exists=True, path_type=Path), help="Read input text from a file.")
@click.option("--corpus", type=click.Path(exists=True, path_type=Path), default=None, help="Path to corpus YAML. Defaults to bundled corpus.")
@click.option("--glossary", type=click.Path(exists=True, path_type=Path), default=None, help="Path to glossary YAML. Defaults to bundled glossary.")
@click.option("--k", default=5, show_default=True, help="Number of exemplars to retrieve.")
@click.option(
    "--provider",
    default="auto",
    show_default=True,
    type=click.Choice(["auto", "claude", "openai"]),
    help="Model provider. 'auto' prefers Claude if both keys exist, otherwise uses whichever provider is configured.",
)
@click.option("--model", default=None, help="Model name override (e.g. gpt-4o, claude-opus-4-7).")
@click.option("--show-examples", is_flag=True, help="Print retrieved exemplars after translation.")
@click.option("--debug-prompt", is_flag=True, help="Print retrieved exemplars and full prompt before translating.")
@click.option("--doctor", is_flag=True, help="Run provider, package, network, and model-call diagnostics.")
@click.option(
    "--out",
    "--output",
    "-o",
    "output",
    type=click.Path(path_type=Path),
    default=None,
    help="Write the translation to a file instead of stdout.",
)
def cli(
    text: str | None,
    input_file: Path | None,
    corpus: Path | None,
    glossary: Path | None,
    k: int,
    provider: str,
    model: str | None,
    show_examples: bool,
    debug_prompt: bool,
    doctor: bool,
    output: Path | None,
) -> None:
    """Targem — translate English to educated spoken Egyptian Arabic."""
    load_runtime_env()
    resolved_provider = resolve_provider(provider)

    if doctor:
        run_preflight_checks(resolved_provider, model=model)
        try:
            translate(
                "hello",
                corpus_path=corpus or DEFAULT_CORPUS,
                glossary_path=glossary or DEFAULT_GLOSSARY,
                k=1,
                provider=resolved_provider,
                model=model,
            )
        except SystemExit as e:
            emit_model_call_result(resolved_provider, model, False, str(e).splitlines()[0])
            raise

        emit_model_call_result(resolved_provider, model, True, "request succeeded")
        return

    if input_file:
        source = input_file.read_text(encoding="utf-8").strip()
    elif text:
        source = text
    elif not sys.stdin.isatty():
        source = sys.stdin.read().strip()
    else:
        raise click.UsageError("Provide TEXT, --file, or pipe input via stdin.")

    corpus_path = corpus or DEFAULT_CORPUS
    glossary_path = glossary or DEFAULT_GLOSSARY

    if debug_prompt:
        from targem.corpus import load_corpus
        from targem.glossary import load_glossary, match_glossary
        from targem.prompt import build_messages
        from targem.retrieval import TFIDFRetriever
        pairs = load_corpus(corpus_path)
        retriever = TFIDFRetriever(pairs)
        exemplars = retriever.retrieve(source, k=k)
        glossary_entries = load_glossary(glossary_path) if glossary_path.exists() else []
        matched_glossary = match_glossary(source, glossary_entries)
        messages = build_messages(source, exemplars, glossary_entries=matched_glossary)
        click.echo("── Retrieved exemplars ──", err=True)
        for ex in exemplars:
            click.echo(f"  EN: {ex.english[:80]}", err=True)
            click.echo(f"  AR: {ex.egyptian_arabic[:80]}", err=True)
        if matched_glossary:
            click.echo("── Matched glossary ──", err=True)
            for entry in matched_glossary:
                click.echo(f"  {entry.source} -> {entry.target}", err=True)
        click.echo("── Prompt ──", err=True)
        click.echo(messages[0]["content"], err=True)
        click.echo("── Translation ──", err=True)

    translation, exemplars = translate(
        source,
        corpus_path=corpus_path,
        glossary_path=glossary_path,
        k=k,
        provider=resolved_provider,
        model=model,
    )

    if output:
        output.write_text(translation + "\n", encoding="utf-8")
    else:
        click.echo(translation)

    if show_examples and not debug_prompt:
        click.echo("\n── Retrieved exemplars ──", err=True)
        for ex in exemplars:
            click.echo(f"  EN: {ex.english[:80]}", err=True)
            click.echo(f"  AR: {ex.egyptian_arabic[:80]}", err=True)
