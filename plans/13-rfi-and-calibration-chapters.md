# Plan 13 — RFI mitigation & practical calibration chapters 📋 Proposed

> Flagged by **research-currency (#5)**. Scope: medium–large (large if both as full chapters).

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
