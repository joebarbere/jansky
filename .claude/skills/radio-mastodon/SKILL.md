---
name: radio-mastodon
description: Read or search recent public Mastodon posts from the radio astronomers and observatories listed in docs/mastodon.md. Use when the user wants to see what radio astronomers are posting, find community posts about a topic (e.g. FRBs, the VLA, an event), or browse the feed — optionally with inline images.
---

# Radio astronomy on Mastodon

The project ships a reader that pulls the listed accounts' recent **public** posts straight from
Mastodon's API — no login or token. The handles come from `docs/mastodon.md`, so the feed stays
in sync with that list.

## How to use it

Run the reader with the right flags for the request, then **summarise** the results for the user
(group by author or topic, keep the permalinks):

```bash
# everything, newest first
uv run python -m jansky.mastodon_reader --no-tui --limit 5

# posts mentioning a topic (case-insensitive substring)
uv run python -m jansky.mastodon_reader --no-tui --search "fast radio burst"

# restrict to particular accounts (repeatable substring match on the handle)
uv run python -m jansky.mastodon_reader --no-tui --account falcke --account astron

# machine-readable, when you need to process the posts
uv run python -m jansky.mastodon_reader --json --limit 3
```

`--list-handles` shows which accounts are queried.

## Reporting

- Lead with the most relevant/recent posts; include each post's author, a one-line gist, and the
  permalink. Note 🔁 boosts and 🖼 image counts.
- If the user wants to **view images**, tell them to run the terminal UI themselves — it renders
  images inline (kitty/iTerm2/sixel terminals):
  `uv sync --extra tui && uv run python -m jansky.mastodon_reader` (or `make mastodon`). You
  cannot show terminal-graphics images in this chat; surface the image URLs instead.
- Accounts that error are skipped automatically; mention if a notable one was unavailable.
- To add/correct accounts, edit `docs/mastodon.md` (the reader re-reads it each run).
