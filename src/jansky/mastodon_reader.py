"""Read recent public posts from the radio astronomers listed in ``docs/mastodon.md``.

A small companion tool to the [Radio Astronomy on Mastodon](../docs/mastodon.md) page: it
parses the handles from that page, fetches each account's recent **public** posts through
Mastodon's unauthenticated API (no login or token required), and shows them either as plain
text or in a terminal UI with inline images.

Usage
-----
Plain text (works anywhere, no extra deps)::

    uv run python -m jansky.mastodon_reader --no-tui --limit 3

The terminal UI with image viewing (needs the optional extra ``uv sync --extra tui``)::

    uv run python -m jansky.mastodon_reader

Images render inline in terminals that support the kitty, iTerm2, or sixel graphics protocols
(kitty, WezTerm, iTerm2, Konsole, foot, …); elsewhere they fall back to Unicode half-blocks.

The data layer (:func:`parse_handles`, :func:`fetch_account_posts`, :func:`gather_posts`) only
needs ``requests`` and is unit-tested; the TUI imports ``textual``/``textual-image`` lazily.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import requests

__all__ = [
    "Post",
    "strip_html",
    "parse_handles",
    "fetch_account_posts",
    "gather_posts",
    "run_tui",
]

#: Default location of the Mastodon page (relative to the repo root).
MASTODON_MD = Path(__file__).resolve().parents[2] / "docs" / "mastodon.md"

_USER_AGENT = "jansky-mastodon-reader (+https://github.com/joebarbere/jansky)"
# Handles look like @user@instance.tld; instance has at least one dot.
_HANDLE_RE = re.compile(r"@([A-Za-z0-9_]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")


@dataclass
class Post:
    """One public Mastodon post (status)."""

    author: str  #: display name (falls back to the username)
    handle: str  #: ``@user@instance``
    created_at: datetime  #: timezone-aware
    text: str  #: HTML stripped to plain text
    url: str  #: permalink
    images: list[str] = field(default_factory=list)  #: image URLs (media attachments)
    boosted: bool = False  #: True if this was a boost/reblog


class _HTMLStripper(HTMLParser):
    """Turn Mastodon's HTML post content into readable plain text."""

    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "p"):
            self._parts.append("\n")

    def handle_data(self, data):
        self._parts.append(data)

    def text(self) -> str:
        out = "".join(self._parts)
        return re.sub(r"\n{3,}", "\n\n", out).strip()


def strip_html(content: str) -> str:
    """Convert a Mastodon status's HTML ``content`` to plain text."""
    parser = _HTMLStripper()
    parser.feed(html.unescape(content or ""))
    return parser.text()


