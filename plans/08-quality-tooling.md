# Plan 08 — Quality tooling: types, coverage, contributing, link-checking 📋 Proposed

> Flagged by **engineering (#5, #6)**, with the link-checker also raised by **research (#6)** and
> **archive (#4)**. Scope: medium.

## Context

The package is lean and ruff-clean, but 16 of 18 `src/jansky` modules are tested, there's no type
checking, no coverage measurement, no contributor onboarding doc, no dependency automation, and no
guard against the inevitable rot in ~490 external doc links.

## Deliverables

- **Type checking** — add `mypy` (or `pyright`) to the `dev` group + a `[tool.mypy]` section scoped
  to `src/jansky`; run it in CI ([Plan 05](05-ci-pipeline.md)). Add return-type hints where missing.
- **Coverage** — `pytest-cov` with `--cov=jansky` and a floor; write tests for the two untested
  modules: `plotting.py` and `_mastodon_tui.py` (the TUI test already covers the latter headlessly —
  extend it / measure).
- **`CONTRIBUTING.md`** — env via `uv sync`, `make lint test docs`, the notebook-output policy
  ([Plan 07](07-notebook-hygiene.md)), how the `.claude/` skills & agents help, and the chapter
  authoring standard (`.claude/agents/notebook-author.md`).
- **`.github/dependabot.yml`** — `pip`/`uv` and `github-actions` ecosystems, weekly.
- **Docs link-checker** — a `lychee` (or `mkdocs` link plugin) CI job over the docs' external URLs;
  this operationalises the "stay current" goal shared with [Plan 11](11-ska-era-refresh.md).

## Verification

- `mypy src/jansky` is clean (or has a documented baseline); coverage report generates and the floor
  holds; CONTRIBUTING renders; Dependabot opens its first PRs; the link-checker reports (and we fix)
  any dead links.
