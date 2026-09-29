"""CLI error-path tests for coverage."""

from __future__ import annotations

from pathlib import Path

import yaml
from click.testing import CliRunner

from ai_risk_screen.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_validate_load_error(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("not: [valid", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(bad)])
    assert result.exit_code == 1


def test_validate_schema_failure(tmp_path: Path) -> None:
    bad = tmp_path / "incomplete.yaml"
    bad.write_text(yaml.dump({"meta": {"task_name": "only"}}), encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(bad)])
    assert result.exit_code == 1


def test_report_markdown_stdout() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["report", str(FIXTURES / "green_screen.yaml"), "--format", "markdown"],
    )
    assert result.exit_code == 0
    assert "# Humanitarian AI Risk Screen Report" in result.output


def test_report_validation_failure(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.dump({"meta": {"task_name": "x"}}), encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["report", str(bad)])
    assert result.exit_code == 1


def test_evaluate_load_error(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["evaluate", str(bad)])
    assert result.exit_code == 1
