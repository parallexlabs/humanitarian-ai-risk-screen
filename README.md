<p align="center" class="brand-mark">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/brand/parallex-mark-dark.png">
    <img src=".github/brand/parallex-mark.png" alt="ParalleX Labs" width="120">
  </picture>
</p>

# Humanitarian AI Risk Screen

An open resource by **ParalleX Labs Inc.**, a small British Columbia company, to help humanitarian and NGO staff decide whether and how to use an AI tool for a task.

**This is not** an official standard, legal advice, or your organisation's policy. All training cases are **synthetic**. No clients or deployments are claimed.

**Status:** early release (0.2.0). The rules have not been tested with a humanitarian organization.

## Open by design

**We build in the open.** ParalleX Labs Inc. publishes its tools, methods and learning materials under open licences, so public-interest teams can use them, check how they work and adapt them freely. Open work is easier to trust, because anyone can see exactly how a result is produced. Code is licensed under Apache-2.0 and content under CC BY 4.0.

**Our own work, and only ours.** Everything in this repository was created by ParalleX Labs Inc. from public data and synthetic examples. It contains no client data, no client projects, and no one else's confidential information or intellectual property.

## What is included

- **Seven-step risk screen** with accountable reviewers per step
- **Pilot charter** template (10 fields) for amber outcomes
- **Four synthetic case cards** with answer keys and facilitator notes
- **Source-check ledger** template
- **Curriculum source matrix** (`SOURCES.md`)
- **CLI** (`ai-risk-screen`) for validation, scoring, and reporting
- **Static site** (`docs/`) with a client-side scorer (no data leaves the browser)

## Licences

| Component | Licence |
|-----------|---------|
| Code | [Apache-2.0](LICENSE) |
| Content under `content/` | [CC BY 4.0](LICENSE-CONTENT) |

Copyright ParalleX Labs Inc.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Export blank templates
ai-risk-screen export-templates ./templates

# Validate and evaluate a completed screen
ai-risk-screen validate examples/green_screen.yaml
ai-risk-screen evaluate examples/green_screen.yaml
ai-risk-screen report examples/green_screen.yaml -o report.html

# Show documented outcome rules
ai-risk-screen rules
```

Open `docs/index.html` in a browser for the toolkit site and scorer.

## Outcome rules

Outcomes are computed **deterministically** from explicit flags in the screen file. Every rule uses strict boolean predicates (`value is True` or `value is False`); missing rule-driving fields trigger amber rule **A9** and never green. Run `ai-risk-screen rules` for machine-readable paths and predicates.

### Red: do not use

| Rule | Predicate |
|------|-----------|
| R1 | `steps.data.includes_prohibited_input` **is True** |
| R2 | `steps.tool.tool_approved` **is False** |
| R3 | `steps.output.high_stakes_decision` **is True** AND `steps.output.output_reviewable` **is False** |
| R4 | `steps.human_control.safe_remedy_available` **is False** |

### Amber: pause for review and a controlled pilot

| Rule | Predicate |
|------|-----------|
| A0 | Any step `complete` **is False** or missing |
| A1 | `steps.data.privacy_review_needed` **is True** |
| A2 | `steps.people.protection_review_needed` **is True** |
| A3 | `steps.people.partner_review_needed` **is True** |
| A4 | `steps.monitoring.controlled_pilot_required` **is True** |
| A5 | `steps.data.includes_personal_data` **is True** AND `authority_basis` is empty |
| A6 | `steps.data.includes_sensitive_non_personal` **is True** AND `minimization_plan` is empty |
| A7 | `steps.output.high_stakes_decision` **is True** |
| A8 | `steps.output.output_reviewable` **is False** |
| A9 | Any rule-driving boolean is missing or not a boolean |

### Green: low risk, proceed with checks

| Rule | Predicate |
|------|-----------|
| G1 | All steps complete; no red or amber predicates match |

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
pyright
python -m build
```

## Citation

See [CITATION.cff](CITATION.cff).

## Source matrix

See [SOURCES.md](SOURCES.md) for the instruments and their verification status.
