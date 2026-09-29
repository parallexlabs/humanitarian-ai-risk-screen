"""Additional loader coverage."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_risk_screen.loader import LoadError, load_yaml_safe


def test_empty_yaml(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    with pytest.raises(LoadError, match="Empty"):
        load_yaml_safe(path)


def test_non_mapping_yaml(tmp_path: Path) -> None:
    path = tmp_path / "list.yaml"
    path.write_text("- item\n", encoding="utf-8")
    with pytest.raises(LoadError, match="mapping"):
        load_yaml_safe(path)
