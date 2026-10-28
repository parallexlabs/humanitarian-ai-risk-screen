"""Blank template export for screens, charters, and ledgers."""

from __future__ import annotations

import os
from pathlib import Path

BLANK_SCREEN_YAML = """# Humanitarian AI Risk Screen: blank template
meta:
  task_name: ""
  organization: ""
  screen_date: "YYYY-MM-DD"
  screen_owner: ""
  reference_url: ""  # optional, https only

steps:
  purpose:
    reviewer:
      name: ""
      role: ""
    task_description: ""
    non_ai_alternative: ""
    ai_value_proposition: ""
    non_ai_viable: false
    complete: false

  people:
    reviewer:
      name: ""
      role: ""
    affected_groups: ""
    partners_to_consult: ""
    safety_language_context: ""
    partner_review_needed: false
    protection_review_needed: false
    complete: false

  data:
    reviewer:
      name: ""
      role: ""
    data_types: ""
    authority_basis: ""
    minimization_plan: ""
    retention_plan: ""
    includes_personal_data: false
    includes_prohibited_input: false
    includes_sensitive_non_personal: false
    privacy_review_needed: false
    complete: false

  tool:
    reviewer:
      name: ""
      role: ""
    tool_name: ""
    vendor_name: ""
    processing_location: ""
    access_controls: ""
    onward_use_policy: ""
    fallback_plan: ""
    tool_approved: false
    vendor_url: ""  # optional, https only
    complete: false

  output:
    reviewer:
      name: ""
      role: ""
    verification_plan: ""
    trusted_sources: ""
    bias_exclusion_test: ""
    high_stakes_decision: false
    output_reviewable: false
    complete: false

  human_control:
    reviewer:
      name: ""
      role: ""
    decision_maker: ""
    record_keeper: ""
    override_process: ""
    remedy_process: ""
    safe_remedy_available: false
    complete: false

  monitoring:
    reviewer:
      name: ""
      role: ""
    pilot_scope: ""
    failure_threshold: ""
    incident_route: ""
    review_date: "YYYY-MM-DD"
    withdrawal_rule: ""
    controlled_pilot_required: false
    complete: false
"""

PILOT_CHARTER_MD = """# Pilot charter template

| Field | Response |
|-------|----------|
| **1. Owner** | Name, role, contact |
| **2. Task and baseline** | What the pilot does; how work is done today without AI |
| **3. Permitted inputs** | Data types and sources allowed in the pilot |
| **4. Tool and vendor** | Approved tool, version, processing location |
| **5. Affected-person and partner role** | Who is affected; who must be consulted |
| **6. Success and subgroup checks** | Success criteria; checks for excluded groups |
| **7. Human approval** | Who approves outputs before use |
| **8. Monitoring** | Metrics, review cadence, incident logging |
| **9. Stop and remedy** | Failure threshold; how to withdraw; remedy path |
| **10. Close-out lessons** | What worked, what failed, recommendations |
"""

SOURCE_CHECK_LEDGER_MD = """# Source-check ledger template

| # | Claim or number in output | Trusted source | Source URL (https) | Checker | Date | Result |
|---|---------------------------|----------------|--------------------|---------|------|--------|
| 1 | | | | | | pass / fail / not found |
| 2 | | | | | | |
| 3 | | | | | | |
"""

TEMPLATE_FILES: dict[str, str] = {
    "blank-screen.yaml": BLANK_SCREEN_YAML,
    "pilot-charter.md": PILOT_CHARTER_MD,
    "source-check-ledger.md": SOURCE_CHECK_LEDGER_MD,
}


class TemplateExportError(OSError):
    """Raised when template export cannot proceed safely."""


def _reject_symlink(path: Path) -> None:
    if path.is_symlink() or os.path.islink(path):
        msg = f"Refusing to write through symlink: {path}"
        raise TemplateExportError(msg)


def export_templates(output_dir: Path, *, force: bool = False) -> list[Path]:
    """Write blank templates to output_dir; return paths written."""
    _reject_symlink(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if output_dir.is_symlink():
        msg = f"Refusing to write through symlink: {output_dir}"
        raise TemplateExportError(msg)

    written: list[Path] = []
    for filename, content in TEMPLATE_FILES.items():
        path = output_dir / filename
        _reject_symlink(path)
        if path.exists() and not force:
            msg = f"File already exists: {path} (use --force to overwrite)"
            raise TemplateExportError(msg)
        flags = "w" if force else "x"
        with path.open(flags, encoding="utf-8") as handle:
            handle.write(content)
        written.append(path)
    return written
