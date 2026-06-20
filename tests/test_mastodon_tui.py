"""Headless smoke test for the Mastodon TUI.

Skipped unless the optional ``tui`` extra is installed (textual / textual-image / pillow).
Run with: ``uv run --extra tui pytest tests/test_mastodon_tui.py``.
"""

from __future__ import annotations

import asyncio
import io
from datetime import datetime, timezone

import pytest

pytest.importorskip("textual")
pytest.importorskip("textual_image")
PIL = pytest.importorskip("PIL.Image")

from jansky import mastodon_reader as mr  # noqa: E402


def _tiny_png() -> bytes:
    buf = io.BytesIO()
    PIL.new("RGB", (8, 8), (128, 0, 200)).save(buf, format="PNG")
    return buf.getvalue()


def test_tui_populates_and_shows_detail(monkeypatch):
    from textual.containers import VerticalScroll
    from textual.widgets import ListView

    from jansky import _mastodon_tui as tui

    posts = [
        mr.Post("ESO", "@esoastronomy@mastodon.social",
                datetime(2026, 6, 1, tzinfo=timezone.utc),
                "A radio map of the sky", "https://m/1", images=["https://img/a.png"]),
        mr.Post("ASTRON", "@astron@mastodon.nl",
                datetime(2026, 5, 1, tzinfo=timezone.utc),
                "LOFAR results", "https://m/2", images=[]),
    ]
    monkeypatch.setattr(tui, "gather_posts", lambda *a, **k: posts)

    class _Resp:
        content = _tiny_png()

        def raise_for_status(self):
            pass

    monkeypatch.setattr(tui.requests, "get", lambda *a, **k: _Resp())

    async def _run():
        app = tui.MastodonApp(handles=["@x@y.social"], per_account=2)
        async with app.run_test() as pilot:
            for _ in range(8):  # let the threaded fetch + populate workers run
                await pilot.pause(0.05)
            listview = app.query_one("#list", ListView)
            assert len(listview) == 2
            detail = app.query_one("#detail", VerticalScroll)
            assert len(detail.children) >= 2  # author + text statics
            for _ in range(8):  # let the image worker mount its widget
                await pilot.pause(0.05)
            assert app.is_running

    asyncio.run(_run())
