---
name: radio-source-lookup
description: Gather what's known about a radio source or sky position across catalogues and archives — SIMBAD/NED for identity, NVSS/FIRST/VLA for radio flux and spectral index, and the VO via astroquery/pyvo. Use when the user names a source (e.g. Cygnus A, 3C 273, Sgr A*) or a position and wants its radio properties, observations, or multi-wavelength data.
---

# Look up a radio source

Assemble a concise profile of a named source or sky position from open catalogues, reusing the
patterns the course already teaches.

## Procedure (mirror Chapters 10 & 14)

1. **Resolve identity & position** with `astroquery.simbad` (and NED for extragalactic objects):
   coordinates, object type, redshift. Use `astropy.coordinates.SkyCoord` for the position.
2. **Radio measurements** via `astroquery.vizier` cone searches:
   - **NVSS** (`VIII/65`) — 1.4 GHz flux over most of the sky.
   - **FIRST** (`VIII/92`) — 1.4 GHz high-resolution.
   - add other-frequency catalogues (e.g. low-frequency surveys) as available, then estimate a
     **spectral index** from two or more frequencies (see `jansky.signals.power_law`).
3. **Which instruments can observe it** — cross-reference `docs/telescopes.md` (declination &
   frequency coverage) and the archives in `docs/resources.md` for where to get raw data.

**Always wrap network calls in try/except** and fall back gracefully (the course chapters do this);
if offline, say so and report what would be queried.

## Report

A short profile: identity/position/type, the radio flux densities found (with frequency and
survey), an estimated spectral index if ≥2 points exist, and pointers to archives/instruments for
follow-up. Cite the surveys (NVSS = Condon et al. 1998, FIRST = Becker et al. 1995 — both in
`docs/references.md`).

For heavy or multi-archive data hunts (finding actual observation datasets to download), hand off
to the **archive-scout** agent.
