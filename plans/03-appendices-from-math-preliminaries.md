# Plan 03 — Deeper math modules from the preliminaries

## Context

[`docs/math-preliminaries.md`](../docs/math-preliminaries.md) is a fast "get up to speed"
reference: nine sections, each a paragraph or two with a tiny snippet. Several of those
sections are the seed of a full, *worked* notebook — the kind of hands-on maths that the
science chapters lean on but don't have room to develop. This plan promotes the highest-value
preliminaries into executable appendix notebooks (an **"Appendix / Maths Lab"** group), each
tied to the chapter that needs it.

The goal is depth, not duplication: the preliminaries page stays the quick reference and gains
"→ see Maths Lab N" links; the new notebooks do the derivations, the plots, and the numerical
experiments.

## Already covered (do not duplicate)

- The *conceptual* treatment of all nine topics is in `math-preliminaries.md`.
- Applied uses already exist: the FFT/convolution in Ch 8–9, the radiometer statistics in Ch 3,
  spectral-index least-squares in Ch 2, beams/special functions in Ch 4. These appendices
  **generalise the method**; they don't re-derive a single chapter's result.

## Proposed appendix notebooks

### A. Fourier & convolution, hands-on
- **From:** preliminaries §2 (Fourier transform) & §3 (convolution).
- **Goal:** FT conventions (sign, 2π) and exactly how NumPy's FFT maps to the integrals; `fftshift`/`ifftshift`; the convolution theorem demonstrated numerically; **windowing & spectral leakage** (Hann/Hamming/Blackman) — the missing practical piece behind every spectrometer; zero-padding vs resolution.
- **Pays off in:** Ch 5 (spectra), Ch 8 (van Cittert–Zernike), [Plan 02-A](02-chapters-from-projects.md) (GNU Radio FFT).

### B. Detection theory & matched filtering
- **From:** preliminaries §5 (probability & statistics) + §8 (sinc/Gaussian).
- **Goal:** the matched filter as the optimal linear detector in Gaussian noise; the boxcar/template trade-off; **dedispersion as a matched filter** (ties to Ch 13) and the single-pulse S/N–vs–DM search (ties to [Plan 01-A FRBs](01-chapters-from-research-and-videos.md) and the Doppler-drift search in [Plan 01-C SETI](01-chapters-from-research-and-videos.md)); ROC curves and thresholds (the "5σ" convention).
- **Helper:** this is where the `jansky.transients` matched-filter primitives from Plan 01 should actually live and be tested.

### C. Noise statistics & RFI excision
- **From:** preliminaries §5 + the [`field-notes.md`](../docs/field-notes.md) RFI/perytons discipline.
- **Goal:** Gaussian vs non-Gaussian (impulsive) noise; the radiometer equation derived from the central limit theorem; robust statistics (median/MAD) for **RFI flagging**; spectral-kurtosis as an RFI detector; why averaging wins as 1/√N and when it doesn't (correlated noise, 1/f drift → Dicke switching, Ch 3).
- **Pays off in:** every observing chapter; especially FRB/SETI searches and AOFlagger-style flagging.

### D. Coordinates, time & the sky
- **From:** preliminaries §7 (coordinates & spherical trig).
- **Goal:** RA/Dec ↔ alt/az ↔ Galactic with `astropy.coordinates`; sidereal vs solar time (callback to Ch 1's "4 minutes earlier"); hour angle and how it drives Earth-rotation synthesis (Ch 8); the LSR correction used for HI velocities (Ch 6/11); precession/epoch (J2000) gotchas from [`notation.md`](../docs/notation.md).
- **Pays off in:** Ch 6, 8, 11, and any pointing/observation-planning task.

### E. Linear algebra for calibration
- **From:** preliminaries §9 (vectors & linear algebra) + §1 (complex numbers/phasors).
- **Goal:** the measurement equation as a matrix; complex antenna gains; **least-squares gain solving and self-calibration** as a linear-algebra problem (motivates Cornwell & Wilkinson 1981, in the [papers timeline](../docs/papers-timeline.md)); closure phase/amplitude as gain-invariant combinations (shared with [Plan 01-B EHT/VLBI](01-chapters-from-research-and-videos.md)); SVD for ill-conditioned solves.
- **Pays off in:** Ch 9, Ch 12 (CASA calibration), the EHT chapter.

### F. Special functions & beams (optional, light)
- **From:** preliminaries §8.
- **Goal:** consolidate sinc, Gaussian (FWHM↔σ), Airy/Bessel `J1` (the `1.22 λ/D` factor, Ch 4), and power-laws (spectral index, Ch 2) with the window-function family from Maths Lab A. Mostly a polished reference notebook reusing `jansky.signals`.

## Cross-cutting deliverables

- A new `docs/` nav group ("Maths Lab" / "Appendices") and "→ Maths Lab N" links added back
  into the relevant `math-preliminaries.md` sections (bidirectional).
- Helper homes: matched-filter/detection primitives in `jansky.transients` (Lab B), robust-stats
  and spectral-kurtosis in `jansky.signals` or a new `jansky.rfi` (Lab C), calibration helpers in
  `jansky.interferometry` (Lab E).
- Keep these notebooks dependency-light (numpy/scipy/astropy already in core).

## Verification

- Each appendix runs on the base env, no network, with unit tests for the new primitives:
  matched filter recovers a known template's S/N; MAD/spectral-kurtosis flags injected RFI;
  the gain-solver recovers injected complex gains; closure phase is invariant under
  per-antenna phase errors.
- `pytest` + `pytest --nbmake` (for the lighter labs) + `mkdocs build --strict`.
