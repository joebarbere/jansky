"""Tests for jansky.mastodon_reader -- the data layer (no network).

HTTP is mocked, so these run offline. The TUI is not exercised here (it lives behind the
optional ``tui`` extra and is smoke-tested separately).
"""

from __future__ import annotations

from datetime import datetime

import pytest

from jansky import mastodon_reader as mr


def test_strip_html():
    out = mr.strip_html("<p>Hello <b>world</b>&amp; the <a href='x'>VLA</a></p><p>line two</p>")
    assert "Hello world& the VLA" in out
    assert "line two" in out
    assert "<" not in out and ">" not in out


def test_parse_handles_reads_the_page():
    handles = mr.parse_handles()  # the real docs/mastodon.md
    assert "@tvern@mastodon.social" in handles
    assert "@hfalcke@mastodon.social" in handles
    assert "@HIprocessor@mastodon.social" in handles  # added this session
    # institutions are picked up too
    assert "@astron@mastodon.nl" in handles
    # de-duplicated and reasonably sized
    assert len(handles) == len(set(handles))
    assert len(handles) >= 8


class _FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_fetch_account_posts_mocked(monkeypatch):
    def fake_get(url, params=None, headers=None, timeout=None):
        if url.endswith("/accounts/lookup"):
            assert params["acct"] == "tvern"
            return _FakeResp({"id": "42", "display_name": "Tessa V."})
        if "/accounts/42/statuses" in url:
            return _FakeResp([
                {
                    "reblog": None,
                    "created_at": "2026-06-01T12:00:00.000Z",
                    "content": "<p>A new <b>EMU</b> radio map!</p>",
                    "url": "https://mastodon.social/@tvern/1",
                    "media_attachments": [
                        {"type": "image", "url": "https://img/1.png"},
                        {"type": "video", "url": "https://vid/1.mp4"},
                    ],
                },
                {
                    "reblog": {
                        "created_at": "2026-05-30T09:00:00.000Z",
                        "content": "<p>boosted thing</p>",
                        "url": "https://other/@x/2",
                        "media_attachments": [],
                    },
                    "created_at": "2026-05-31T09:00:00.000Z",
                },
            ])
        raise AssertionError(f"unexpected url {url}")

    monkeypatch.setattr(mr.requests, "get", fake_get)
    posts = mr.fetch_account_posts("@tvern@mastodon.social", limit=5)

    assert len(posts) == 2
    first = posts[0]
    assert first.author == "Tessa V."
    assert "EMU radio map" in first.text
    assert first.images == ["https://img/1.png"]  # video filtered out
    assert isinstance(first.created_at, datetime)
    assert posts[1].boosted is True
    assert posts[1].text == "boosted thing"


def test_gather_posts_skips_failures_and_sorts(monkeypatch):
    def fake_fetch(handle, per_account):
        if handle == "@bad@x.social":
            raise RuntimeError("boom")
        return [
            mr.Post("A", handle, mr._parse_dt("2026-01-01T00:00:00Z"), "old", "u1"),
            mr.Post("A", handle, mr._parse_dt("2026-09-01T00:00:00Z"), "new", "u2"),
        ]

    monkeypatch.setattr(mr, "fetch_account_posts", fake_fetch)
    errors = []
    posts = mr.gather_posts(
        ["@good@x.social", "@bad@x.social"], per_account=5,
        on_error=lambda h, e: errors.append(h),
    )
    assert [p.text for p in posts] == ["new", "old"]  # newest first
    assert errors == ["@bad@x.social"]


def test_run_tui_without_extra_raises(monkeypatch):
    # Simulate the TUI deps being absent -> a helpful SystemExit.
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name == "jansky._mastodon_tui":
            raise ImportError("textual", name="textual")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(SystemExit):
        mr.run_tui([])
