"""Tests that docs/sources.html matches SOURCES.md."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from generate_sources_html import OUTPUT_HTML, expected_sources_html  # noqa: E402


def test_sources_html_matches_sources_md() -> None:
    expected = expected_sources_html()
    actual = OUTPUT_HTML.read_text(encoding="utf-8")
    assert actual == expected


def test_sources_html_includes_ifrc_unverified_and_iasc_partial() -> None:
    html = OUTPUT_HTML.read_text(encoding="utf-8")
    assert "UNVERIFIED" in html
    assert "Partially verified" in html
    assert (
        "https://www.icrc.org/en/publication/"
        "building-responsible-humanitarian-approach-icrcs-policy-artificial-intelligence"
    ) in html
