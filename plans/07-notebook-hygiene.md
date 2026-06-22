# Plan 07 — Notebook output hygiene 📋 Proposed

> Flagged by **engineering (#2)**. Scope: medium. (Pairs with the docs-publishing
> work, which is already delivered.)

## Context

32 of 36 notebooks ship executed outputs in git (359 output-bearing cells); the largest single
notebook is **~3.6 MB** and the top five total ~13 MB. This bloats clones, makes diffs unreadable,
and causes merge conflicts on every re-run. But the published site currently *depends* on those
committed outputs (`mkdocs-jupyter: execute: false`), so stripping must be paired with a rendering
strategy.

## Deliverables

- **`.pre-commit-config.yaml`** with an `nbstripout` hook (and `ruff`/`ruff-format` hooks while
  we're here).
- A one-time pass stripping outputs from the committed notebooks (and optionally a history rewrite,
  decided with the user — history rewrite is invasive).
- **Rendering strategy** (pick one, document it):
  - flip `mkdocs-jupyter` to `execute: true` so the site renders from clean sources at build time
    (raises build cost — measure it), **or**
  - keep `execute: false` but execute notebooks in the docs/deploy CI job before `mkdocs build`.
- A CI check that fails if a committed notebook contains outputs.
- Update `CONTRIBUTING.md` (the quality-tooling work, already delivered) with the no-output policy.

## Approach

- `.gitignore` currently only covers `.ipynb_checkpoints` and `/site`; add nothing for notebooks
  (they're tracked) but enforce the no-output rule via the hook + CI.
- Measure `mkdocs build` time with `execute: true` before committing to it; if too slow, prefer the
  execute-in-CI approach.

## Verification

- Repo size drops markedly; `git diff` on a re-run notebook is empty (outputs stripped); the
  published site still renders every notebook with figures.
