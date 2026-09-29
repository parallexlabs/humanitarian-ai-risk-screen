"""Tests for template export safety."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_risk_screen.templates import TemplateExportError, export_templates


def test_export_writes_all(tmp_path: Path) -> None:
    paths = export_templates(tmp_path)
    assert len(paths) == 3
    assert (tmp_path / "blank-screen.yaml").is_file()


def test_export_refuses_existing_file(tmp_path: Path) -> None:
    export_templates(tmp_path)
    with pytest.raises(TemplateExportError, match="already exists"):
        export_templates(tmp_path)


def test_export_force_overwrites(tmp_path: Path) -> None:
    export_templates(tmp_path)
    paths = export_templates(tmp_path, force=True)
    assert len(paths) == 3


def test_export_refuses_symlink_destination(tmp_path: Path) -> None:
    target = tmp_path / "real"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target)
    with pytest.raises(TemplateExportError, match="symlink"):
        export_templates(link)


def test_export_refuses_symlink_file(tmp_path: Path) -> None:
    real = tmp_path / "real.yaml"
    real.write_text("x", encoding="utf-8")
    link = tmp_path / "blank-screen.yaml"
    link.symlink_to(real)
    with pytest.raises(TemplateExportError, match="symlink"):
        export_templates(tmp_path)
