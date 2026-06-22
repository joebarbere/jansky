# Plan 13 — RFI mitigation & practical calibration chapters ✅ Both delivered

> Flagged by **research-currency (#5)**. Scope: medium–large (large if both as full chapters).
>
> **Part A delivered — RFI mitigation chapter** (the plan advised doing A first):
> - **New chapter** `notebooks/39_rfi_mitigation.ipynb` (Part IV) — practical flagging on a
>   synthetic dynamic spectrum with realistic RFI (CW lines, broadband bursts, a faint drifting
>   feature, periodic satellite blips); compares three flaggers from `jansky.rfi` (robust
>   thresholding, spectral kurtosis, SumThreshold), quantifies flagged fraction and signal-recovery
>   RMSE, and covers radio-quiet zones, ITU spectrum protection, and Starlink. Cites Offringa et al.
>   (2010) and Nita & Gary (2010). Fully offline. Authored by `notebook-author`, reviewed by
>   `science-reviewer`.
> - **Helper** — added **`jansky.rfi.sumthreshold`** (1-D Offringa SumThreshold) and
>   **`sumthreshold2d`** (time-then-frequency) with unit tests (low false-positive on noise; catches
>   a faint *extended* burst a single-sample cut misses; flags both a narrowband line and a
>   broadband burst in 2-D).
> - **Docs** — glossary (AOFlagger/SumThreshold, Flagging, Radio-quiet zone), nav, and learning-paths
>   integration (map node + Maths-Lab C service row).
>
> **Part B delivered — practical calibration chapter** (`notebooks/41_practical_calibration.ipynb`,
> Part III; shipped as Ch 41 because Ch 40 became the Lightning chapter). The applied companion to
> Maths Lab E: the measurement equation $V^\mathrm{obs}_{ij}=g_i V^\mathrm{true}_{ij} g_j^*$ →
> gain calibration → per-channel bandpass → gain-error-vs-SNR → the Cornwell–Wilkinson self-cal loop,
> with closure phase/amplitude as the gain-immune anchor and a guarded `pyuvdata` real-VLA aside.
> - **Helpers** — added **`jansky.interferometry.apply_gains`** (the forward measurement equation) and
>   **`solve_gains_stefcal`** (the antenna-based StefCal solver behind gain-cal and self-cal), with
>   unit tests (recovers point-source gains to ~1e-6, robust to 2% visibility noise).
> - **Docs** — glossary (Gain calibration, Measurement equation), nav (Part III), references
>   (Cornwell & Wilkinson 1981, Pearson & Readhead 1984, Hamaker et al. 1996), learning-paths.
> - Authored by `notebook-author`, reviewed by `science-reviewer`.
> - **Polarisation calibration added (Section 9).** Ch 41 now extends the measurement equation to
>   the polarised case: per-antenna **D-terms** (leakage), solved from an unpolarised calibrator's
>   cross-hand visibilities ($V^{RL}_{ij} \approx (d_i + d_j^{*})I$, gauge-fixed to a reference
>   antenna) — feeding the Stokes Q/U science of Ch 37. New tested helpers
>   `jansky.interferometry.apply_leakage` / `solve_leakage` (exact round-trip, noise-robust).

## Context

RFI currently lives mostly in Maths Lab C and the `jansky.rfi` helper (spectral kurtosis);
calibration is a linear-algebra appendix (Maths Lab E). The field-notes page itself says
"math-heavy calibration is the secret sauce" and that RFI is "the discipline of not fooling
yourself" — yet these are the thinnest *practical* coverage in the course, and they are where real
projects succeed or fail.

## Deliverables

### A. RFI mitigation chapter (Part II/IV)
`notebooks/39_rfi_mitigation.ipynb` — flagging strategies in practice (AOFlagger-style
sumthreshold), time/frequency vs baseline flagging, the regulatory context (radio-quiet zones),
**satellite-constellation interference** (Starlink — already flagged in `field-notes.md`), and how
excision fits a real pipeline. Reuse `jansky.rfi` (`flag_outliers`, `spectral_kurtosis`,
`flag_by_kurtosis`); add a sumthreshold-style flagger to the module with tests.

### B. Practical calibration chapter (Part III/IV)
`notebooks/40_practical_calibration.ipynb` — a hands-on bandpass → gain → (optionally) polarisation
calibration walkthrough on a **real, small Measurement Set** (via `pyuvdata`, no CASA container
needed; coordinate with [Plan 16](16-real-archive-chapters.md) which sources the MS). Reuse
`interferometry.solve_point_source_gains` and the closure quantities; connect to Cornwell &
Wilkinson 1981 self-cal and Ch 12 (CASA at scale).

## Approach

- These can ship independently; A is lighter (reuses `jansky.rfi` + sims), B depends on a real MS
  sample. Consider doing A first.

## Verification

- Both run offline (B with a bundled small MS or a synthetic fallback); new flagger has unit tests;
  `nbmake` + `mkdocs --strict` green.
