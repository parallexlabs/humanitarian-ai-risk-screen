"""JSON Schema validation for completed screens."""

from __future__ import annotations

import json
from importlib import resources
from typing import Any, cast

from jsonschema import Draft202012Validator, FormatChecker

from ai_risk_screen.security import collect_url_errors


def load_schema() -> dict[str, Any]:
    """Load the screen JSON Schema from package resources."""
    resource = resources.files("ai_risk_screen.data").joinpath("screen.schema.json")
    with resource.open(encoding="utf-8") as fh:
        return cast(dict[str, Any], json.load(fh))


def get_validator() -> Draft202012Validator:
    """Return a compiled JSON Schema validator."""
    return Draft202012Validator(load_schema(), format_checker=FormatChecker())


def validate_screen(data: dict[str, Any]) -> list[str]:
    """Validate screen data; return list of error messages (empty if valid)."""
    validator = get_validator()
    errors: list[str] = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in err.path) if err.path else "(root)"
        errors.append(f"{path}: {err.message}")
    errors.extend(collect_url_errors(data))
    return errors
