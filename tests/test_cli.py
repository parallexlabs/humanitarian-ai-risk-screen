"""Tests for CLI commands."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from ai_risk_screen.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.2.0" in result.output


def test_validate_green() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(FIXTURES / "green_screen.yaml")])
    assert result.exit_code == 0
    assert "Valid" in result.output


def test_evaluate_green() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["evaluate", str(FIXTURES / "green_screen.yaml")])
    assert result.exit_code == 0
    assert "Green" in result.output


def test_evaluate_red() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["evaluate", str(FIXTURES / "red_prohibited.yaml")])
    assert result.exit_code == 0
    assert "Red" in result.output


def test_report_html(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "report.html"
    result = runner.invoke(
        main,
        [
            "report",
            str(FIXTURES / "green_screen.yaml"),
            "--format",
            "html",
            "-o",
            str(out),
        ],
    )
    assert result.exit_code == 0
    assert out.is_file()
    content = out.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content


def test_export_templates(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["export-templates", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / "blank-screen.yaml").is_file()
    assert (tmp_path / "pilot-charter.md").is_file()


def test_rules_json() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["rules"])
    assert result.exit_code == 0
    assert "R1" in result.output
    assert "A1" in result.output
