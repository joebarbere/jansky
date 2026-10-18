# Plan 01 — Orbital angular momentum of radio waves: a chapter and a station experiment

Status: 📋 proposed (2026-10-17). Two deliverables that share one helper module: a course chapter
(notebook 51) and a hands-on station experiment that measures the OAM mode of a radio beam with
the KrakenSDR from Chapter 17. Research follow-up (testing the M87\* "twisted light" spin claim on
public EHT data) belongs in `../jansky-research` and is being GATE-0'd there; this plan only
teaches the idea and points to it.

## Why

Light carries two kinds of angular momentum: **spin** (circular polarisation, ±ħ per photon —
already taught in Chapter 37) and **orbital** (a helical phase front e^{iℓφ}, ℓħ per photon). OAM
was established for optical beams by Allen et al. (1992) and taken to radio by Thidé et al. (2007),
who generated and detected it with antenna arrays. In astronomy it has been proposed as a probe of
spinning black holes (Tamburini et al. 2011) and claimed in EHT data of M87\* (Tamburini, Thidé &
Della Valle 2020) — a claim that, as far as a first literature check shows, has not been
independently tested. It is a rare topic where the physics is clean, the hardware is affordable,
and the open questions are visible to a student. It also teaches critical reading: the 2012
"radio vorticity" multiplexing experiment drew a published Comment and Reply.

## Deliverable A — Chapter 51: "Twisted radio waves: orbital angular momentum"

Follows `.claude/agents/notebook-author.md` and the inline-first + back-of-the-envelope style of
Chapter 3. Outline:

1. **Spin vs orbital angular momentum.** Circular polarisation (link Ch. 37) vs a helical phase
   front; why ℓ can be any integer while spin is ±1. Allen et al. 1992.
2. **Laguerre–Gauss beams.** Plot the intensity "donut" and the phase spiral for ℓ = 0, ±1, ±2;
   the on-axis null and why it matters for detection.
3. **Making OAM at radio frequencies.** A uniform circular array (UCA) with progressive phase
   2πℓ/N between N elements (Thidé et al. 2007); spiral phase plates and twisted reflectors.
4. **Measuring ℓ with a ring of antennas.** Sample the field at N points on a circle, take a DFT
   in azimuth → an OAM spectrum. Azimuthal Nyquist: N > 2|ℓ_max|. What tilt and offset do
   (power leaks into neighbouring ℓ), and what noise does to mode purity.
5. **Is it new physics or MIMO?** The 2012 debate (Tamburini et al. 2012; the Comment by
   Tamagnone et al. 2012; the Reply). Present both sides; let the reader compute the far-field
   mode overlap that the argument turns on.
6. **OAM in astronomy — and why it is hard.** A helical phase is only visible to an aperture that
   spans the structure; for a distant source the relevant scale grows with distance
   (Harwit 2003; Elias 2008 review). Back-of-the-envelope: the aperture needed to see ℓ = 1 from a
   given source.
7. **Spinning black holes.** Frame-dragging imprints OAM (Tamburini et al. 2011); the 2020 M87\*
   spin claim, stated as a claim, with the reason an independent test is interesting (and a link
   to the research slice if it happens).
8. **Exercises + a station sidebar** pointing to Deliverable B.

Back-of-the-envelope section (Chapter 3 pattern, `expected_log10` answers): how many ring elements
for |ℓ| ≤ 3; mode leakage from a 5° tilt; the aperture needed at a stated distance.

## Deliverable B — Station experiment: measure the OAM mode of a beam with the KrakenSDR

The Chapter 17 KrakenSDR already gives five phase-coherent channels on one clock with a built-in
noise source for phase calibration. Arranged on a **ring** instead of a line, those five channels
are an OAM spectrometer for |ℓ| ≤ 2.

