# Plan 11 — SKA-era & 2025–2026 currency refresh 📋 Proposed

> Flagged by **research-currency (#2 top, plus #3 and #6)**. Scope: small–medium.

## Context

The papers timeline ends at 2025 and the telescopes catalogue still frames SKA / DSA-2000 / ngVLA
as purely future — but **SKA-Low produced its first image in 2025** (≈1,000 of 131,000 antennas)
and **SKA-Mid achieved first fringes in January 2026**. A course that frames the defining event of
the current radio era as "will be the world's largest" reads as dated to any practitioner. One
contested result is also presented as established.

## Deliverables

- **Timeline refresh** (`docs/papers-timeline.md`) — add verified 2025–2026 landmarks: SKA-Low
  first light / SKA-Mid first fringes, the latest long-period-transient and most-distant-FRB
  results, and any 2025 PTA/EHT follow-ups. Verify each via ADS/observatory pages.
- **Telescopes update** (`docs/telescopes.md`) — change SKAO/DSA-2000/ngVLA status lines from
  "under construction" to current AA0.5/AA1 milestones; refresh the KML note if needed.
- **EDGES caveat** — the 2018 timeline entry presents Bowman/EDGES as "first detection of the
  cosmic-dawn 21 cm signal"; add a one-line caveat that **SARAS-3 disfavours it at ~95%** and it
  remains contested. (Optionally a short cosmic-dawn/EoR section — global signal vs power spectrum,
  EDGES/SARAS/REACH/HERA/LOFAR/MWA — but that can be its own follow-up.)
- **Stay-current process** — a short `MAINTAINING.md` (or a section in `CONTRIBUTING.md`) describing
  a quarterly cadence that runs the repo's own `dataset-watch` / `find-radio-papers` /
  `archive-scout` tooling to surface new landmarks, plus the docs link-checker from
  [Plan 08](08-quality-tooling.md).

## Verification

- New entries are link-verified (ADS/DOI/observatory); `mkdocs --strict` passes; the EDGES entry
  no longer overclaims.
