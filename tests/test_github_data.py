"""Validate docs/data/radio_github.yml and keep it in sync with docs/github.md.

This is an offline, deterministic test (no network). Live-URL checking is done by
``scripts/check_dataset_urls.py --github docs/data/radio_github.yml`` (``make check-urls``).
"""

from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO = Path(__file__).resolve().parents[1]
YAML_PATH = REPO / "docs" / "data" / "radio_github.yml"
PAGE_PATH = REPO / "docs" / "github.md"
NOTEBOOKS = REPO / "notebooks"

VALID_KINDS = {"org", "repo", "person", "beyond-github"}


def _entries() -> list[dict]:
    data = yaml.safe_load(YAML_PATH.read_text())
    return data["entries"]


def _notebook_numbers() -> set[int]:
    nums = set()
    for p in NOTEBOOKS.glob("[0-9][0-9]_*.ipynb"):
        nums.add(int(p.name[:2]))
    return nums


def test_yaml_parses_and_has_entries():
    entries = _entries()
    assert isinstance(entries, list) and len(entries) > 50


def test_required_fields_and_kinds():
    for e in _entries():
        assert isinstance(e.get("name"), str) and e["name"].strip(), e
        assert isinstance(e.get("url"), str) and e["url"].startswith("http"), e
        assert e.get("kind") in VALID_KINDS, e
        assert isinstance(e.get("category"), str) and e["category"].strip(), e


def test_urls_are_unique():
    urls = [e["url"] for e in _entries()]
    dupes = {u for u in urls if urls.count(u) > 1}
    assert not dupes, f"duplicate urls: {sorted(dupes)}"


def test_chapters_map_to_real_notebooks():
    available = _notebook_numbers()
    assert available, "no chapter notebooks found"
    for e in _entries():
        for ch in e.get("chapters", []) or []:
            assert isinstance(ch, int), e
            assert ch in available, f"{e['name']} references missing chapter {ch}"


def test_paper_blocks_are_well_formed():
    for e in _entries():
        paper = e.get("paper")
        if paper is None:
            continue
        assert isinstance(paper, dict), e
        assert isinstance(paper.get("cite"), str) and paper["cite"].strip(), e
        assert isinstance(paper.get("url"), str) and paper["url"].startswith("http"), e


def test_every_entry_url_appears_on_the_page():
    """Sync guard: the data file must not drift from the human-facing page."""
    page = PAGE_PATH.read_text()
    missing = [e["url"] for e in _entries() if e["url"] not in page]
    assert not missing, f"urls in YAML but not in docs/github.md: {missing}"
