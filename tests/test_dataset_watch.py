"""Tests for scripts/dataset_watch.py (loaded from file; mocked, no network)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_PATH = Path(__file__).resolve().parents[1] / "scripts" / "dataset_watch.py"
_spec = importlib.util.spec_from_file_location("dataset_watch", _PATH)
dw = importlib.util.module_from_spec(_spec)
sys.modules["dataset_watch"] = dw  # so dataclasses can resolve the module's namespace
_spec.loader.exec_module(dw)


def test_arxiv_new_reported_only_after_baseline(monkeypatch):
    feed = dw.ArxivFeed("test", "cat:astro-ph.IM")
    calls = {"n": 0}

    def fake_query(f, timeout=20.0):
        calls["n"] += 1
        if calls["n"] == 1:
            return [{"id": "2601.001", "title": "A", "link": "L1"}]
        return [
            {"id": "2601.002", "title": "B (new)", "link": "L2"},
            {"id": "2601.001", "title": "A", "link": "L1"},
        ]

    monkeypatch.setattr(dw, "query_arxiv", fake_query)
    monkeypatch.setattr(dw, "page_hash", lambda url, timeout=20.0: "h")

    state = {"arxiv_seen": {}, "page_hashes": {}}
    r1 = dw.check(state, arxiv_feeds=[feed], watch_pages=[])
    assert r1.new_papers == {}  # first run = baseline, nothing flagged
    r2 = dw.check(state, arxiv_feeds=[feed], watch_pages=[])
    assert "test" in r2.new_papers
    assert [e["id"] for e in r2.new_papers["test"]] == ["2601.002"]


def test_page_change_detection(monkeypatch):
    page = dw.WatchPage("Archive", "https://x/")
    seq = iter(["hashA", "hashA", "hashB"])
    monkeypatch.setattr(dw, "page_hash", lambda url, timeout=20.0: next(seq))
    monkeypatch.setattr(dw, "query_arxiv", lambda f, timeout=20.0: [])

    state = {"arxiv_seen": {}, "page_hashes": {}}
    assert dw.check(state, arxiv_feeds=[], watch_pages=[page]).changed_pages == []  # baseline
    assert dw.check(state, arxiv_feeds=[], watch_pages=[page]).changed_pages == []  # unchanged
    changed = dw.check(state, arxiv_feeds=[], watch_pages=[page]).changed_pages
    assert changed and changed[0]["name"] == "Archive"


def test_errors_collected_not_raised(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("network down")

    monkeypatch.setattr(dw, "query_arxiv", boom)
    monkeypatch.setattr(dw, "page_hash", boom)
    state = {"arxiv_seen": {}, "page_hashes": {}}
    report = dw.check(
        state, arxiv_feeds=[dw.ArxivFeed("f", "q")], watch_pages=[dw.WatchPage("p", "u")]
    )
    assert len(report.errors) == 2
    assert report.new_papers == {} and report.changed_pages == []


def test_state_roundtrip(tmp_path):
    state = {"arxiv_seen": {"f": ["1", "2"]}, "page_hashes": {"p": "abc"}}
    path = tmp_path / "state.json"
    dw.save_state(state, path)
    assert dw.load_state(path) == state


def test_registry_includes_radiojove(monkeypatch):
    names = [p.name for p in dw.WATCH_PAGES]
    assert any("Radio JOVE" in n for n in names)  # SkyPipe data source is watched


def test_query_arxiv_parses_atom(monkeypatch):
    atom = """<?xml version='1.0'?>
    <feed xmlns='http://www.w3.org/2005/Atom'>
      <entry><id>http://arxiv.org/abs/2601.12345v1</id><title>A  radio
      burst</title></entry>
    </feed>"""

    class _Resp:
        text = atom

        def raise_for_status(self):
            pass

    monkeypatch.setattr(dw.requests, "get", lambda *a, **k: _Resp())
    out = dw.query_arxiv(dw.ArxivFeed("t", "q"))
    assert out == [
        {
            "id": "2601.12345v1",
            "title": "A radio burst",
            "link": "https://arxiv.org/abs/2601.12345v1",
        }
    ]
