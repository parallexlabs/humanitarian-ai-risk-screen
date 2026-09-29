"""Tests for JSON Schema validation."""

from __future__ import annotations

from typing import Any

from ai_risk_screen.validate import validate_screen


def test_valid_green_screen(green_screen: dict[str, Any]) -> None:
    errors = validate_screen(green_screen)
    assert errors == []


def test_missing_required_field() -> None:
    data: dict[str, Any] = {"meta": {"task_name": "x"}}
    errors = validate_screen(data)
    assert any("meta" in e or "steps" in e for e in errors)


def test_invalid_date_format() -> None:
    data: dict[str, Any] = {
        "meta": {
            "task_name": "t",
            "organization": "o",
            "screen_date": "not-a-date",
            "screen_owner": "owner",
        },
        "steps": {},
    }
    errors = validate_screen(data)
    assert any("screen_date" in e for e in errors)


def test_rejects_bad_url_in_schema() -> None:
    data: dict[str, Any] = {
        "meta": {
            "task_name": "t",
            "organization": "o",
            "screen_date": "2026-01-01",
            "screen_owner": "owner",
            "reference_url": "ftp://bad.example.org",
        },
        "steps": {
            "purpose": {
                "reviewer": {"name": "n", "role": "r"},
                "task_description": "d",
                "non_ai_alternative": "a",
                "ai_value_proposition": "v",
                "complete": True,
            },
            "people": {
                "reviewer": {"name": "n", "role": "r"},
                "affected_groups": "g",
                "partners_to_consult": "p",
                "safety_language_context": "c",
                "complete": True,
            },
            "data": {
                "reviewer": {"name": "n", "role": "r"},
                "data_types": "d",
                "authority_basis": "a",
                "minimization_plan": "m",
                "retention_plan": "r",
                "complete": True,
            },
            "tool": {
                "reviewer": {"name": "n", "role": "r"},
                "tool_name": "t",
                "vendor_name": "v",
                "processing_location": "l",
                "access_controls": "a",
                "onward_use_policy": "o",
                "fallback_plan": "f",
                "complete": True,
            },
            "output": {
                "reviewer": {"name": "n", "role": "r"},
                "verification_plan": "v",
                "trusted_sources": "s",
                "bias_exclusion_test": "b",
                "complete": True,
            },
            "human_control": {
                "reviewer": {"name": "n", "role": "r"},
                "decision_maker": "d",
                "record_keeper": "k",
                "override_process": "o",
                "remedy_process": "r",
                "complete": True,
            },
            "monitoring": {
                "reviewer": {"name": "n", "role": "r"},
                "pilot_scope": "p",
                "failure_threshold": "f",
                "incident_route": "i",
                "review_date": "2026-01-01",
                "withdrawal_rule": "w",
                "complete": True,
            },
        },
    }
    errors = validate_screen(data)
    assert any("reference_url" in e for e in errors)
