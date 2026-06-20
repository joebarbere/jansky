"""Check the project's radio-astronomy data sources for anything new.

Two kinds of check, run against a small registry that mirrors the archives in
``docs/resources.md`` and the preprint feeds the field watches:

1. **arXiv feeds** — query the arXiv API for the most recent preprints in a
   category/keyword and report any whose IDs we haven't seen before. This is the
   reliable, genuinely useful "new research/data" signal.
2. **Page change-detection** — fetch an archive's landing/news page and hash its
   text; if the hash changed since last run, flag it for a manual look. (Generic,
   so it errs toward "go check" rather than parsing each archive's bespoke API.)

State (seen arXiv IDs + page hashes) is kept in a JSON file so each run reports
only what's new. Powers the ``dataset-watch`` skill.

Usage::

    uv run python scripts/dataset_watch.py            # check everything
    uv run python scripts/dataset_watch.py --list     # show the registry
    uv run python scripts/dataset_watch.py --reset     # forget all state
    uv run python scripts/dataset_watch.py --json      # machine-readable report
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

import requests

_UA = {"User-Agent": "jansky-dataset-watch (+https://github.com/joebarbere/jansky)"}
_STATE = Path(__file__).resolve().parents[1] / ".cache" / "dataset_watch.json"


@dataclass
class ArxivFeed:
    """An arXiv search to watch (new preprints = new IDs)."""

    name: str
    query: str  #: arXiv search_query, e.g. "cat:astro-ph.IM AND abs:radio"
    max_results: int = 15


@dataclass
class WatchPage:
    """An archive page to change-detect."""

    name: str
    url: str
    note: str = ""


# Mirrors the archives/feeds the project tracks (docs/resources.md, papers-timeline).
ARXIV_FEEDS = [
    ArxivFeed("arXiv astro-ph.IM (instrumentation)", "cat:astro-ph.IM AND abs:radio"),
    ArxivFeed("arXiv FRBs", 'abs:"fast radio burst"'),
    ArxivFeed("arXiv pulsar timing arrays", 'abs:"pulsar timing array"'),
]

WATCH_PAGES = [
    WatchPage("NRAO Science Data Archive", "https://data.nrao.edu/", "VLA/VLBA/ALMA-NA"),
    WatchPage("ALMA Science Archive", "https://almascience.org/aq/", "mm/submm"),
    WatchPage(
        "ATNF Pulsar Catalogue",
        "https://www.atnf.csiro.au/research/pulsar/psrcat/",
        "watch the version number",
    ),
    WatchPage("NASA LAMBDA", "https://lambda.gsfc.nasa.gov/product/", "CMB / foreground products"),
    WatchPage(
        "Radio JOVE Data Archive",
        "https://radiojove.net/archive.html",
        "observer SkyPipe (.spd) / SPS (.sps) data",
    ),
    WatchPage(
        "MASER Radio JOVE collection",
        "https://maser.obspm.fr/data/radiojove/",
        "PADC decametric / Radio JOVE",
    ),
]


@dataclass
class Report:
    new_papers: dict = field(default_factory=dict)  #: feed name -> list of {id,title,link}
    changed_pages: list = field(default_factory=list)  #: list of {name,url,note}
    errors: list = field(default_factory=list)  #: list of {source, error}


def query_arxiv(feed: ArxivFeed, timeout: float = 20.0) -> list[dict]:
    """Return recent arXiv entries for a feed, newest first."""
    resp = requests.get(
        "http://export.arxiv.org/api/query",
        params={
            "search_query": feed.query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": feed.max_results,
        },
        headers=_UA,
        timeout=timeout,
    )
    resp.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(resp.text)
    out = []
    for entry in root.findall("a:entry", ns):
        arxiv_id = (entry.findtext("a:id", default="", namespaces=ns) or "").rsplit("/", 1)[-1]
        title = re.sub(r"\s+", " ", entry.findtext("a:title", default="", namespaces=ns)).strip()
        out.append({"id": arxiv_id, "title": title, "link": f"https://arxiv.org/abs/{arxiv_id}"})
    return out


def page_hash(url: str, timeout: float = 20.0) -> str:
    """SHA-256 of a page's text (used for change-detection)."""
    resp = requests.get(url, headers=_UA, timeout=timeout)
    resp.raise_for_status()
    return hashlib.sha256(resp.text.encode("utf-8", "ignore")).hexdigest()


