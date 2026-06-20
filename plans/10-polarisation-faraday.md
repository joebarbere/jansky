# Plan 10 — Polarisation & Faraday rotation chapter ✅ Delivered

> Flagged by **research-currency (#1 top)**. Scope: medium.
>
> **Delivered:**
> - **New chapter** `notebooks/37_polarisation_faraday.ipynb` (Part III) — Stokes parameters,
>   the Faraday λ² law and rotation measure, and **RM synthesis** / Faraday tomography. Recovers
>   an injected RM two ways (χ-vs-λ² fit and RM synthesis) on synthetic ASKAP/POSSUM-like spectra,
>   noiseless and noisy; shows the RMSF as the Faraday "dirty beam" across three survey bands;
>   includes a cosmic-magnetism / RM-grid section. Runs fully offline; 7 committed figures. Cites
>   Burn (1966), Brentjens & de Bruyn (2005), Dreher et al. (1987), Garrington et al. (1988), with
>   back-links to the timeline. (Authored by the `notebook-author` agent; reviewed by
>   `science-reviewer`.)
> - **Helper** `src/jansky/polarization.py` — `stokes_linear`, `linear_polarization_fraction`,
>   `polarization_angle`, `complex_polarization`, `faraday_rotate`, `rotation_measure_fit`, `rmsf`,
>   `rm_synthesis` — with `tests/test_polarization.py` (RM synthesis recovers the injected RM;
>   Stokes round-trips; RMSF normalised). Registered in `jansky.__init__`.
> - **Docs** — glossary entries (Faraday rotation, polarisation fraction & angle, rotation
>   measure, RM synthesis, Stokes), notation rows (χ, RM, I/Q/U/V), nav entry, and integration
>   into `docs/learning-paths.md` (map node + interferometry route + Maths-Lab A service row).
>
> Verification: `pytest` 106 passed/1 skipped (incl. nbmake on Ch 37), `ruff`, `mypy`, and
> `mkdocs --strict` all green.

## Context

The course has no treatment of polarisation, Stokes parameters, rotation measure, or RM synthesis —
confirmed by grep (no glossary entries for "Faraday rotation", "rotation measure", or "Stokes"
beyond passing mentions). Polarisation is one of the four pillars of radio observation and the
primary probe of cosmic magnetic fields; the science is *already cited* in the bibliography
(Garrington 1988, Dreher 1987) but never taught. SKA/POSSUM/LOFAR are producing million-source RM
grids right now.

## Deliverables

- **New chapter** (Part III), e.g. `notebooks/37_polarisation_faraday.ipynb`:
  - the **Stokes parameters** I/Q/U/V and the polarisation fraction/angle;
  - **Faraday rotation**, the λ² law, and the **rotation measure** (RM);
  - **RM synthesis** / Faraday tomography — a worked example recovering an RM from polarised
    spectra (synthetic, with a real-data path if a small POSSUM/LOFAR sample is available);
  - links to the magnetic-field science and the existing Laing–Garrington / Faraday entries in
    `papers-timeline.md`.
- **Helper** — small additions to `jansky.signals` (or a new `jansky.polarization`): Stokes
  construction, `faraday_rotate(angle, rm, wavelength)`, a simple RM-synthesis transform; with
  unit tests (recover an injected RM).
- **Docs** — glossary entries (Stokes, polarisation fraction, Faraday rotation, rotation measure,
  RM synthesis); a `notation.md` row; nav entry.

## Verification

- The chapter runs offline; the RM-synthesis demo recovers the injected RM; helper unit tests pass;
  `nbmake` + `mkdocs --strict` green.
