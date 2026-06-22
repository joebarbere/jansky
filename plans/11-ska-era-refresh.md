# Plan 11 — SKA-era & 2025–2026 currency refresh ✅ Delivered

> Flagged by **research-currency (#2 top, plus #3 and #6)**. Scope: small–medium.
>
> **Delivered (all link-verified, HTTP 200):**
> - **Timeline** (`docs/papers-timeline.md`) — added SKA-Low first image (March 2025, 1,024/131,072
>   antennas) and SKA-Mid first fringes (Jan 2026, two 15 m dishes); the 2020s intro now names the
>   SKA's first light.
> - **EDGES caveat** — the 2018 Bowman/EDGES entry is flagged **contested**, with a new 2022
>   SARAS-3 (Singh et al.) row noting the 95.3% rejection of the cosmic-dawn profile.
> - **Telescopes** (`docs/telescopes.md`) — the SKAO row moved from "Under construction … will be
>   the world's largest" to current early-array milestones (SKA-Low first image; SKA-Mid first
>   fringes, ~7 of 197 dishes on site) and "becoming the world's largest". DSA-2000/ngVLA were left
>   as accurate "planned/under development" (no verified 2025–26 milestone to update without
>   overclaiming).
> - **`MAINTAINING.md`** — a quarterly currency process built on the repo's own `dataset-watch` /
>   `find-radio-papers` / `archive-scout` tooling plus the lychee link-checker, with
>   verify-then-write / annotate-don't-erase principles. Linked from `CONTRIBUTING.md`.
>
> Sources: [SKA-Low first image](https://www.skao.int/en/news/560/first-image-released-one-ska-low-station),
> [SKA-Mid first fringes](https://www.skao.int/en/news/693/ska-mid-milestone),
> [SARAS-3](https://doi.org/10.1038/s41550-022-01610-5).
> The optional standalone cosmic-dawn/EoR *chapter* remains a possible follow-up. (The EoR/21 cm and
> CMB *software ecosystem* — 21cmFAST, tools21cm, 21cmSense, HERA/CHIME m-mode tools, healpy/PySM —
> is now catalogued in [`docs/github.md`](../docs/github.md), and the course covers 21 cm physics in
> Ch 6/11 and CMB in Ch 22.)

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
