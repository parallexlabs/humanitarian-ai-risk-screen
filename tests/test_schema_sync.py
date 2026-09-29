"""Ensure repository schema matches packaged schema."""

from __future__ import annotations

import json
from pathlib import Path


def test_repo_schema_matches_package_schema() -> None:
    repo = Path(__file__).resolve().parent.parent / "schemas" / "screen.schema.json"
    pkg = (
        Path(__file__).resolve().parent.parent
        / "src"
        / "ai_risk_screen"
        / "data"
        / "screen.schema.json"
    )
    assert json.loads(repo.read_text(encoding="utf-8")) == json.loads(
        pkg.read_text(encoding="utf-8")
    )