- **Source.** A small UCA (4–8 elements) fed from one oscillator with fixed cable-length phase
  steps (or a Butler matrix) to make ℓ = 0, ±1. Frequency **must** be legal to transmit on:
  a low-power unlicensed band (US: 902–928 MHz under FCC Part 15) or an amateur band under a
  licence. This is the plan's one hard prerequisite and is decided before any hardware is bought.
  Everything else is receive-only.
- **Receiver.** Five antennas on a ring of radius ~λ (≈ 33 cm at 915 MHz), coherent phases from the
  KrakenSDR, calibrated with its noise source; the OAM spectrum is the azimuthal DFT.
- **Controls, fixed before the first measurement** (the research repo's planted-truth habit):
  ℓ = 0 transmit must give a flat phase ring; rotating the receive ring rotates the phase pattern
  but not ℓ; swapping the feed order flips the sign of ℓ; moving from near to far field shows the
  purity loss the 2012 Comment predicts. A cabled (not over-the-air) injection is the first
  recover-a-known.
- **Where it lives.** Build notes in `../jansky-research/station/oam-experiment.md` next to the
  other station guides; the analysis code is `jansky.oam` so the chapter and the station share it.

## Shared helper — `src/jansky/oam.py` (tested)

`laguerre_gauss(r, phi, z, ell, p, w0, wavelength)`, `uca_weights(n, ell)`,
`sample_ring(field_fn, radius, n)`, `oam_spectrum(samples)` (azimuthal DFT, normalised),
`mode_purity(spectrum, ell)`, `tilt_leakage(ell, tilt_rad, radius, wavelength)`. Unit tests
against closed forms (a pure mode gives purity 1; N samples alias ℓ and ℓ ± N; tilt leakage
matches the small-angle expansion). Constants in `jansky.constants`, not cells.

## Order of work

1. `jansky.oam` + tests (offline). 2. Chapter 51 notebook + `docs/chapters` page + `mkdocs.yml`
nav + references/papers-timeline entries. 3. `science-reviewer` pass. 4. Station experiment:
licensing decision → cabled test → over-the-air ℓ = 0/±1 → write-up. Steps 1–3 do not depend on 4.

## Checks

`make lint`, `make typecheck`, `make cov`, `make docs` (strict), `make test-notebooks` for the
new notebook; every reference below cited in the chapter and added to `docs/references.md`.

## References (DOIs verified on Crossref, 2026-10-17)

- Allen, Beijersbergen, Spreeuw & Woerdman 1992, *Phys. Rev. A* 45, 8185 — 10.1103/PhysRevA.45.8185
- Harwit 2003, *ApJ* 597, 1266 — 10.1086/378623
- Thidé et al. 2007, *Phys. Rev. Lett.* 99, 087701 — 10.1103/PhysRevLett.99.087701
- Elias 2008, *A&A* 492, 883 — 10.1051/0004-6361:200809791
- Tamburini et al. 2011, *Nature Physics* 7, 195 — 10.1038/nphys1907
- Tamburini et al. 2012, *New J. Phys.* 14, 033001 — 10.1088/1367-2630/14/3/033001
- Tamagnone, Craeye & Perruisseau-Carrier 2012 (Comment), *New J. Phys.* 14, 118001 —
  10.1088/1367-2630/14/11/118001
- Tamburini et al. 2012 (Reply), *New J. Phys.* 14, 118002 — 10.1088/1367-2630/14/11/118002
- Tamburini, Thidé & Della Valle 2020 (online 2019), *MNRAS* 492, L22–L27 — 10.1093/mnrasl/slz176

Authors, volumes and pages as Crossref returns them for each DOI.

## Risks

- **Transmit legality** gates Deliverable B only; the chapter does not depend on it.
- **Over-claiming the astronomy.** The M87\* result is presented as a single group's claim until an
  independent test exists; no sentence says OAM "has been detected" from an astronomical source.
- **Hardware.** Five channels limit the ring to |ℓ| ≤ 2; that is enough for the teaching goal.
