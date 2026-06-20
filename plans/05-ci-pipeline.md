# Plan 05 — Continuous integration pipeline 📋 Proposed

> Flagged by **engineering (#1)** and **science-rigor (#1)** — the strongest cross-agent
> signal. Scope: small–medium.

## Context

There is no `.github/` at all. Nothing enforces lint, tests, the notebook smoke-tests, or the
docs build on a change, and only **3 of 36 notebooks** are ever executed (`make test-notebooks`).
The other 33 — every physics and research chapter — import `src/jansky` and can silently rot when
astropy/astroquery/PINT drift or an archive URL changes. The course's headline promise ("complete
the entire course offline") is currently verified only by hand.

## Deliverables

- **`.github/workflows/ci.yml`** — on pull requests and pushes to `main`:
  - `astral-sh/setup-uv@v5` with `enable-cache: true`;
  - `uv run ruff check` + `uv run ruff format --check`;
  - `uv run pytest` (+ the `tui` extra job so the headless Textual test runs);
  - `uv run pytest --nbmake` on the **Part I** notebooks (fast smoke test);
  - `uv run mkdocs build --strict`;
  - matrix over Python **3.10 and 3.12** to honour `requires-python = ">=3.10,<3.13"`.
- **`.github/workflows/notebooks.yml`** — `on: schedule` (weekly) + `workflow_dispatch`:
  `uv run pytest --nbmake notebooks/*.ipynb` with the offline/synthetic fallbacks forced on, a
  per-notebook `--nbmake-timeout`, and network/hardware chapters skipped via a pytest marker or
  cell tag. Keeps the full run off the PR critical path while still catching helper regressions.
- A status badge in `README.md`.

## Approach

- The four PR checks already exist as Makefile targets — wire them up.
- For the scheduled full run, lean on the "degrades to synthetic data" design; tag the handful of
  cells that genuinely need network so they skip cleanly offline.

## Verification

- A trial PR shows all checks running and green; deliberately breaking a helper or a notebook cell
  makes CI fail. The matrix confirms the advertised Python range actually works.
