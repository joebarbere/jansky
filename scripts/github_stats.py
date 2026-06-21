#!/usr/bin/env python3
"""Generate the "At a glance" summary block in docs/github.md from the YAML catalogue.

The block (between the BEGIN/END markers) is derived from
``docs/data/radio_github.yml`` so the page's headline counts can never drift from the
data. ``tests/test_github_data.py`` runs ``--check`` to enforce this.

Usage::

    uv run python scripts/github_stats.py            # check (exit 1 if out of sync)
    uv run python scripts/github_stats.py --check     # same, explicit
    uv run python scripts/github_stats.py --write      # regenerate the block in place
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "docs" / "data" / "radio_github.yml"
PAGE_PATH = REPO / "docs" / "github.md"

BEGIN = "<!-- BEGIN github-stats -->"
END = "<!-- END github-stats -->"

# Display order and labels for the per-kind summary.
KINDS = [
    ("org", "Organizations & collaborations"),
    ("repo", "Software repositories"),
    ("person", "People"),
    ("beyond-github", "Beyond GitHub (GitLab / SourceForge)"),
]


def render_block() -> str:
    """Render the BEGIN..END stats block from the YAML."""
    entries = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))["entries"]
    counts: dict[str, int] = {}
    for e in entries:
        counts[e["kind"]] = counts.get(e["kind"], 0) + 1
    n_categories = len({e["category"] for e in entries})
    total = len(entries)

    lines = [
        BEGIN,
        f"*{total} catalogued entries across {n_categories} categories — generated from "
        "`docs/data/radio_github.yml` by `scripts/github_stats.py` (kept in sync by a test).*",
        "",
        "| Kind | Entries |",
        "|---|---|",
    ]
    for kind, label in KINDS:
        lines.append(f"| {label} | {counts.get(kind, 0)} |")
    lines.append(f"| **Total** | **{total}** |")
    lines.append(END)
    return "\n".join(lines)


def current_block(text: str) -> str | None:
    """Return the existing BEGIN..END block in ``text``, or None if absent."""
    i = text.find(BEGIN)
    j = text.find(END)
    if i == -1 or j == -1 or j < i:
        return None
    return text[i : j + len(END)]


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite the block in docs/github.md")
    parser.add_argument("--check", action="store_true", help="check the block is in sync (default)")
    parser.parse_args(argv)

    page = PAGE_PATH.read_text(encoding="utf-8")
    want = render_block()
    have = current_block(page)
    if have is None:
        print(f"markers {BEGIN} / {END} not found in {PAGE_PATH}", file=sys.stderr)
        return 1

    if "--write" in (argv if argv is not None else sys.argv[1:]):
        PAGE_PATH.write_text(page.replace(have, want), encoding="utf-8")
        print("docs/github.md stats block updated.")
        return 0

    if have != want:
        print(
            "docs/github.md stats block is OUT OF SYNC with the YAML; "
            "run: uv run python scripts/github_stats.py --write",
            file=sys.stderr,
        )
        return 1
    print("docs/github.md stats block is in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
