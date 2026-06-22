# Plan 14 — Real-data starter set ◑ Mostly delivered

> Flagged by **archive/real-data (#1 top, plus #3)**. Scope: medium.
>
> **Delivered:**
> - **Small real-data registry** in `src/jansky/data.py` — a `category` field ("small"/"large")
>   on `Dataset`, plus five real files (all < 2 MB, stable raw-GitHub URLs, HTTP 200-verified):
>   `psrfits-small` and `filterbank-small`/`filterbank-example` (real PSRFITS/SIGPROC from the
>   `your` test suite) and `pint-ngc6440e-par`/`pint-ngc6440e-tim` (the real NANOGrav timing
>   model + TOAs for PSR J1748−2021E in NGC 6440). The 576 MB HI4PI map is **demoted to
>   `category="large"`**, off the default path. New `small_datasets()` helper; `--list` now groups
>   small-first.
> - **`scripts/check_dataset_urls.py`** — verifies every registered URL still resolves (overlaps
>   [Plan 16](16-real-archive-chapters.md)); a green run is the evidence the starter files are
>   fetchable. All six URLs currently resolve.
> - **Tests** (`tests/test_data.py`) — registry well-formedness, the small-vs-large split, and a
>   network-gated real fetch (downloads the real `NGC6440E.par`, skipped offline). `docs/data-formats.md`
>   documents the starter set.
>
> **Chapter wiring — Ch 13 done.** Chapter 13 (Pulsars), previously 100% synthetic, now runs a
> **real PINT timing fit** on the registered `pint-ngc6440e-par`/`-tim` (PSR J1748−2021E) and plots
> the real NANOGrav timing residuals, guarded behind the `pulsar` extra with an offline fallback.
> Chapter 23 similarly reads the real `.sps` Jupiter recording (see [Plan 15](15-sps-spd-readers.md)).
>
> **Update — both done.** Ch 18 runs the real `your` filterbank (`filterbank-example`) through the
> `dm_search` butterfly (DM ≈ 474, S/N 13.3). And **Ch 11 now reduces a real HI spectrum**: a small
> (366 KB) `(b, v)` slice of the **LAB all-sky HI survey** at l = 12° (`lab-hi-l12`, registered in
> `jansky.data`) — the b = 0 sightline gives a real tangent-point rotation point (v_rot ≈ 199 km/s at
> R ≈ 1.7 kpc), with an offline fallback. (The 576 MB HI4PI all-sky cube remains opt-in; the LAB slice
> is the small real HI path.)

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
