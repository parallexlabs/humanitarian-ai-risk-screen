"""Content parity checks between English and French documents."""

from __future__ import annotations

import re
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "content"
FR_LABEL = "Traduction de travail"


def _read(rel: str) -> str:
    return (CONTENT / rel).read_text(encoding="utf-8")


def test_french_documents_keep_working_translation_label() -> None:
    for path in (CONTENT / "fr").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert FR_LABEL in text


def test_risk_screen_seven_steps_and_outcome_rules() -> None:
    en = _read("en/risk-screen.md")
    fr = _read("fr/risk-screen.md")
    for n in range(1, 8):
        assert f"## Step {n}" in en
        assert f"## Étape {n}" in fr
    for marker in (
        "**Stop if:**",
        "**Stop (red) if:**",
        "**Flag for amber review if:**",
        "**Arrêt si :**",
        "**Arrêt (rouge) si :**",
        "**Signaler pour examen ambre si :**",
    ):
        assert marker in en or marker in fr


def test_risk_screen_outcome_rule_markers_parity() -> None:
    en = _read("en/risk-screen.md")
    fr = _read("fr/risk-screen.md")
    assert en.count("**Stop") + en.count("**Flag for amber") == 8
    assert fr.count("**Arrêt") + fr.count("**Signaler pour examen ambre") == 8


def test_case_cards_facilitator_sections() -> None:
    en = _read("en/case-cards.md")
    fr = _read("fr/case-cards.md")
    assert en.count("### Facilitator notes") == 4
    assert fr.count("### Notes pour l'animateur") == 4


def test_pilot_charter_row_counts() -> None:
    en = _read("en/pilot-charter.md")
    fr = _read("fr/pilot-charter.md")
    en_rows = len(re.findall(r"^\| \d+ \|", en, re.MULTILINE))
    fr_rows = len(re.findall(r"^\| \d+ \|", fr, re.MULTILINE))
    assert en_rows == fr_rows == 10
    assert "## Sign-off" in en
    assert "## Approbation" in fr


def test_source_check_ledger_row_counts() -> None:
    en = _read("en/source-check-ledger.md")
    fr = _read("fr/source-check-ledger.md")
    en_rows = len(re.findall(r"^\| [123] \|", en, re.MULTILINE))
    fr_rows = len(re.findall(r"^\| [123] \|", fr, re.MULTILINE))
    assert en_rows == fr_rows == 3
