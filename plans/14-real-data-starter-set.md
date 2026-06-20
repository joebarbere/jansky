# Plan 14 — Real-data starter set 📋 Proposed

> Flagged by **archive/real-data (#1 top, plus #3)**. Scope: medium.

## Context

`jansky.data.DATASETS` has exactly **one** entry — `hi4pi-sample`, a **~576 MB** all-sky FITS that
is never bundled and that CI/offline always falls back from to synthetic. The "real data" chapters
are mostly simulated: Ch 11 almost always runs on `synthetic_hi_cube`, Ch 13 (Pulsars) is **100%
synthetic** (`psrfits_path = None`). Learners rarely see a single real byte unless they have a
network *and* patience for a half-gigabyte download.

## Deliverables

- **Add a small (<5 MB) real-data registry** to `src/jansky/data.py` (with a `size`/`category`
  field), and make these the *default* path:
  - a **HI4PI cutout** (a single small region, not the 576 MB `NHI_HPX.fits`);
  - `your`'s real **`small.fil` / `small.fits`** (PSRFITS/filterbank) —
    `github.com/thepetabyteproject/your` (raw, verified live);
  - PINT's **`NGC6440E.par` / `NGC6440E.tim`** (real NANOGrav timing, verified live).
  - keep the full HI4PI map as an opt-in `"large"` entry.
- **Wire into chapters** — Ch 11 reduces the real HI cutout; Ch 13 de-disperses/folds the real
  `small.fil` (drives the existing `Your(psrfits_path)` branch) — see also
  [Plan 16](16-real-archive-chapters.md) for the pulsar-timing piece.
- Cache to the existing `data/` dir; commit nothing large (fetch + cache, with synthetic fallback
  preserved for offline).

## Verification

- `python -m jansky.data --list` shows the new small entries; `nbmake` smoke-tests now exercise the
  *real* read paths; the 576 MB map is no longer on the default path. Re-verify all registered URLs
  resolve (overlaps [Plan 16](16-real-archive-chapters.md)'s URL checker).
