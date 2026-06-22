# Plan 16 — Finish the real-archive chapters ◑ URL-verification delivered

> Flagged by **archive/real-data (#3, #4, #5, #6)**. Scope: medium.
>
> **Delivered — the "keep it verified" engineering** (the last two deliverables):
> - **`scripts/check_dataset_urls.py`** extended to also check the documentation's external links
>   (`docs/resources.md` by default, which advertises "All URLs verified live"; `--docs FILE …`
>   for others). Runs concurrently with a browser User-Agent; classifies results **ok / warn /
>   fail** so bot-blocked 403s (publisher/SourceForge sites that are live for humans) are warnings,
>   not failures, and only genuinely-dead links (404/410/5xx/connection/SSL) fail the run.
> - **Fixed the 3 genuinely-dead links** the checker found in `resources.md`: the IAU Commission B4
>   page (404 → the live `iau.org/CommissionB4/…` URL), Arecibo/NAIC (SSL-broken `www.naic.edu` →
>   the NSF Arecibo C3 page), and UFRO's dead IJRO host (→ the UF Astronomy department). The
>   checker now exits 0 (4 remaining entries are bot-blocked-but-live 403 warnings).
> - **`make check-urls`** target (datasets + `resources.md`).
>
> **Ch 13 timing residuals — done.** Chapter 13 (Pulsars) now runs a **real PINT fit** on the
> registered `NGC6440E` par/tim (PSR J1748−2021E, 62 NANOGrav TOAs, 709-day span) and plots the
> microsecond timing residuals (post-fit RMS ≈ 21 µs ≈ the TOA errors), guarded behind the `pulsar`
> extra with an offline fallback. Closes the Ch 13/20 par/tim item.
>
> **Ch 18 real filterbank — done.** Chapter 18 (FRBs) now points the same `dm_search` at the real
> `your` example filterbank (`filterbank-example`, registered in `jansky.data`): it reads the
> 336-channel L-band recording with `your`, runs the butterfly over 0–1000 pc cm⁻³, and recovers a
> genuine dispersed burst at **DM ≈ 474 pc cm⁻³, S/N 13.3** (vs 3.4 at DM 0) — guarded behind the
> `pulsar` extra with an offline fallback.
>
> **Ch 10 HEASARC — done.** Chapter 10's Exercise 2 TODO is now an implemented `heasarc_snr_search`:
> it queries the **Green catalogue of Galactic SNRs** (`snrgreen`) via `astroquery.heasarc`'s
> current TAP API (`Heasarc.query_region(coord, catalog=…, radius=…)`) within 5° of Cas A —
> returning 5 real SNRs with their 1 GHz radio fluxes (Cas A itself the brightest at ~2400 Jy) —
> with `heasarc` added to the defensive `ARCHIVE_LIBS` guards and a citable bundled offline
> fallback, mirroring `cone_search_nvss`.
>
> **Ch 12 real visibilities — done.** Chapter 12's base-env "concept stand-in" now opens a **real**
> (E)VLA Measurement Set — the CASA-guides `day2_TDEM0003` UVFITS (calibrator J1008+0730 at 36 GHz,
> 18 antennas; registered as the `vla-uvfits` dataset) — with **`pyuvdata`** (no CASA container),
> and plots the genuine **uv-coverage** and **amplitude-vs-baseline** (flat, the point-source
> calibrator signature). Guarded behind the `formats` extra with an offline fallback.
>
> **Walkthrough — covered.** The guided "download real data" walkthrough is delivered in place as
> Chapter 10's section *"4 · Caching what you fetch with `jansky.data`"*, which takes a learner through
> a real archive query → cache → analyse end-to-end; a separate notebook would have duplicated it.
> (Minor open item: Ch 10's code cells are committed without executed outputs — a later re-execution
> pass would populate them.)

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
