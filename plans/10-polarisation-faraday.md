# Plan 10 — Polarisation & Faraday rotation chapter 📋 Proposed

> Flagged by **research-currency (#1 top)**. Scope: medium.

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
