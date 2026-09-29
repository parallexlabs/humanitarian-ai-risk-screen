"""Additional outcome rule coverage."""

from __future__ import annotations

from ai_risk_screen.outcome import evaluate_outcome


def test_amber_protection_review() -> None:
    data = {
        "steps": {
            "people": {"protection_review_needed": True, "complete": True},
            "tool": {"tool_approved": True, "complete": True},
            "human_control": {"safe_remedy_available": True, "complete": True},
            "purpose": {"complete": True},
            "data": {"complete": True},
            "output": {"complete": True},
            "monitoring": {"complete": True},
        }
    }
    result = evaluate_outcome(data)
    assert result.level == "amber"
    assert "A2" in result.rule_ids


def test_amber_controlled_pilot() -> None:
    data = {
        "steps": {
            "monitoring": {"controlled_pilot_required": True, "complete": True},
            "tool": {"tool_approved": True, "complete": True},
            "human_control": {"safe_remedy_available": True, "complete": True},
            "purpose": {"complete": True},
            "people": {"complete": True},
            "data": {"complete": True},
            "output": {"complete": True},
        }
    }
    result = evaluate_outcome(data)
    assert "A4" in result.rule_ids


def test_amber_sensitive_without_minimization() -> None:
    data = {
        "steps": {
            "data": {
                "includes_sensitive_non_personal": True,
                "minimization_plan": "",
                "complete": True,
            },
            "tool": {"tool_approved": True, "complete": True},
            "human_control": {"safe_remedy_available": True, "complete": True},
            "purpose": {"complete": True},
            "people": {"complete": True},
            "output": {"complete": True},
            "monitoring": {"complete": True},
        }
    }
    result = evaluate_outcome(data)
    assert "A6" in result.rule_ids