def load_state(path: Path = _STATE) -> dict:
    if Path(path).exists():
        return json.loads(Path(path).read_text())
    return {"arxiv_seen": {}, "page_hashes": {}}


def save_state(state: dict, path: Path = _STATE) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2))


def check(
    state: dict,
    arxiv_feeds: list[ArxivFeed] = ARXIV_FEEDS,
    watch_pages: list[WatchPage] = WATCH_PAGES,
) -> Report:
    """Run all checks against ``state`` (mutated in place) and return a :class:`Report`."""
    report = Report()
    seen = state.setdefault("arxiv_seen", {})
    hashes = state.setdefault("page_hashes", {})

    for feed in arxiv_feeds:
        try:
            entries = query_arxiv(feed)
        except Exception as exc:  # noqa: BLE001
            report.errors.append({"source": feed.name, "error": str(exc)})
            continue
        known = set(seen.get(feed.name, []))
        fresh = [e for e in entries if e["id"] not in known]
        if fresh and known:  # only report as "new" once we have a baseline
            report.new_papers[feed.name] = fresh
        seen[feed.name] = [e["id"] for e in entries]

    for page in watch_pages:
        try:
            digest = page_hash(page.url)
        except Exception as exc:  # noqa: BLE001
            report.errors.append({"source": page.name, "error": str(exc)})
            continue
        if page.name in hashes and hashes[page.name] != digest:
            report.changed_pages.append({"name": page.name, "url": page.url, "note": page.note})
        hashes[page.name] = digest

    return report


def _print_report(report: Report) -> None:
    if report.new_papers:
        print("\n\033[1mNew preprints:\033[0m")
        for feed, entries in report.new_papers.items():
            print(f"  {feed}:")
            for e in entries:
                print(f"    • {e['title']}\n      {e['link']}")
    if report.changed_pages:
        print("\n\033[1mArchive pages that changed (check manually):\033[0m")
        for p in report.changed_pages:
            print(f"  • {p['name']} — {p['note']}\n    {p['url']}")
    if report.errors:
        print("\n\033[2mUnreachable this run:\033[0m", file=sys.stderr)
        for e in report.errors:
            print(f"  - {e['source']}: {e['error']}", file=sys.stderr)
    if not (report.new_papers or report.changed_pages):
        print("Nothing new since the last check (or this is the first run — baseline saved).")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Watch radio-astronomy data sources for new data.")
    parser.add_argument("--state", default=str(_STATE), help="state file path")
    parser.add_argument("--list", action="store_true", help="list the watched sources and exit")
    parser.add_argument("--reset", action="store_true", help="forget all state before checking")
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    args = parser.parse_args(argv)

    if args.list:
        print("arXiv feeds:")
        for f in ARXIV_FEEDS:
            print(f"  - {f.name}: {f.query}")
        print("Watched archive pages:")
        for p in WATCH_PAGES:
            print(f"  - {p.name}: {p.url}")
        return 0

    state = {"arxiv_seen": {}, "page_hashes": {}} if args.reset else load_state(Path(args.state))
    report = check(state)
    save_state(state, Path(args.state))

    if args.json:
        print(
            json.dumps(
                {
                    "new_papers": report.new_papers,
                    "changed_pages": report.changed_pages,
                    "errors": report.errors,
                },
                indent=2,
            )
        )
    else:
        _print_report(report)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
