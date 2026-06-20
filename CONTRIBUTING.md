# Contributing to jansky

Thanks for helping improve this radio-astronomy course! Whether you're fixing a
typo, tightening the physics, or authoring a whole chapter, this guide gets you
set up and shows you the checks the CI enforces.

## Set up the environment

The project is managed with [uv](https://docs.astral.sh/uv/) and pinned to
Python 3.12 (CASA tooling supports only ≤3.12):

```bash
uv sync                      # core + dev toolchain
uv sync --extra tui          # add an optional extra (tui, pulsar, sdr, seti, ...)
uv run python -c "import jansky"   # sanity check
```

Everything below runs through `uv run`, so you never need to activate a venv by
hand. There's a `Makefile` of shortcuts — `make help` lists them.

## The checks (run these before opening a PR)

CI runs all of these on every PR, across Python 3.10 and 3.12. To reproduce locally:

| Command | What it checks |
|---|---|
| `make lint`      | `ruff check` — lint |
| `make fmt`       | `ruff format` — auto-format `src/` and `tests/` |
| `make typecheck` | `mypy` over `src/jansky` |
| `make test`      | `pytest` unit tests |
| `make cov`       | unit tests with the coverage floor (currently 85%) |
| `make docs`      | `mkdocs build --strict` — fails on any broken internal link/anchor |
| `make test-notebooks` | executes the Part I notebooks via `nbmake` |

A one-liner before pushing: `make lint typecheck cov docs`.

## Notebook policy

The MkDocs site renders the **committed notebook outputs** (mkdocs-jupyter runs
with `execute: false`), so the published figures come from what's in git. If you
change a notebook, **re-run it top-to-bottom and commit the refreshed outputs**
so the site stays in sync. Every notebook must run **fully offline** — network or
hardware sources degrade to synthetic/cached data (see `src/jansky/data.py`).

The scheduled `notebooks.yml` workflow executes all 36 notebooks weekly to catch
helper/library drift.

## Authoring a new chapter

Chapters follow a consistent standard captured in
[`.claude/agents/notebook-author.md`](.claude/agents/notebook-author.md): prose +
LaTeX + runnable cells + plots, citing the seminal paper(s), leaning on the
`jansky` helper package, and adding a `docs/chapters` framing page plus a `nav`
entry in `mkdocs.yml`. New physics/constants belong in `src/jansky/` (with a unit
test), not hard-coded in a cell — see `src/jansky/constants.py`.

## The `.claude/` helpers

This repo ships reusable Claude Code **skills** (`.claude/skills/`) and **agents**
(`.claude/agents/`) for research tasks — searching Mastodon for radio astronomers,
watching the data sources for new datasets, finding papers, and reviewing chapters
for scientific accuracy. They're optional, but handy if you use Claude Code.

## Submitting

Open a PR against `main` with a clear description. Keep changes focused; if you're
proposing a larger piece of work, the `plans/` directory is where course expansions
are tracked. Be kind, cite your sources, and have fun. 📡

For keeping the course current (new telescopes, papers, and link rot), see
[`MAINTAINING.md`](MAINTAINING.md).
