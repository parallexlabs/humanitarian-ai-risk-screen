"""Tests for HTML and Markdown rendering."""

from __future__ import annotations

from typing import Any

from ai_risk_screen.outcome import evaluate_outcome
from ai_risk_screen.render import render_html, render_markdown


def test_markdown_contains_outcome_label(green_screen: dict[str, Any]) -> None:
    outcome = evaluate_outcome(green_screen)
    md = render_markdown(green_screen, outcome)
    assert "Green" in md
    assert "low risk, proceed with checks" in md
    assert "Humanitarian AI Risk Screen Report" in md


def test_html_has_single_h1(green_screen: dict[str, Any]) -> None:
    outcome = evaluate_outcome(green_screen)
    html = render_html(green_screen, outcome)
    assert html.count("<h1") == 1
    assert 'role="banner"' in html
    assert 'role="main"' in html
    assert 'role="contentinfo"' in html


def test_html_escapes_user_input() -> None:
    data: dict[str, Any] = {
        "meta": {
            "task_name": "<img src=x onerror=alert(1)>",
            "organization": "Org",
            "screen_date": "2026-01-01",
            "screen_owner": "Owner",
        },
        "steps": {},
    }
    outcome = evaluate_outcome(data)
    html = render_html(data, outcome)
    assert "<img" not in html
    assert "&lt;img" in html


def test_html_outcome_has_text_label(green_screen: dict[str, Any]) -> None:
    outcome = evaluate_outcome(green_screen)
    html = render_html(green_screen, outcome)
    assert "outcome-text-label" in html
    assert "outcome-green" in html
    assert "Green" in html


def test_html_amber_class(amber_privacy_screen: dict[str, Any]) -> None:
    outcome = evaluate_outcome(amber_privacy_screen)
    html = render_html(amber_privacy_screen, outcome)
    assert "outcome-amber" in html
    assert "Amber" in html


def test_html_red_class(red_prohibited_screen: dict[str, Any]) -> None:
    outcome = evaluate_outcome(red_prohibited_screen)
    html = render_html(red_prohibited_screen, outcome)
    assert "outcome-red" in html
    assert "Red" in html


def test_html_landmarks_and_labels() -> None:
    data: dict[str, Any] = {
        "meta": {
            "task_name": "Test",
            "organization": "O",
            "screen_date": "2026-01-01",
            "screen_owner": "Owner",
        },
        "steps": {
            "purpose": {
                "reviewer": {"name": "A", "role": "B"},
                "task_description": "desc",
                "complete": True,
            }
        },
    }
    outcome = evaluate_outcome(data)
    html = render_html(data, outcome)
    assert 'aria-label="Report sections"' in html
    assert "aria-labelledby" in html
