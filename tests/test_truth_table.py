"""Truth-table parity tests for Python outcome evaluation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ai_risk_screen.outcome import evaluate_outcome

TRUTH_TABLE = Path(__file__).parent / "fixtures" / "outcome-truth-table.json"


@pytest.fixture(scope="module")
def truth_cases() -> list[dict[str, Any]]:
    payload = json.loads(TRUTH_TABLE.read_text(encoding="utf-8"))
    return payload["cases"]


TRUTH_CASES: list[dict[str, Any]] = json.loads(TRUTH_TABLE.read_text(encoding="utf-8"))["cases"]


@pytest.mark.parametrize("case", TRUTH_CASES, ids=lambda c: c["id"])
def test_truth_table_case(case: dict[str, Any]) -> None:
    result = evaluate_outcome(case["input"])
    expected = case["expected"]
    assert result.level == expected["level"]
    for rule_id in expected["rule_ids"]:
        assert rule_id in result.rule_ids


def test_truth_table_never_green_on_missing_fields(truth_cases: list[dict[str, Any]]) -> None:
    missing_cases = [
        case
        for case in truth_cases
        if "missing" in case["id"] or case["expected"].get("rule_ids") == ["A9"]
    ]
    assert missing_cases
    for case in missing_cases:
        result = evaluate_outcome(case["input"])
        assert result.level != "green"
