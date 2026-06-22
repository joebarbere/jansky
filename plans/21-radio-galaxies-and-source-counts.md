# Plan 21 — Radio galaxies, AGN & the radio source population 📋 Proposed

> Flagged by the **ERA gap analysis** (the extragalactic radio sky / source counts). Scope:
> medium. The research-flavoured one of the three ERA-gap chapters; builds on
> [Plan 19](19-synchrotron-radiation.md) (synchrotron powers these sources).

## Context

The extragalactic radio sky — radio-loud AGN, radio galaxies, quasars, and their **source counts** —
runs through *Essential Radio Astronomy* (ERA Ch 2's source counts and Ch 5's radio galaxies). The
jansky course touches AGN only obliquely: Ch 19 images M87's black hole and Ch 14 builds an AGN SED,
but there is no treatment of **radio-source morphology** (FR I vs FR II), the radio luminosity
function, or **log N–log S source counts** — the cosmological probe whose departure from the
Euclidean −1.5 slope helped end steady-state cosmology (Ryle's Nobel work, already name-dropped in
Ch 7). "Source counts" appears in **zero** notebooks. This is the natural *research* companion to the
synchrotron physics of [Plan 19](19-synchrotron-radiation.md), and it reuses the archive-query
machinery the course already has.

## Deliverables

- **New chapter** `notebooks/45_radio_galaxies_and_source_counts.ipynb` — suggested placement in
  **Part IV — Real Data & Research** (it queries real catalogues).
- **Helper** `src/jansky/sourcecounts.py` (tested), e.g.:
  - `euclidean_counts(s)` — the static-Euclidean differential count N(S) ∝ S^−2.5 (integral ∝ S^−1.5).
  - `differential_counts(...)` / `integral_counts(...)` from a flux array (the empirical estimator).
  - `count_slope(...)` — fit the log N–log S slope.
  - a toy **radio luminosity function** and an optional simple cosmological-evolution factor.
- **Notebook content:** FR I vs FR II morphology (edge-darkened jets vs edge-brightened lobes &
  hotspots — a toy image generator, reusing `jansky.plotting`); the radio-loud unified model in
  brief; the **radio luminosity function**; and **log N–log S source counts** — the Euclidean slope,
  why a steeper observed slope at faint flux implies cosmic evolution (the steady-state-killer), and
  the modern normalised differential counts. 5–6 captured figures.
- **Real data:** compute a **real log N–log S from the NVSS catalogue** (the `astroquery`/VizieR
  cone-search already used in Ch 10/14), and show a real **Cygnus A / FR II** image or flux table;
  offline fallback to a simulated catalogue.
- **3 "Try it yourself" exercises** with collapsible worked solutions.
- **Wiring:** nav; references (ERA Ch 2/5; Fanaroff & Riley 1974; Ryle & Clarke 1961 source counts;
  Condon 1992 radio–FIR; de Zotti et al. 2010 counts); glossary (*FR I / FR II*, *log N–log S source
  counts*, *radio luminosity function*, *radio-loud AGN*); learning-paths node; cross-links to Ch 7
  (Ryle's counts), Ch 14 (SEDs), Ch 19 (AGN/VLBI), and Plan 19's synchrotron chapter.

## Approach

- Build and unit-test `jansky.sourcecounts` first (Euclidean slope recovery; the estimator on a
  simulated population), then author the notebook, then `science-reviewer`.
- Keep the cosmological-evolution treatment qualitative/toy; the teaching point is the slope and its
  departure from Euclidean, not a full evolutionary model.

## Verification

- `ruff` + `mypy` + `pytest` green; `nbmake` **fully offline** (the real NVSS counts guarded with a
  simulated fallback); `mkdocs build --strict` + doc-link test green; new citation URLs verified live.