def _parse_dt(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return datetime.now(timezone.utc)


def parse_handles(md_path: str | Path = MASTODON_MD) -> list[str]:
    """Extract the unique ``@user@instance`` handles listed in the Mastodon page.

    Picks up both the institution and astronomer tables. Order-preserving and de-duplicated.
    """
    text = Path(md_path).read_text(encoding="utf-8")
    seen: list[str] = []
    for m in _HANDLE_RE.finditer(text):
        handle = f"@{m.group(1)}@{m.group(2)}"
        if handle not in seen:
            seen.append(handle)
    return seen


def fetch_account_posts(handle: str, limit: int = 5, timeout: float = 15.0) -> list[Post]:
    """Fetch an account's recent public posts via the unauthenticated Mastodon API.

    Looks the account up on its home instance, then reads its public statuses. Boosts are
    unwrapped to the original post (and flagged). Raises ``requests`` errors on failure (the
    caller in :func:`gather_posts` catches and skips).

    Parameters
    ----------
    handle
        ``@user@instance`` (a leading ``@`` is optional).
    limit
        Maximum number of posts to return.
    timeout
        Per-request timeout in seconds.
    """
    user, instance = handle.lstrip("@").split("@", 1)
    base = f"https://{instance}"
    headers = {"User-Agent": _USER_AGENT, "Accept": "application/json"}

    lookup = requests.get(
        f"{base}/api/v1/accounts/lookup",
        params={"acct": user},
        headers=headers,
        timeout=timeout,
    )
    lookup.raise_for_status()
    account = lookup.json()
    account_id = account["id"]
    display = account.get("display_name") or user

    resp = requests.get(
        f"{base}/api/v1/accounts/{account_id}/statuses",
        params={"limit": limit, "exclude_replies": "true"},
        headers=headers,
        timeout=timeout,
    )
    resp.raise_for_status()

    posts: list[Post] = []
    for status in resp.json():
        boosted = status.get("reblog") is not None
        source = status["reblog"] if boosted else status
        images = [
            m["url"]
            for m in source.get("media_attachments", [])
            if m.get("type") == "image" and m.get("url")
        ]
        posts.append(
            Post(
                author=display,
                handle=handle,
                created_at=_parse_dt(source.get("created_at", "")),
                text=strip_html(source.get("content", "")),
                url=source.get("url", ""),
                images=images,
                boosted=boosted,
            )
        )
    return posts


def gather_posts(
    handles: list[str] | None = None,
    per_account: int = 5,
    *,
    md_path: str | Path = MASTODON_MD,
    query: str | None = None,
    accounts: list[str] | None = None,
    on_error=None,
) -> list[Post]:
    """Fetch posts from every handle and return them newest-first.

    Accounts that fail (network error, blocked API, unknown user) are skipped; ``on_error`` is
    called with ``(handle, exception)`` if provided, otherwise a note is printed to stderr.

    Parameters
    ----------
    query
        If given, keep only posts whose text contains it (case-insensitive).
    accounts
        If given, restrict to handles that contain any of these substrings
        (case-insensitive) — e.g. ``["falcke", "astron"]``.
    """
    handles = handles if handles is not None else parse_handles(md_path)
    if accounts:
        needles = [a.lower() for a in accounts]
        handles = [h for h in handles if any(n in h.lower() for n in needles)]

    all_posts: list[Post] = []
    for handle in handles:
        try:
            all_posts.extend(fetch_account_posts(handle, per_account))
        except Exception as exc:  # noqa: BLE001 - any account may fail; keep going
            if on_error is not None:
                on_error(handle, exc)
            else:
                print(f"[skip] {handle}: {exc}", file=sys.stderr)

    if query:
        q = query.lower()
        all_posts = [p for p in all_posts if q in p.text.lower()]
    all_posts.sort(key=lambda p: p.created_at, reverse=True)
    return all_posts


def _print_posts(posts: list[Post]) -> None:
    """Plain-text rendering (the ``--no-tui`` path)."""
    if not posts:
        print("No posts fetched (network blocked, or all accounts unavailable).")
        return
    for post in posts:
        when = post.created_at.astimezone().strftime("%Y-%m-%d %H:%M")
        boost = " \U0001f501 boosted" if post.boosted else ""
        print(f"\n\033[1m{post.author}\033[0m  {post.handle}  ·  {when}{boost}")
        print(post.text or "(no text)")
        for url in post.images:
            print(f"  \U0001f5bc  {url}")
        if post.url:
            print(f"  \U0001f517 {post.url}")


def run_tui(
    handles: list[str] | None = None,
    per_account: int = 5,
    *,
    query: str | None = None,
    accounts: list[str] | None = None,
) -> None:
    """Launch the terminal UI (requires the ``tui`` extra). Imports textual lazily."""
    try:
        from jansky._mastodon_tui import MastodonApp
    except ImportError as exc:
        raise SystemExit(
            "The TUI needs the optional extra. Install it with:\n"
            "    uv sync --extra tui\n"
            f"(missing: {exc.name})"
        ) from exc
    MastodonApp(handles=handles, per_account=per_account, query=query, accounts=accounts).run()


def _posts_to_json(posts: list[Post]) -> str:
    import json

    return json.dumps(
        [
            {
                "author": p.author,
                "handle": p.handle,
                "created_at": p.created_at.isoformat(),
                "text": p.text,
                "url": p.url,
                "images": p.images,
                "boosted": p.boosted,
            }
            for p in posts
        ],
        indent=2,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read recent posts from the radio astronomers in docs/mastodon.md.",
    )
    parser.add_argument("--no-tui", action="store_true", help="print posts instead of the TUI")
    parser.add_argument("--limit", type=int, default=5, help="posts per account (default 5)")
    parser.add_argument("--search", metavar="TERM", help="keep only posts containing TERM")
    parser.add_argument(
        "--account",
        action="append",
        metavar="SUBSTR",
        help="restrict to handles matching SUBSTR (repeatable)",
    )
    parser.add_argument(
        "--json", action="store_true", help="print posts as JSON (implies --no-tui)"
    )
    parser.add_argument(
        "--list-handles", action="store_true", help="just list the handles and exit"
    )
    parser.add_argument("--md", default=str(MASTODON_MD), help="path to mastodon.md")
    args = parser.parse_args(argv)

    if args.list_handles:
        for handle in parse_handles(args.md):
            print(handle)
        return 0

    handles = parse_handles(args.md)
    if args.no_tui or args.json:
        posts = gather_posts(
            handles,
            args.limit,
            md_path=args.md,
            query=args.search,
            accounts=args.account,
        )
        if args.json:
            print(_posts_to_json(posts))
        else:
            _print_posts(posts)
        return 0
    run_tui(handles, args.limit, query=args.search, accounts=args.account)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
