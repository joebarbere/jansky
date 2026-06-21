#!/usr/bin/env python3
"""Check that the project's external URLs still resolve.

Covers two sources:

* every URL in ``jansky.data.DATASETS`` (the bundled sample datasets), and
* every external link in the documentation (``docs/resources.md`` by default,
  which advertises "All URLs below were verified live") — pass ``--docs`` to add
  these, or extra files after it.

Each URL gets a lightweight request (HEAD, falling back to a ranged GET for hosts
that reject HEAD). Checks run concurrently. Exits non-zero if any URL fails, so it
can gate CI or run on the ``dataset_watch`` cadence — a green run is the evidence
that the "verified live" claim is still true.

Usage::

    uv run python scripts/check_dataset_urls.py                 # datasets only
    uv run python scripts/check_dataset_urls.py --category small
    uv run python scripts/check_dataset_urls.py --docs          # + docs/resources.md
    uv run python scripts/check_dataset_urls.py --docs docs/telescopes.md
    uv run python scripts/check_dataset_urls.py --github        # + docs/data/radio_github.yml
    make check-urls                                             # datasets + resources + github, via make
"""

from __future__ import annotations

import argparse
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

from jansky.data import DATASETS

# Markdown inline links ``[text](url)`` and autolinks ``<url>``.
_LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)|<(https?://[^>\s]+)>")

_DEFAULT_DOC = "docs/resources.md"
_DEFAULT_GITHUB_YAML = "docs/data/radio_github.yml"

# Many sites reject the default python-requests User-Agent with a 403; a
# browser-like UA gets an honest status without pretending to be a person.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def extract_doc_urls(path: str | Path) -> list[str]:
    """Return the unique external URLs linked from a markdown file."""
    text = Path(path).read_text(encoding="utf-8")
    urls = {a or b for a, b in _LINK_RE.findall(text)}
    # Strip a trailing punctuation that sometimes sneaks into a match.
    return sorted(u.rstrip(".,;") for u in urls)


def extract_yaml_urls(path: str | Path) -> list[str]:
    """Return the unique URLs from a github-catalogue YAML (entry + paper links)."""
    import yaml  # imported lazily so the dataset-only path needs no PyYAML

    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    urls: set[str] = set()
    for entry in data.get("entries", []):
        if isinstance(entry.get("url"), str):
            urls.add(entry["url"])
        paper = entry.get("paper")
        if isinstance(paper, dict) and isinstance(paper.get("url"), str):
            urls.add(paper["url"])
    return sorted(urls)


# Codes where the *server answered* but blocked the bot (auth/forbidden/rate
# limit): the link is live for a human, so these are warnings, not failures.
_SOFT_CODES = {401, 403, 429}


def check(url: str, timeout: float = 30.0) -> tuple[str, str]:
    """Return (status, detail) where status is 'ok', 'warn', or 'fail'."""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout, headers=_HEADERS)
        if resp.status_code >= 400 or resp.status_code == 405:
            # Some hosts reject HEAD; retry with a 0-byte ranged GET.
            resp = requests.get(
                url,
                headers={**_HEADERS, "Range": "bytes=0-0"},
                stream=True,
                timeout=timeout,
            )
        code = resp.status_code
        if code < 400:
            return "ok", f"HTTP {code}"
        if code in _SOFT_CODES:
            return "warn", f"HTTP {code} (bot-blocked; live for humans)"
        return "fail", f"HTTP {code}"
    except Exception as exc:  # noqa: BLE001 - report any failure
        return "fail", f"ERROR: {type(exc).__name__}"


def _check_targets(targets: list[tuple[str, str]]) -> int:
    """Check (label, url) pairs concurrently; print results; return failure count."""
    failures = 0
    flags = {"ok": "ok  ", "warn": "WARN", "fail": "FAIL"}
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = pool.map(lambda t: (t[0], t[1], *check(t[1])), targets)
        for label, url, status, detail in results:
            print(f"[{flags[status]}] {label:24s} {detail:35s} {url}")
            if status == "fail":
                failures += 1
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--category", choices=["small", "large"], help="only check one dataset category"
    )
    parser.add_argument(
        "--docs",
        nargs="*",
        metavar="FILE",
        help=f"also check doc links (default: {_DEFAULT_DOC})",
    )
    parser.add_argument(
        "--github",
        nargs="*",
        metavar="FILE",
        help=f"also check the github-catalogue YAML links (default: {_DEFAULT_GITHUB_YAML})",
    )
    args = parser.parse_args(argv)

    targets: list[tuple[str, str]] = []
    for name in sorted(DATASETS):
        spec = DATASETS[name]
        if args.category and spec.category != args.category:
            continue
        targets.append((name, spec.url))

    if args.docs is not None:
        doc_files = args.docs or [_DEFAULT_DOC]
        for doc in doc_files:
            for url in extract_doc_urls(doc):
                targets.append((Path(doc).stem, url))

    if args.github is not None:
        yaml_files = args.github or [_DEFAULT_GITHUB_YAML]
        for yml in yaml_files:
            for url in extract_yaml_urls(yml):
                targets.append((Path(yml).stem, url))

    print(f"Checking {len(targets)} URL(s)...\n")
    failures = _check_targets(targets)

    if failures:
        print(f"\n{failures} URL(s) failed.", file=sys.stderr)
        return 1
    print("\nAll URLs resolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
