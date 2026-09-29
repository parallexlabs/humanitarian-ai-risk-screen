"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def green_screen() -> dict[str, Any]:
    path = FIXTURES / "green_screen.yaml"
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.fixture
def red_prohibited_screen() -> dict[str, Any]:
    path = FIXTURES / "red_prohibited.yaml"
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.fixture
def amber_privacy_screen() -> dict[str, Any]:
    path = FIXTURES / "amber_privacy.yaml"
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))
