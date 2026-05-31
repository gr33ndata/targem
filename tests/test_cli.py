import os
from pathlib import Path

import pytest
from click import UsageError
from click.testing import CliRunner

from targem.cli import cli, load_runtime_env, resolve_provider, run_preflight_checks


def test_resolve_provider_auto_prefers_anthropic(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-test")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")

    assert resolve_provider("auto") == "claude"


def test_resolve_provider_auto_uses_openai_when_only_openai_is_set(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")

    assert resolve_provider("auto") == "openai"


def test_resolve_provider_preserves_explicit_choice(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    assert resolve_provider("openai") == "openai"


def test_resolve_provider_auto_requires_any_configured_provider(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(UsageError):
        resolve_provider("auto")


def test_load_runtime_env_reads_home_targem_when_no_local_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    (tmp_path / ".targem").write_text("OPENAI_API_KEY=home-openai\n", encoding="utf-8")

    load_runtime_env()

    assert os.environ.get("OPENAI_API_KEY") == "home-openai"


def test_load_runtime_env_does_not_override_existing_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "existing-openai")
    (tmp_path / ".targem").write_text("OPENAI_API_KEY=home-openai\n", encoding="utf-8")

    load_runtime_env()

    assert os.environ.get("OPENAI_API_KEY") == "existing-openai"


def test_run_preflight_checks_logs_expected_lines(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setattr("targem.cli.is_package_installed", lambda provider: True)
    monkeypatch.setattr("targem.cli.check_dns", lambda host: (True, "1.2.3.4"))
    monkeypatch.setattr("targem.cli.check_https", lambda url: (True, "HTTP 401"))

    run_preflight_checks("openai", model="gpt-4o")

    captured = capsys.readouterr()
    assert "provider selected: ok (openai / gpt-4o)" in captured.err
    assert "key present: ok" in captured.err
    assert "package installed: ok (openai)" in captured.err
    assert "DNS works: ok (api.openai.com -> 1.2.3.4)" in captured.err
    assert "HTTPS connection works: ok (https://api.openai.com/ -> HTTP 401)" in captured.err


def test_cli_doctor_logs_model_call_success(monkeypatch):
    runner = CliRunner()
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setattr("targem.cli.run_preflight_checks", lambda provider, model=None: None)
    monkeypatch.setattr(
        "targem.cli.translate",
        lambda *args, **kwargs: ("ده ترجمة تجريبية بالمصري.", []),
    )

    result = runner.invoke(cli, ["--doctor", "--provider", "openai"])

    assert result.exit_code == 0
    assert "model call works: ok (gpt-4o / request succeeded)" in result.stderr


def test_cli_debug_prompt_flag_still_prints_prompt(monkeypatch):
    runner = CliRunner()
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setattr("targem.cli.translate", lambda *args, **kwargs: ("ok", []))

    class _Example:
        english = "Hello world."
        egyptian_arabic = "أهلا"

    monkeypatch.setattr("targem.corpus.load_corpus", lambda path: [_Example()])

    class _Retriever:
        def __init__(self, pairs):
            self.pairs = pairs

        def retrieve(self, source, k=5):
            return self.pairs

    monkeypatch.setattr("targem.retrieval.TFIDFRetriever", _Retriever)
    monkeypatch.setattr(
        "targem.prompt.build_messages",
        lambda source, exemplars, glossary_entries=None: [{"content": "PROMPT"}],
    )

    result = runner.invoke(cli, ["--debug-prompt", "--provider", "openai", "Hello world."])

    assert result.exit_code == 0
    assert "── Prompt ──" in result.stderr
    assert "PROMPT" in result.stderr


def test_cli_output_writes_translation_to_file(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setattr("targem.cli.translate", lambda *args, **kwargs: ("ده ترجمة تجريبية بالمصري.", []))
    out = tmp_path / "out.txt"

    result = runner.invoke(cli, ["--provider", "openai", "--out", str(out), "Hello world."])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert out.read_text(encoding="utf-8") == "ده ترجمة تجريبية بالمصري.\n"


def test_cli_in_and_out_options_work_together(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setattr("targem.cli.translate", lambda *args, **kwargs: ("ده ترجمة تجريبية بالمصري.", []))
    input_file = tmp_path / "article.txt"
    output_file = tmp_path / "translation.txt"
    input_file.write_text("Hello world.", encoding="utf-8")

    result = runner.invoke(cli, ["--provider", "openai", "--in", str(input_file), "--out", str(output_file)])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert output_file.read_text(encoding="utf-8") == "ده ترجمة تجريبية بالمصري.\n"
