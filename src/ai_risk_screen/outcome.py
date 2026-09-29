"""Deterministic outcome rules for the humanitarian AI risk screen."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

OutcomeLevel = Literal["green", "amber", "red"]


@dataclass(frozen=True)
class OutcomeResult:
    """Screen outcome with documented reasons."""

    level: OutcomeLevel
    label: str
    reasons: tuple[str, ...] = field(default_factory=tuple)
    rule_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RuleSpec:
    """Documented outcome rule with explicit predicate semantics."""

    rule_id: str
    description: str
    path: tuple[str, ...]
    predicate: str


STEP_KEYS: tuple[str, ...] = (
    "purpose",
    "people",
    "data",
    "tool",
    "output",
    "human_control",
    "monitoring",
)

RULE_DRIVING_BOOLEAN_PATHS: tuple[tuple[str, ...], ...] = (
    ("steps", "data", "includes_prohibited_input"),
    ("steps", "tool", "tool_approved"),
    ("steps", "output", "high_stakes_decision"),
    ("steps", "output", "output_reviewable"),
    ("steps", "human_control", "safe_remedy_available"),
    ("steps", "data", "privacy_review_needed"),
    ("steps", "people", "protection_review_needed"),
    ("steps", "people", "partner_review_needed"),
    ("steps", "monitoring", "controlled_pilot_required"),
    ("steps", "data", "includes_personal_data"),
    ("steps", "data", "includes_sensitive_non_personal"),
    *tuple(("steps", key, "complete") for key in STEP_KEYS),
)

OUTCOME_LABELS: dict[OutcomeLevel, str] = {
    "green": "Green — Approved low-risk assistance with source checking",
    "amber": "Amber — Pause for review and controlled pilot",
    "red": "Red — Do not use",
}

RED_RULES: tuple[RuleSpec, ...] = (
    RuleSpec(
        "R1",
        "Prohibited input declared in the data step",
        ("steps", "data", "includes_prohibited_input"),
        "value is True",
    ),
    RuleSpec(
        "R2",
        "Tool is not on the organization's approved list",
        ("steps", "tool", "tool_approved"),
        "value is False",
    ),
    RuleSpec(
        "R3",
        "High-stakes decision with output that cannot be human-reviewed",
        ("steps", "output", "high_stakes_decision"),
        "value is True AND steps.output.output_reviewable is False",
    ),
    RuleSpec(
        "R4",
        "No safe remedy path for people affected by errors",
        ("steps", "human_control", "safe_remedy_available"),
        "value is False",
    ),
)

AMBER_RULES: tuple[RuleSpec, ...] = (
    RuleSpec(
        "A0",
        "One or more screen steps are not marked complete",
        ("steps",),
        "any step complete is False or missing",
    ),
    RuleSpec(
        "A1",
        "Privacy review required before use",
        ("steps", "data", "privacy_review_needed"),
        "value is True",
    ),
    RuleSpec(
        "A2",
        "Protection review required before use",
        ("steps", "people", "protection_review_needed"),
        "value is True",
    ),
    RuleSpec(
        "A3",
        "Partner consultation review required before use",
        ("steps", "people", "partner_review_needed"),
        "value is True",
    ),
    RuleSpec(
        "A4",
        "Controlled pilot required before wider rollout",
        ("steps", "monitoring", "controlled_pilot_required"),
        "value is True",
    ),
    RuleSpec(
        "A5",
        "Personal data involved without documented authority",
        ("steps", "data", "includes_personal_data"),
        "value is True AND steps.data.authority_basis is empty",
    ),
    RuleSpec(
        "A6",
        "Sensitive non-personal data (e.g. aid location) without minimization sign-off",
        ("steps", "data", "includes_sensitive_non_personal"),
        "value is True AND steps.data.minimization_plan is empty",
    ),
    RuleSpec(
        "A7",
        "High-stakes decision requires enhanced human review",
        ("steps", "output", "high_stakes_decision"),
        "value is True",
    ),
    RuleSpec(
        "A8",
        "Output verification not yet confirmed as reviewable",
        ("steps", "output", "output_reviewable"),
        "value is False",
    ),
)

GREEN_RULE = RuleSpec(
    "G1",
    "All steps complete; no red or amber triggers",
    ("steps",),
    "all step complete is True AND no red or amber predicates match",
)


def _get_value(data: dict[str, Any], *path: str) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _is_true(data: dict[str, Any], *path: str) -> bool:
    return _get_value(data, *path) is True


def _is_false(data: dict[str, Any], *path: str) -> bool:
    return _get_value(data, *path) is False


def _non_empty_string(data: dict[str, Any], *path: str) -> bool:
    value = _get_value(data, *path)
    if value is None:
        return False
    return str(value).strip() != ""


def _all_steps_complete(data: dict[str, Any]) -> bool:
    steps = data.get("steps")
    if not isinstance(steps, dict):
        return False
    for key in STEP_KEYS:
        step = steps.get(key)
        if not isinstance(step, dict) or step.get("complete") is not True:
            return False
    return True


def _missing_rule_driving_boolean(data: dict[str, Any]) -> bool:
    for path in RULE_DRIVING_BOOLEAN_PATHS:
        value = _get_value(data, *path)
        if not isinstance(value, bool):
            return True
    return False


def evaluate_outcome(data: dict[str, Any]) -> OutcomeResult:
    """Compute green, amber, or red outcome with explicit reasons."""
    red_reasons: list[str] = []
    red_ids: list[str] = []

    if _is_true(data, "steps", "data", "includes_prohibited_input"):
        red_ids.append("R1")
        red_reasons.append(RED_RULES[0].description)

    if _is_false(data, "steps", "tool", "tool_approved"):
        red_ids.append("R2")
        red_reasons.append(RED_RULES[1].description)

    if _is_true(data, "steps", "output", "high_stakes_decision") and _is_false(
        data, "steps", "output", "output_reviewable"
    ):
        red_ids.append("R3")
        red_reasons.append(RED_RULES[2].description)

    if _is_false(data, "steps", "human_control", "safe_remedy_available"):
        red_ids.append("R4")
        red_reasons.append(RED_RULES[3].description)

    if red_reasons:
        return OutcomeResult(
            level="red",
            label=OUTCOME_LABELS["red"],
            reasons=tuple(red_reasons),
            rule_ids=tuple(red_ids),
        )

    amber_reasons: list[str] = []
    amber_ids: list[str] = []

    if _missing_rule_driving_boolean(data):
        amber_ids.append("A9")
        amber_reasons.append("One or more required rule-driving fields are missing")

    if _is_true(data, "steps", "data", "privacy_review_needed"):
        amber_ids.append("A1")
        amber_reasons.append(AMBER_RULES[1].description)

    if _is_true(data, "steps", "people", "protection_review_needed"):
        amber_ids.append("A2")
        amber_reasons.append(AMBER_RULES[2].description)

    if _is_true(data, "steps", "people", "partner_review_needed"):
        amber_ids.append("A3")
        amber_reasons.append(AMBER_RULES[3].description)

    if _is_true(data, "steps", "monitoring", "controlled_pilot_required"):
        amber_ids.append("A4")
        amber_reasons.append(AMBER_RULES[4].description)

    if _is_true(data, "steps", "data", "includes_personal_data") and not _non_empty_string(
        data, "steps", "data", "authority_basis"
    ):
        amber_ids.append("A5")
        amber_reasons.append(AMBER_RULES[5].description)

    if _is_true(
        data, "steps", "data", "includes_sensitive_non_personal"
    ) and not _non_empty_string(data, "steps", "data", "minimization_plan"):
        amber_ids.append("A6")
        amber_reasons.append(AMBER_RULES[6].description)

    if _is_true(data, "steps", "output", "high_stakes_decision"):
        amber_ids.append("A7")
        amber_reasons.append(AMBER_RULES[7].description)

    if _is_false(data, "steps", "output", "output_reviewable"):
        amber_ids.append("A8")
        amber_reasons.append(AMBER_RULES[8].description)

    if not _all_steps_complete(data):
        amber_ids.append("A0")
        amber_reasons.append(AMBER_RULES[0].description)

    if amber_reasons:
        return OutcomeResult(
            level="amber",
            label=OUTCOME_LABELS["amber"],
            reasons=tuple(amber_reasons),
            rule_ids=tuple(amber_ids),
        )

    return OutcomeResult(
        level="green",
        label=OUTCOME_LABELS["green"],
        reasons=(GREEN_RULE.description,),
        rule_ids=(GREEN_RULE.rule_id,),
    )


def rules_document() -> dict[str, Any]:
    """Return machine-readable rule documentation with predicate semantics."""
    return {
        "red": [
            {
                "id": rule.rule_id,
                "description": rule.description,
                "path": list(rule.path),
                "predicate": rule.predicate,
            }
            for rule in RED_RULES
        ],
        "amber": [
            {
                "id": rule.rule_id,
                "description": rule.description,
                "path": list(rule.path),
                "predicate": rule.predicate,
            }
            for rule in AMBER_RULES
        ],
        "green": {
            "id": GREEN_RULE.rule_id,
            "description": GREEN_RULE.description,
            "path": list(GREEN_RULE.path),
            "predicate": GREEN_RULE.predicate,
        },
        "missing_fields": {
            "id": "A9",
            "description": "One or more required rule-driving fields are missing",
            "predicate": "any rule-driving boolean is missing or not a boolean",
        },
    }
