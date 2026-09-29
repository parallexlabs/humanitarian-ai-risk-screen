"""Tests for safe YAML/JSON loading."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_risk_screen.loader import LoadError, load_screen, load_yaml_safe

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_yaml_safe(green_screen: object) -> None:
    path = FIXTURES / "green_screen.yaml"
    data = load_yaml_safe(path)
    assert data["meta"]["task_name"] == "Draft internal meeting notes"


def test_load_screen_yaml() -> None:
    data = load_screen(FIXTURES / "green_screen.yaml")
    assert "steps" in data


def test_load_screen_json(tmp_path: Path, green_screen: object) -> None:
    import json

    path = tmp_path / "screen.json"
    path.write_text(json.dumps(green_screen), encoding="utf-8")
    data = load_screen(path)
    assert data["meta"]["organization"] == "Synthetic Aid Org"


def test_rejects_unsafe_url_in_yaml(tmp_path: Path, green_screen: dict[str, object]) -> None:
    import copy

    data = copy.deepcopy(green_screen)
    meta = dict(data["meta"]) if isinstance(data.get("meta"), dict) else {}
    meta["reference_url"] = "javascript:alert(1)"
    data["meta"] = meta
    path = tmp_path / "bad.yaml"
    path.write_text(yaml.dump(data), encoding="utf-8")
    with pytest.raises(LoadError, match="reference_url"):
        load_screen(path)


def test_rejects_unknown_extension(tmp_path: Path) -> None:
    path = tmp_path / "screen.txt"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(LoadError, match="Unsupported"):
        load_screen(path)
