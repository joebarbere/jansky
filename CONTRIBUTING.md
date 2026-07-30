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

We **deliberately commit notebook outputs**. The MkDocs site renders them directly
(mkdocs-jupyter runs with `execute: false`), so the published figures come from what's
in git — and that is intentional: it keeps the site building reliably without executing
42 notebooks per deploy, and it preserves the **real-data figures** (pulsar fits, the LAB
HI spectrum, the Radio JOVE `.sps` waterfall, VLA visibilities) that need optional extras
and network to produce. So: **do not strip outputs.** The repo carries ~47 MB of them by
design.

If you change a notebook, **re-run it top-to-bottom and commit the refreshed outputs** so
the site stays in sync, and **strip any `stderr` stream outputs** (download bars, library
warnings) — keep only the clean stdout/figure outputs. Every notebook must run **fully
offline**: network or hardware sources degrade to synthetic/cached data (see
`src/jansky/data.py`).

The scheduled `notebooks.yml` workflow executes every notebook weekly to catch
helper/library drift. Optional local hooks live in `.pre-commit-config.yaml`
(`pip install pre-commit && pre-commit install`); the `nbstripout` hook there runs with
`--keep-output`, so it tidies metadata **without** removing the committed figures.

## Notebook code style — inline first

Community feedback on the course converged on one principle: **teaching code should read
as a stream of consciousness** — top to bottom, with the physics in the open — not routed
through layers of helper calls. The razor:

> **Inline the physics, wrap the plumbing.** If a wrapper's internals are *this chapter's*
> content, unroll it. If the reader would skim its internals (figure styling, seeding,
> data fetching, repetitive checking), wrap it. When in doubt, ask what the learner loses
> by not reading it.

Concretely:

- **New physics is written inline**, in flat NumPy: named intermediate variables, one
  concept per cell, a print or plot after every step. No `def` unless the chapter is about
  building that function; no nested call chains; no clever one-liners.
- **Helpers may be called for *earlier* chapters' physics** (abstraction already earned)
  and for plumbing (`plotting.use_jansky_style()`, `signals.rng`, `jansky.data` fetchers,
  `jansky.envelope.check`).
- **Every chapter ends by "promoting" its inline code**: a short cell asserting the inline
  result equals the packaged helper (`assert np.allclose(inline, packaged)`), then telling
  the reader the one-liner now has a name. New physics still lands in `src/jansky/` with a
  unit test — the package exists for later chapters and downstream research; the notebook
  just must not front it while teaching.

### The "Back of the envelope" section

Every chapter carries an estimation section right after **The physics**, before any
imports — four beats:

1. **The setup** (markdown): one concrete question with real numbers, answerable by
   dimensional reasoning alone. Decades matter, factors of two don't.
2. **Your estimate** (code): the given quantities as plain floats with units in comments,
   and one line left as `guess = None` for the reader to write.
3. **The check** (code): `jansky.envelope.check(guess, expected_log10=..., name=...,
   units=...)` — order-of-magnitude feedback that never raises and runs green with
   `None`, so CI and the reader coexist in the same cells. Pass the answer as its
   **base-10 logarithm** (4 decimal places), never as a plain `expected=` value: the
   check cell sits right under the learner cell, and a readable answer there spoils the
   estimate for anyone whose eye lands on it before committing.
4. **The reveal** (markdown `<details>`): the worked arithmetic, then **"where the
   envelope leaks"** — the effects the estimate ignored, each pointing at the part of the
   chapter that treats it properly. Optionally a **"turn the knob"** follow-up that reuses
   the reader's expression at a different scale.

Chapter 3 (Signals, Noise & the Radiometer Equation) is the reference implementation of
both patterns.

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
