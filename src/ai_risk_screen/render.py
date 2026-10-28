"""HTML and Markdown report rendering with accessibility structure."""

from __future__ import annotations

from typing import Any

from ai_risk_screen.outcome import OutcomeResult
from ai_risk_screen.security import escape_html, escape_markdown

STEP_TITLES: dict[str, str] = {
    "purpose": "1. Purpose and non-AI alternative",
    "people": "2. People and partners",
    "data": "3. Data",
    "tool": "4. Tool and vendor",
    "output": "5. Output verification",
    "human_control": "6. Human control",
    "monitoring": "7. Monitoring and stop",
}

OUTCOME_CSS_CLASS: dict[str, str] = {
    "green": "outcome-green",
    "amber": "outcome-amber",
    "red": "outcome-red",
}


def _reviewer_line(step: dict[str, Any]) -> str:
    reviewer = step.get("reviewer", {})
    if not isinstance(reviewer, dict):
        return ""
    name = reviewer.get("name", "")
    role = reviewer.get("role", "")
    return f"{name} ({role})"


def render_markdown(data: dict[str, Any], outcome: OutcomeResult) -> str:
    """Render an accessible Markdown report."""
    meta = data.get("meta", {})
    lines: list[str] = [
        "# Humanitarian AI Risk Screen Report",
        "",
        f"**Outcome:** {escape_markdown(outcome.label)}",
        "",
        "## Task",
        "",
        f"- **Task:** {escape_markdown(str(meta.get('task_name', '')))}",
        f"- **Organization:** {escape_markdown(str(meta.get('organization', '')))}",
        f"- **Screen date:** {escape_markdown(str(meta.get('screen_date', '')))}",
        f"- **Screen owner:** {escape_markdown(str(meta.get('screen_owner', '')))}",
        "",
        "## Outcome reasons",
        "",
    ]
    for rule_id, reason in zip(outcome.rule_ids, outcome.reasons, strict=False):
        lines.append(f"- [{escape_markdown(rule_id)}] {escape_markdown(reason)}")
    lines.append("")
    steps = data.get("steps", {})
    if isinstance(steps, dict):
        for key, title in STEP_TITLES.items():
            step = steps.get(key, {})
            if not isinstance(step, dict):
                continue
            lines.extend(
                [
                    f"## {escape_markdown(title)}",
                    "",
                    f"**Accountable reviewer:** {escape_markdown(_reviewer_line(step))}",
                    "",
                ]
            )
            for field, value in step.items():
                if field in {"reviewer", "complete"}:
                    continue
                label = escape_markdown(field.replace("_", " ").title())
                lines.append(f"- **{label}:** {escape_markdown(str(value))}")
            lines.append("")
    return "\n".join(lines)


def render_html(data: dict[str, Any], outcome: OutcomeResult) -> str:
    """Render an accessible HTML report with landmarks and text labels."""
    meta = data.get("meta", {})
    task_name = escape_html(str(meta.get("task_name", "")))
    organization = escape_html(str(meta.get("organization", "")))
    screen_date = escape_html(str(meta.get("screen_date", "")))
    screen_owner = escape_html(str(meta.get("screen_owner", "")))
    outcome_label = escape_html(outcome.label)
    outcome_class = OUTCOME_CSS_CLASS.get(outcome.level, "outcome-amber")

    reasons_html = "\n".join(
        f"<li><span class='rule-id'>{escape_html(rid)}</span> "
        f"{escape_html(reason)}</li>"
        for rid, reason in zip(outcome.rule_ids, outcome.reasons, strict=False)
    )

    steps_html_parts: list[str] = []
    steps = data.get("steps", {})
    if isinstance(steps, dict):
        for key, title in STEP_TITLES.items():
            step = steps.get(key, {})
            if not isinstance(step, dict):
                continue
            fields_html = "\n".join(
                f"<dt>{escape_html(field.replace('_', ' ').title())}</dt>"
                f"<dd>{escape_html(str(value))}</dd>"
                for field, value in step.items()
                if field not in {"reviewer", "complete"}
            )
            reviewer = escape_html(_reviewer_line(step))
            steps_html_parts.append(
                f"""<section class="screen-step" aria-labelledby="step-{key}">
  <h2 id="step-{key}">{escape_html(title)}</h2>
  <p><strong>Accountable reviewer:</strong> {reviewer}</p>
  <dl>{fields_html}</dl>
</section>"""
            )

    steps_html = "\n".join(steps_html_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Humanitarian AI Risk Screen | {task_name}</title>
  <style>
    :root {{
      --text: #1a1a1a;
      --bg: #ffffff;
      --border: #cccccc;
    }}
    body {{
      font-family: system-ui, -apple-system, sans-serif;
      line-height: 1.6;
      max-width: 48rem;
      margin: 0 auto;
      padding: 1.5rem;
      color: var(--text);
      background: var(--bg);
    }}
    .outcome-banner {{
      border: 2px solid var(--border);
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 4px;
    }}
    .outcome-green {{ border-left: 6px solid #2d6a4f; }}
    .outcome-amber {{ border-left: 6px solid #b08900; }}
    .outcome-red {{ border-left: 6px solid #9b2226; }}
    .outcome-text-label {{
      font-weight: 700;
      display: block;
      margin-bottom: 0.5rem;
    }}
    .rule-id {{ font-family: monospace; margin-right: 0.5rem; }}
    dl {{ margin: 0.5rem 0; }}
    dt {{ font-weight: 600; margin-top: 0.5rem; }}
    dd {{ margin-left: 0; margin-bottom: 0.25rem; }}
    nav {{ margin-bottom: 1.5rem; }}
  </style>
</head>
<body>
  <header role="banner">
    <h1>Humanitarian AI Risk Screen Report</h1>
  </header>
  <nav aria-label="Report sections">
    <a href="#outcome">Outcome</a> |
    <a href="#task">Task</a> |
    <a href="#steps">Screen steps</a>
  </nav>
  <main role="main">
    <section id="outcome" aria-labelledby="outcome-heading">
      <h2 id="outcome-heading">Outcome</h2>
      <div class="outcome-banner {outcome_class}" role="status"
           aria-label="Screen outcome: {outcome_label}">
        <span class="outcome-text-label">{outcome_label}</span>
        <ul>{reasons_html}</ul>
      </div>
    </section>
    <section id="task" aria-labelledby="task-heading">
      <h2 id="task-heading">Task</h2>
      <dl>
        <dt>Task</dt><dd>{task_name}</dd>
        <dt>Organization</dt><dd>{organization}</dd>
        <dt>Screen date</dt><dd>{screen_date}</dd>
        <dt>Screen owner</dt><dd>{screen_owner}</dd>
      </dl>
    </section>
    <section id="steps" aria-labelledby="steps-heading">
      <h2 id="steps-heading">Screen steps</h2>
      {steps_html}
    </section>
  </main>
  <footer role="contentinfo">
    <p><small>Generated by Humanitarian AI Risk Screen (ParalleX Labs Inc.)</small></p>
  </footer>
</body>
</html>"""
