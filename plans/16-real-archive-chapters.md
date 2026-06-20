# Plan 16 — Finish the real-archive chapters 📋 Proposed

> Flagged by **archive/real-data (#3, #4, #5, #6)**. Scope: medium.

## Context

Several "real data" touchpoints are unfinished or simulated: Ch 10 ("Accessing Open Archives")
leaves `heasarc_snr_search` as a printed `TODO`; Ch 12 (VLA) has no bundled Measurement Set and
falls back to a Högbom stand-in; Ch 13 (Pulsars) has no real timing data; Ch 18 (FRBs) runs the DM
search on synthetic data only. And `docs/resources.md` claims "All URLs verified live" with nothing
keeping that true.

## Deliverables

- **Ch 10** — implement the HEASARC SNR query (`astroquery.heasarc`, `snrgreen` around Cas A) with a
  bundled offline fallback; models a second real archive beyond VizieR.
- **Ch 12** — register a small **real VLA Measurement Set / UVFITS** (e.g. a CASA-Guides 3C391
  subset) so learners inspect genuine visibilities via `pyuvdata` without the CASA container.
- **Ch 13 / Ch 20** — a real pulsar par/tim (PINT's `NGC6440E`) produces a real timing-residuals
  plot (pairs with [Plan 14](14-real-data-starter-set.md)).
- **Ch 18** — a real FRB / single-pulse filterbank (stably hosted: a Zenodo mirror or the
  `your`/PRESTO test corpus — CHIME's web root was flaky) to run the DM search on real bytes.
- **A guided "download real data" walkthrough** — one short notebook/section taking a learner
  end-to-end through a real archive query → cache via `jansky.data` → analyse.
- **`scripts/check_dataset_urls.py`** — `HEAD`-request every registered dataset URL and every
  archive link in `docs/resources.md`, reporting dead ones; run it on the `dataset_watch` cadence /
  in CI ([Plan 08](08-quality-tooling.md)). A `make fetch-data ARGS=--check` mode.

## Verification

- The previously-TODO cells execute (with offline fallbacks); the real MS/FRB/par-tim load; the URL
  checker passes (and we fix anything it flags); `nbmake` + `mkdocs --strict` green.
