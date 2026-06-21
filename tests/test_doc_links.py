"""Guard against broken in-notebook cross-links.

`mkdocs --strict` validates links in the prose `.md` pages but not the ones
*inside* notebooks (mkdocs-jupyter renders those, and `mkdocs_hooks.py` rewrites
them to the site's URL form at build time). The hook can only rewrite a link
whose basename matches a real page; a typo'd target (e.g. a notebook that was
renamed) silently 404s on the site. This test catches exactly that class of bug
without building the site.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
DOCS_DIR = ROOT / "docs"

# Markdown links to a local .ipynb or .md target (optionally with an #anchor).
_LINK_RE = re.compile(r"\]\((?!https?://|//)([^)]+?\.(?:ipynb|md))(?:#[^)]*)?\)")

_NB_STEMS = {p.stem for p in NB_DIR.glob("*.ipynb")}
_DOC_STEMS = {p.stem for p in DOCS_DIR.glob("*.md")}


def _markdown(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(c.get("source", []))
        for c in nb.get("cells", [])
        if c.get("cell_type") == "markdown"
    )


@pytest.mark.parametrize("nb_path", sorted(NB_DIR.glob("*.ipynb")), ids=lambda p: p.name)
def test_notebook_links_target_real_pages(nb_path):
    bad = []
    for target in _LINK_RE.findall(_markdown(nb_path)):
        name = Path(target).name
        stem, ext = name.rsplit(".", 1)
        known = _NB_STEMS if ext == "ipynb" else _DOC_STEMS
        if stem not in known:
            bad.append(target)
    assert not bad, f"{nb_path.name} links to non-existent page(s): {sorted(set(bad))}"
