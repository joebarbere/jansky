# Plan 06 — Publish the docs site to GitHub Pages 📋 Proposed

> Flagged by **engineering (#3)**. Scope: small. Best done after [Plan 05](05-ci-pipeline.md).

## Context

The course's reference-library-quality MkDocs site (rendered notebooks, full bibliography, the
glossary/notation/telescopes/papers-timeline pages, ~490 external links) is built locally but
**never hosted**. Publishing it is the payoff for all the docs work and makes the course
discoverable. `pyproject.toml`'s `Documentation` URL currently points at the repo, not a live site.

## Deliverables

- **`.github/workflows/gh-pages.yml`** — on push to `main`, build and deploy with
  `mkdocs gh-deploy --force` (or the `actions/deploy-pages` flow); cache uv.
- **`mkdocs.yml`**: set `site_url` to the Pages URL; confirm `repo_url`/edit links.
- **`pyproject.toml`**: update `Documentation = "https://joebarbere.github.io/jansky/"`.
- A "Read the docs" link in `README.md`.

## Approach

- Decide the notebook-rendering source: the site currently renders committed outputs
  (`mkdocs-jupyter: execute: false`). Either keep that, or coordinate with
  [Plan 07](07-notebook-hygiene.md) to execute on build/CI so the published site doesn't depend on
  committed outputs.
- Enable Pages in the repo settings (source = GitHub Actions).

## Verification

- The workflow runs on `main` and the site is live at the Pages URL with notebooks, images, and
  Mermaid diagrams rendering correctly; internal links resolve (already guaranteed by `--strict`).
