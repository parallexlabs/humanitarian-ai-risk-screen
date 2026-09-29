"""Safe loading of YAML and JSON screen files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from ai_risk_screen.security import collect_url_errors


class LoadError(ValueError):
    """Raised when a screen file cannot be loaded safely."""


def load_yaml_safe(path: Path) -> dict[str, Any]:
    """Load YAML using safe_load only (no arbitrary object construction)."""
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if data is None:
        raise LoadError(f"Empty YAML file: {path}")
    if not isinstance(data, dict):
        raise LoadError(f"Expected mapping at root of {path}")
    return data


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON screen file."""
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise LoadError(f"Expected object at root of {path}")
    return data


def load_screen(path: Path) -> dict[str, Any]:
    """Load a screen from YAML or JSON based on extension."""
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = load_yaml_safe(path)
    elif suffix == ".json":
        data = load_json(path)
    else:
        raise LoadError(f"Unsupported file extension: {suffix}")

    url_errors = collect_url_errors(data)
    if url_errors:
        raise LoadError("; ".join(url_errors))
    return data
