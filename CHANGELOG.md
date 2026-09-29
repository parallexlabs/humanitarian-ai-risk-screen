# Changelog

## 0.2.0 — 2026-09-28

### Fixed

- Unified Python and browser outcome predicates with explicit `is True` / `is False` checks; missing rule-driving booleans now trigger amber (A9) and never green.
- Made all rule-driving booleans required in `schemas/screen.schema.json`.
- Exposed predicate semantics in `ai-risk-screen rules` JSON output and README.
- Escaped Markdown metacharacters and neutralized raw HTML in Markdown reports.
- Completed French translations to parity with English (risk screen stop/amber rules, facilitator notes, charter sign-off, ledger rows).
- Synchronized `docs/sources.html` with `research/SOURCES.md` (exact titles, issuers, URLs, verification status).
- Set mypy `python_version` to 3.12; CI runs mypy and pyright on 3.12 while runtime tests cover 3.11 and 3.12.
- Template export now uses exclusive file creation by default, rejects symlink destinations, and adds `--force`.
- Added `:focus-visible` styles for interactive controls.
- Included `schemas/` and `content/` in the wheel via `importlib.resources`.

### Added

- Shared outcome truth-table fixture with Python pytest and Node `node --test` parity coverage.
- Automated French/English content parity tests.
- CI wheel smoke tests for `validate`, `evaluate`, `report`, and `export-templates`.
- Markdown injection regression tests.

## 0.1.0 — 2026-09-28

Initial public toolkit release.
