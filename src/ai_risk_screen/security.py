"""Security helpers: HTML escaping and URL validation."""

from __future__ import annotations

import html
import re
from urllib.parse import urlparse

_HTTPS_URL_PATTERN = re.compile(r"^https://[^\s]+$")
_UNSAFE_SCHEMES = frozenset({"javascript", "data", "vbscript", "file"})


def escape_html(text: str) -> str:
    """Escape user-supplied text for safe HTML embedding."""
    return html.escape(text, quote=True)


_MARKDOWN_SPECIAL = '\\`*_{}[]()#+-.!|>'


def escape_markdown(text: str) -> str:
    """Escape Markdown metacharacters and neutralize raw HTML in user text."""
    safe = html.escape(str(text), quote=False)
    escaped: list[str] = []
    for char in safe:
        if char in _MARKDOWN_SPECIAL:
            escaped.append("\\")
        escaped.append(char)
    return "".join(escaped)


def is_safe_https_url(url: str) -> bool:
    """Return True if url is an absolute https URL with no unsafe scheme."""
    if not url or not isinstance(url, str):
        return False
    stripped = url.strip()
    if stripped.startswith("//"):
        return False
    if not _HTTPS_URL_PATTERN.match(stripped):
        return False
    parsed = urlparse(stripped)
    if parsed.scheme.lower() != "https":
        return False
    return parsed.netloc != ""


def validate_url_field(url: str | None, field_name: str) -> list[str]:
    """Validate an optional URL field; return error messages."""
    if url is None or url == "":
        return []
    if not is_safe_https_url(url):
        return [f"{field_name}: URL must be absolute https (got unsafe or invalid value)"]
    return []


def collect_url_errors(data: dict[str, object]) -> list[str]:
    """Collect URL validation errors from a screen document."""
    errors: list[str] = []
    meta = data.get("meta")
    if isinstance(meta, dict):
        ref = meta.get("reference_url")
        if isinstance(ref, str):
            errors.extend(validate_url_field(ref, "meta.reference_url"))
    steps = data.get("steps")
    if isinstance(steps, dict):
        tool = steps.get("tool")
        if isinstance(tool, dict):
            vendor_url = tool.get("vendor_url")
            if isinstance(vendor_url, str):
                errors.extend(validate_url_field(vendor_url, "steps.tool.vendor_url"))
    return errors
