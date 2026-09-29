"""Tests for Markdown escaping in reports."""

from __future__ import annotations

from typing import Any

from ai_risk_screen.outcome import OutcomeResult
from ai_risk_screen.render import render_markdown

INJECTION = (
    '<script>alert(1)</script> [link](https://evil.example) '
    "![img](https://evil.example/x.png) `code`"
)


def _screen_with_meta(**meta_fields: str) -> dict[str, Any]:
    meta = {
        "task_name": "Task",
        "organization": "Org",
        "screen_date": "2026-01-01",
        "screen_owner": "Owner",
    }
    meta.update(meta_fields)
    return {"meta": meta, "steps": {}}


def _outcome() -> OutcomeResult:
    return OutcomeResult(
        level="amber",
        label="Amber — Pause",
        reasons=(INJECTION,),
        rule_ids=("A1",),
    )


def test_markdown_escapes_meta_task_name() -> None:
    md = render_markdown(_screen_with_meta(task_name=INJECTION), _outcome())
    assert "<script>" not in md
    assert "[link](https://evil.example)" not in md
    assert "![img]" not in md


def test_markdown_escapes_meta_organization() -> None:
    md = render_markdown(_screen_with_meta(organization=INJECTION), _outcome())
    assert "<script>" not in md
    assert "\\[link\\]" in md or "[link]" not in md


def test_markdown_escapes_meta_screen_date() -> None:
    md = render_markdown(_screen_with_meta(screen_date=INJECTION), _outcome())
    assert "<script>" not in md


def test_markdown_escapes_meta_screen_owner() -> None:
    md = render_markdown(_screen_with_meta(screen_owner=INJECTION), _outcome())
    assert "<script>" not in md


def test_markdown_escapes_outcome_label_and_reasons() -> None:
    outcome = OutcomeResult(
        level="red",
        label=f"Red {INJECTION}",
        reasons=(INJECTION,),
        rule_ids=(INJECTION,),
    )
    md = render_markdown(_screen_with_meta(), outcome)
    assert "<script>" not in md
    assert "alert\\(1\\)" in md or "&lt;script&gt;" in md


def test_markdown_escapes_step_fields() -> None:
    data: dict[str, Any] = {
        "meta": {
            "task_name": "Task",
            "organization": "Org",
            "screen_date": "2026-01-01",
            "screen_owner": "Owner",
        },
        "steps": {
            "purpose": {
                "reviewer": {"name": INJECTION, "role": INJECTION},
                "task_description": INJECTION,
                "complete": True,
            }
        },
    }
    md = render_markdown(data, _outcome())
    assert "<script>" not in md
    assert "![img]" not in md
