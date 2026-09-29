"""Ensure packaged content matches repository content/."""

from __future__ import annotations

from pathlib import Path


def test_packaged_content_matches_repo_content() -> None:
    repo = Path(__file__).resolve().parent.parent / "content"
    pkg = Path(__file__).resolve().parent.parent / "src" / "ai_risk_screen" / "content"
    for path in repo.rglob("*.md"):
        rel = path.relative_to(repo)
        assert (pkg / rel).read_text(encoding="utf-8") == path.read_text(encoding="utf-8")
