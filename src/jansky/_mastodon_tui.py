"""Textual terminal UI for :mod:`jansky.mastodon_reader` (the ``tui`` extra).

A two-pane reader: a scrollable list of posts on the left, a detail pane with the full text and
**inline images** on the right. Images render through whatever terminal graphics protocol is
available (kitty / iTerm2 / sixel) via ``textual-image``, falling back to Unicode half-blocks.

This module is imported lazily by :func:`jansky.mastodon_reader.run_tui`, so the base course has
no dependency on ``textual``.
"""

from __future__ import annotations

import io
import webbrowser

import requests
from rich.markup import escape
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Label, ListItem, ListView, LoadingIndicator, Static

from jansky.mastodon_reader import Post, gather_posts

_USER_AGENT = "jansky-mastodon-reader (+https://github.com/joebarbere/jansky)"


class PostItem(ListItem):
    """A list row carrying its :class:`Post`."""

    def __init__(self, post: Post) -> None:
        when = post.created_at.astimezone().strftime("%b %d %H:%M")
        boost = " \U0001f501" if post.boosted else ""
        camera = " \U0001f5bc" if post.images else ""
        first_line = (post.text.splitlines() or [""])[0]
        super().__init__(
            Label(
                f"[b]{escape(post.author)}[/b]{boost}{camera}\n"
                f"[dim]{when}[/dim]  {escape(first_line[:60])}"
            )
        )
        self.post = post


class MastodonApp(App):
    """The reader application."""

    CSS = """
    #body { height: 1fr; }
    #list { width: 42%; border-right: solid $accent; }
    #detail { width: 1fr; padding: 1 2; }
    #detail Static { margin-bottom: 1; }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("o", "open", "Open in browser"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(
        self,
        handles: list[str] | None = None,
        per_account: int = 5,
        *,
        query: str | None = None,
        accounts: list[str] | None = None,
    ) -> None:
        super().__init__()
        self._handles = handles
        self._per_account = per_account
        self._query = query
        self._accounts = accounts
        self._image_token = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="body"):
            yield ListView(id="list")
            with VerticalScroll(id="detail"):
                yield LoadingIndicator()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "jansky — Radio Astronomy on Mastodon"
        self._load_posts()

    # ---- data loading (worker thread) ------------------------------------ #
    @work(thread=True, exclusive=True)
    def _load_posts(self) -> None:
        posts = gather_posts(
            self._handles,
            self._per_account,
            query=self._query,
            accounts=self._accounts,
            on_error=lambda h, e: None,
        )
        self.call_from_thread(self._populate, posts)

    def _populate(self, posts: list[Post]) -> None:
        listview = self.query_one("#list", ListView)
        listview.clear()
        detail = self.query_one("#detail", VerticalScroll)
        detail.remove_children()
        if not posts:
            detail.mount(Static("No posts (network blocked, or all accounts unavailable)."))
            self.sub_title = "0 posts"
            return
        for post in posts:
            listview.append(PostItem(post))
        self.sub_title = f"{len(posts)} posts from {len({p.handle for p in posts})} accounts"
        listview.index = 0
        listview.focus()
        self._show(posts[0])

    # ---- selection -> detail pane ---------------------------------------- #
    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if isinstance(event.item, PostItem):
            self._show(event.item.post)

    def _show(self, post: Post) -> None:
        self._current = post
        detail = self.query_one("#detail", VerticalScroll)
        detail.remove_children()
        when = post.created_at.astimezone().strftime("%Y-%m-%d %H:%M")
        boost = "  \U0001f501 boosted" if post.boosted else ""
        detail.mount(
            Static(
                f"[b]{escape(post.author)}[/b]  [dim]{escape(post.handle)}[/dim]\n[dim]{when}{boost}[/dim]"
            )
        )
        detail.mount(Static(post.text or "(no text)", markup=False))
        if post.url:
            detail.mount(Static(f"{post.url}   (press o to open)", markup=False))
        self._image_token += 1
        if post.images:
            detail.mount(Static(f"[dim]loading {len(post.images)} image(s)…[/dim]"))
            self._load_images(post.images, self._image_token)

    @work(thread=True)
    def _load_images(self, urls: list[str], token: int) -> None:
        for url in urls:
            try:
                resp = requests.get(url, timeout=15, headers={"User-Agent": _USER_AGENT})
                resp.raise_for_status()
                data = resp.content
            except Exception:  # noqa: BLE001
                data = None
            self.call_from_thread(self._mount_image, data, url, token)

    def _mount_image(self, data: bytes | None, url: str, token: int) -> None:
        if token != self._image_token:
            return  # the user moved on to another post
        detail = self.query_one("#detail", VerticalScroll)
        if data is None:
            detail.mount(Static(f"\U0001f5bc could not load: {url}", markup=False))
            return
        try:
            from PIL import Image as PILImage
            from textual_image.widget import Image as ImageWidget

            pil = PILImage.open(io.BytesIO(data))
            pil.thumbnail((900, 700))
            detail.mount(ImageWidget(pil))
        except Exception:  # noqa: BLE001 - protocol/lib issues -> show the link instead
            detail.mount(Static(f"\U0001f5bc {url}", markup=False))

    # ---- actions --------------------------------------------------------- #
    def action_open(self) -> None:
        post = getattr(self, "_current", None)
        if post is not None and post.url:
            webbrowser.open(post.url)

    def action_refresh(self) -> None:
        self.sub_title = "refreshing…"
        self._load_posts()
