"""Tests for deterministic outcome rules."""

from __future__ import annotations

from typing import Any

from ai_risk_screen.outcome import evaluate_outcome


def test_green_screen(green_screen: dict[str, Any]) -> None:
    result = evaluate_outcome(green_screen)
    assert result.level == "green"
    assert "G1" in result.rule_ids


def test_red_prohibited_input(red_prohibited_screen: dict[str, Any]) -> None:
    result = evaluate_outcome(red_prohibited_screen)
    assert result.level == "red"
    assert "R1" in result.rule_ids


def test_red_unapproved_tool() -> None:
    data = {
        "steps": {
            "tool": {"tool_approved": False},
            "human_control": {"safe_remedy_available": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "red"
    assert "R2" in result.rule_ids


def test_red_high_stakes_unreviewable() -> None:
    data = {
        "steps": {
            "tool": {"tool_approved": True},
            "output": {"high_stakes_decision": True, "output_reviewable": False},
            "human_control": {"safe_remedy_available": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "red"
    assert "R3" in result.rule_ids


def test_red_no_remedy() -> None:
    data = {
        "steps": {
            "tool": {"tool_approved": True},
            "human_control": {"safe_remedy_available": False},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "red"
    assert "R4" in result.rule_ids


def test_amber_privacy_review() -> None:
    data = {
        "steps": {
            "data": {"privacy_review_needed": True},
            "tool": {"tool_approved": True},
            "human_control": {"safe_remedy_available": True},
            "purpose": {"complete": True},
            "people": {"complete": True},
            "output": {"complete": True},
            "monitoring": {"complete": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "amber"
    assert "A1" in result.rule_ids


def test_amber_partner_review(amber_privacy_screen: dict[str, Any]) -> None:
    result = evaluate_outcome(amber_privacy_screen)
    assert result.level == "amber"
    assert "A3" in result.rule_ids


def test_amber_incomplete_steps() -> None:
    data = {
        "steps": {
            "purpose": {"complete": False},
            "people": {"complete": True},
            "data": {"complete": True},
            "tool": {"tool_approved": True, "complete": True},
            "output": {"complete": True},
            "human_control": {"safe_remedy_available": True, "complete": True},
            "monitoring": {"complete": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "amber"
    assert "A0" in result.rule_ids


def test_amber_personal_data_no_authority() -> None:
    data = {
        "steps": {
            "data": {"includes_personal_data": True, "authority_basis": ""},
            "tool": {"tool_approved": True},
            "human_control": {"safe_remedy_available": True},
            "purpose": {"complete": True},
            "people": {"complete": True},
            "output": {"complete": True},
            "monitoring": {"complete": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "amber"
    assert "A5" in result.rule_ids


def test_amber_output_not_reviewable() -> None:
    data = {
        "steps": {
            "data": {"complete": True},
            "tool": {"tool_approved": True, "complete": True},
            "output": {"output_reviewable": False, "complete": True},
            "human_control": {"safe_remedy_available": True, "complete": True},
            "purpose": {"complete": True},
            "people": {"complete": True},
            "monitoring": {"complete": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "amber"
    assert "A8" in result.rule_ids


def test_red_takes_priority_over_amber() -> None:
    data = {
        "steps": {
            "data": {
                "includes_prohibited_input": True,
                "privacy_review_needed": True,
            },
            "tool": {"tool_approved": True},
            "human_control": {"safe_remedy_available": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "red"
