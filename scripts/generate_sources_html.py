"""Generate docs/sources.html from SOURCES.md curriculum matrix."""

from __future__ import annotations

import html
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_MD = REPO_ROOT / "SOURCES.md"
OUTPUT_HTML = REPO_ROOT / "docs" / "sources.html"

TABLE_HEADER = (
    "| Instrument | Exact title | Issuer | Year | Version | URL | "
    "Use in toolkit | Limits | Verification |"
)


def _parse_curriculum_rows(markdown: str) -> list[dict[str, str]]:
    if TABLE_HEADER not in markdown:
        msg = "Curriculum source matrix table not found in SOURCES.md"
        raise ValueError(msg)

    section = markdown.split("## Curriculum source matrix", 1)[1]
    section = section.split("\n---", 1)[0]
    rows: list[dict[str, str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("| Instrument"):
            continue
        if line.startswith("|-"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 9:
            continue
        rows.append(
            {
                "instrument": cells[0],
                "title": cells[1],
                "issuer": cells[2],
                "year": cells[3],
                "version": cells[4],
                "url": cells[5],
                "use": cells[6],
                "limits": cells[7],
                "verification": cells[8],
            }
        )
    return rows


def render_sources_html(rows: list[dict[str, str]]) -> str:
    body_rows = []
    for row in rows:
        url = row["url"]
        if url.startswith("https://"):
            url_cell = (
                f'<a href="{html.escape(url, quote=True)}">'
                f"{html.escape(url)}</a>"
            )
        else:
            url_cell = html.escape(url)
        body_rows.append(
            "<tr>"
            f"<td>{html.escape(row['instrument'])}</td>"
            f"<td>{html.escape(row['title'])}</td>"
            f"<td>{html.escape(row['issuer'])}</td>"
            f"<td>{html.escape(row['year'])}</td>"
            f"<td>{html.escape(row['version'])}</td>"
            f"<td>{url_cell}</td>"
            f"<td>{html.escape(row['use'])}</td>"
            f"<td>{html.escape(row['limits'])}</td>"
            f"<td>{html.escape(row['verification'])}</td>"
            "</tr>"
        )

    table_body = "\n        ".join(body_rows)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Source matrix — Humanitarian AI Risk Screen</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header role="banner">
    <h1>Curriculum source matrix</h1>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="screen.html">Risk screen</a></li>
        <li><a href="scorer.html">Screen scorer</a></li>
        <li><a href="cases.html">Case cards</a></li>
        <li><a href="sources.html" aria-current="page">Source matrix</a></li>
      </ul>
    </nav>
  </header>
  <main role="main">
    <p>Instruments that informed this toolkit. Verify URLs on the publisher page before citing. Generated from <code>SOURCES.md</code>.</p>
    <table>
      <caption class="sr-only">Curriculum source matrix</caption>
      <thead>
        <tr>
          <th scope="col">Instrument</th>
          <th scope="col">Exact title</th>
          <th scope="col">Issuer</th>
          <th scope="col">Year</th>
          <th scope="col">Version</th>
          <th scope="col">URL</th>
          <th scope="col">Use in toolkit</th>
          <th scope="col">Limits</th>
          <th scope="col">Verification</th>
        </tr>
      </thead>
      <tbody>
        {table_body}
      </tbody>
    </table>
  </main>
  <footer role="contentinfo">
    <p>Copyright ParalleX Labs Inc.</p>
  </footer>
</body>
</html>
"""


def generate_sources_html(
    sources_md: Path = SOURCES_MD,
    output_html: Path = OUTPUT_HTML,
) -> str:
    """Generate docs/sources.html from SOURCES.md."""
    markdown = sources_md.read_text(encoding="utf-8")
    rows = _parse_curriculum_rows(markdown)
    rendered = render_sources_html(rows)
    output_html.write_text(rendered, encoding="utf-8")
    return rendered


def expected_sources_html(sources_md: Path = SOURCES_MD) -> str:
    """Return HTML that would be generated from SOURCES.md without writing."""
    markdown = sources_md.read_text(encoding="utf-8")
    return render_sources_html(_parse_curriculum_rows(markdown))


def main() -> None:
    generate_sources_html()
    print(f"Wrote {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
