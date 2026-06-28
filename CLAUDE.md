# jansky — guide for Claude

**What this is.** A hands-on **radio-astronomy course in Python** — executable Jupyter notebooks
(prose + physics + runnable code + plots, each chapter citing the seminal papers), a tested helper
package `jansky` (`src/jansky/`), and an MkDocs documentation site. Named after Karl Jansky. Read
online: <https://joebarbere.github.io/jansky/>. `uv`-managed, pinned to Python 3.12.

## The research sibling (each repo should point at the other)

**[`jansky-research`](https://github.com/joebarbere/jansky-research)** (checked out at
`../jansky-research`) is a separate repo that **depends on this course as a library** and does
original, reproducible amateur research as tested "slices" → honest AASTeX papers. It reuses this
repo's helpers (`jansky.transients`, `jansky.timing`, `jansky.seti`, `jansky.data`, …) and Claude
agents/skills. If a task is about *doing research* (a new analysis, a paper, a data slice), it likely
belongs in `../jansky-research`, not here. A new session in either repo: read this file (or the
research repo's `CLAUDE.md`) to learn the other exists.

## Working rules

- **Branch before committing — never commit on `main`.** Open a PR.
- Before a PR, run the checks `CONTRIBUTING.md` lists (CI enforces them on Python 3.10 + 3.12):
  `make lint` (ruff), `make typecheck` (mypy), `make test` / `make cov` (coverage floor),
  `make docs` (strict MkDocs build), and `make test-notebooks` for touched Part-I notebooks.
- Notebooks are the course; the `jansky` package is the tested helpers behind them. Keep new physics
  cited (add to `docs/references.md` / `docs/papers-timeline.md`).
- See `CONTRIBUTING.md` (contributor checks) and `MAINTAINING.md` (release/maintenance) for specifics.

## Layout

`src/jansky/` (helper package) · `notebooks/` (the chapters) · `docs/` (MkDocs site: references,
papers-timeline, telescopes, glossary, projects, …) · `tests/` · `.claude/` (agents: archive-scout,
radio-research-assistant, science-reviewer, notebook-author; skills: find-radio-papers,
radio-source-lookup, dataset-watch, radio-mastodon) · `Makefile` (`make help`).

## Claude agents/skills shared with the research repo

`archive-scout`, `radio-research-assistant`, `science-reviewer` and the `find-radio-papers` /
`radio-source-lookup` skills are also used in `../jansky-research` (copied there, since skills aren't
auto-discovered across repos). If you change one here meaningfully, mirror it there. `dataset-watch`
and `radio-mastodon` are course-specific (they read `docs/mastodon.md` etc.) and stay here only.
