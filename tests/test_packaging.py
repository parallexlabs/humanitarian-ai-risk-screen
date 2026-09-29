"""Tests for wheel packaging and importlib.resources access."""

from __future__ import annotations

import json
from importlib import resources

from ai_risk_screen import __version__


def test_version_is_0_2_0() -> None:
    assert __version__ == "0.2.0"


def test_schema_available_from_package_data() -> None:
    schema_path = resources.files("ai_risk_screen.data").joinpath("screen.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema["title"] == "Humanitarian AI Risk Screen"
    required = schema["$defs"]["step_tool"]["required"]
    assert "tool_approved" in required


def test_content_available_from_package() -> None:
    content_root = resources.files("ai_risk_screen.content")
    en_screen = content_root.joinpath("en/risk-screen.md")
    fr_screen = content_root.joinpath("fr/risk-screen.md")
    assert "seven-step" in en_screen.read_text(encoding="utf-8")
    assert "Traduction de travail" in fr_screen.read_text(encoding="utf-8")
