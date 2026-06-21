"""MkDocs build hooks for the jansky site.

mkdocs-jupyter renders each notebook to HTML but does **not** rewrite the
relative links inside it. A link that is correct when the notebook is opened in
JupyterLab — a sibling notebook ``31_x.ipynb`` or a prose page ``../docs/page.md``
— therefore 404s on the built site, where notebooks live at ``notebooks/<stem>/``
and prose pages at ``<stem>/`` (``use_directory_urls`` is on).

This hook rewrites those links in the rendered notebook pages to the site's
directory-URL form, so the published site works while the notebooks keep their
Jupyter-correct relative links. External (``http``) links are left untouched.
"""

from __future__ import annotations

import re

# href="<path ending in .ipynb or .md>[#anchor]"
_LINK_RE = re.compile(r'(href=")([^"#]+?\.(?:ipynb|md))((?:#[^"]*)?)(")')

# Populated in on_files: the stems that actually exist as built pages, so we
# never rewrite a link into a target that isn't there.
_STEMS: dict[str, set[str]] = {"notebooks": set(), "docs": set()}


def on_files(files, config, **kwargs):
    notebooks: set[str] = set()
    docs: set[str] = set()
    for f in files:
        src = f.src_path.replace("\\", "/")
        if src.startswith("notebooks/") and src.endswith(".ipynb"):
            notebooks.add(src.rsplit("/", 1)[-1][: -len(".ipynb")])
        elif src.endswith(".md") and "/" not in src:
            docs.add(src[: -len(".md")])
    _STEMS["notebooks"], _STEMS["docs"] = notebooks, docs
    return files


def on_post_page(output: str, page, config, **kwargs) -> str:
    src = page.file.src_path.replace("\\", "/")
    if not (src.startswith("notebooks/") and src.endswith(".ipynb")):
        return output

    def _rewrite(match: re.Match) -> str:
        pre, path, anchor, post = match.groups()
        if path.startswith(("http://", "https://", "//")):
            return match.group(0)
        name = path.rsplit("/", 1)[-1]
        if name.endswith(".ipynb"):
            stem = name[: -len(".ipynb")]
            if stem in _STEMS["notebooks"]:
                return f"{pre}../{stem}/{anchor}{post}"
        elif name.endswith(".md"):
            stem = name[: -len(".md")]
            if stem in _STEMS["docs"]:
                return f"{pre}../../{stem}/{anchor}{post}"
        return match.group(0)

    return _LINK_RE.sub(_rewrite, output)
