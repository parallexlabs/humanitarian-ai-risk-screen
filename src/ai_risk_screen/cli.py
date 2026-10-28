"""Command-line interface for ai-risk-screen."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from ai_risk_screen import __version__
from ai_risk_screen.loader import LoadError, load_screen
from ai_risk_screen.outcome import evaluate_outcome
from ai_risk_screen.render import render_html, render_markdown
from ai_risk_screen.templates import TemplateExportError, export_templates
from ai_risk_screen.validate import validate_screen


@click.group()
@click.version_option(__version__, prog_name="ai-risk-screen")
def main() -> None:
    """Humanitarian AI Risk Screen: validate, score, and report."""


@main.command("validate")
@click.argument("screen_file", type=click.Path(exists=True, path_type=Path))
def validate_cmd(screen_file: Path) -> None:
    """Validate a completed screen file against the JSON Schema."""
    try:
        data = load_screen(screen_file)
    except LoadError as exc:
        click.echo(f"Load error: {exc}", err=True)
        sys.exit(1)
    errors = validate_screen(data)
    if errors:
        for err in errors:
            click.echo(err, err=True)
        sys.exit(1)
    click.echo("Valid.")


@main.command("evaluate")
@click.argument("screen_file", type=click.Path(exists=True, path_type=Path))
def evaluate_cmd(screen_file: Path) -> None:
    """Evaluate outcome (green, amber, red) for a screen file."""
    try:
        data = load_screen(screen_file)
    except LoadError as exc:
        click.echo(f"Load error: {exc}", err=True)
        sys.exit(1)
    errors = validate_screen(data)
    if errors:
        click.echo("Validation errors:", err=True)
        for err in errors:
            click.echo(f"  {err}", err=True)
        sys.exit(1)
    outcome = evaluate_outcome(data)
    click.echo(outcome.label)
    for rule_id, reason in zip(outcome.rule_ids, outcome.reasons, strict=False):
        click.echo(f"  [{rule_id}] {reason}")


@main.command("report")
@click.argument("screen_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["html", "markdown", "md"]),
    default="html",
    help="Output format",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    help="Output file (default: stdout)",
)
def report_cmd(screen_file: Path, fmt: str, output: Path | None) -> None:
    """Render an HTML or Markdown report for a validated screen."""
    try:
        data = load_screen(screen_file)
    except LoadError as exc:
        click.echo(f"Load error: {exc}", err=True)
        sys.exit(1)
    errors = validate_screen(data)
    if errors:
        for err in errors:
            click.echo(err, err=True)
        sys.exit(1)
    outcome = evaluate_outcome(data)
    content = render_html(data, outcome) if fmt == "html" else render_markdown(data, outcome)
    if output:
        output.write_text(content, encoding="utf-8")
        click.echo(f"Wrote {output}")
    else:
        click.echo(content)


@main.command("export-templates")
@click.argument(
    "output_dir",
    type=click.Path(path_type=Path),
    default=".",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing template files",
)
def export_templates_cmd(output_dir: Path, force: bool) -> None:
    """Export blank screen, pilot charter, and source-check ledger templates."""
    try:
        paths = export_templates(output_dir, force=force)
    except TemplateExportError as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)
    for path in paths:
        click.echo(f"Wrote {path}")


@main.command("rules")
def rules_cmd() -> None:
    """Print documented outcome rules as JSON."""
    from ai_risk_screen.outcome import rules_document

    click.echo(json.dumps(rules_document(), indent=2))


if __name__ == "__main__":
    main()
