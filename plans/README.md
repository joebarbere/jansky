# jansky — expansion plans (delivered)

This directory held the expansion plans for the course. **All four plans have now been
implemented and merged**, so each plan file below is a short *delivered record* (what shipped,
which chapters/modules, and any outstanding follow-ups) rather than a forward-looking proposal.
The git history and the chapters themselves are the full record.

## Status

| Plan | Status | Delivered |
|---|---|---|
| [01 — chapters from research & videos](01-chapters-from-research-and-videos.md) | ✅ Complete | Chapters 18–25 (FRBs, EHT/VLBI, PTAs, SETI, CMB, solar/Jupiter, molecular/masers, intensity interferometry) |
| [02 — chapters from the projects list](02-chapters-from-projects.md) | ✅ Complete | Chapters 17, 26–30 (KrakenSDR, meteor scatter, VLF/SuperSID, GNU Radio, VIRGO/PICTOR, RASDR) |
| [03 — appendices from math preliminaries](03-appendices-from-math-preliminaries.md) | ✅ Complete | Chapters 31–36 (the six "Maths Lab" appendices) |
| [04 — data formats & SETI software](04-data-formats-and-seti-software.md) | ✅ Complete | Chapter 16 + `jansky.formats`; the `.sps`/`.spd` readers (the one deferral) are now implemented — see Plan 15 |

## What the plans added

**10 new helper modules / capabilities** in `src/jansky/`: `formats`, `transients`, `timing`,
`seti`, `solar`, `molecular`, `meteor`, `vlf`, `rfi`, plus coherent-interferometry, closure
quantities, HBT intensity interferometry, a point-source gain solver, and `units.planck_brightness`.

**21 new chapters** (16–36) taking the course from 15 → 36 chapters, every one runnable fully
offline, all covered by `pytest`/`nbmake` and the strict docs build.

## Proposed (from the agent review)

Plans **05–18** came out of a repo-wide review by the project's agents (science-rigor, pedagogy,
research-currency, archive/real-data, and engineering). They are **📋 proposed** — not yet
implemented. ⭐ marks an agent top-pick or a cross-agent consensus item.

| Plan | Theme | Scope |
|---|---|---|
| ⭐ [05 — CI pipeline](05-ci-pipeline.md) ✅ | Engineering | small–medium |
| [06 — Publish docs to GitHub Pages](06-publish-docs.md) ✅ | Engineering | small |
| [07 — Notebook output hygiene](07-notebook-hygiene.md) | Engineering | medium |
| [08 — Quality tooling (types, coverage, contributing, link-check)](08-quality-tooling.md) ✅ | Engineering | medium |
| ⭐ [09 — Scientific-accuracy hardening](09-accuracy-hardening.md) ✅ | Rigor | small–medium |
| ⭐ [10 — Polarisation & Faraday rotation chapter](10-polarisation-faraday.md) ✅ | Content | medium |
| ⭐ [11 — SKA-era & 2025–2026 refresh](11-ska-era-refresh.md) ✅ | Content | small–medium |
| [12 — Machine learning in radio astronomy](12-ml-in-radio.md) ✅ | Content | medium |
| [13 — RFI mitigation & calibration chapters](13-rfi-and-calibration-chapters.md) ✅ | Content | medium–large |
| ⭐ [14 — Real-data starter set](14-real-data-starter-set.md) ✅ | Real data | medium |
| ⭐ [15 — Implement SPS/SPD readers](15-sps-spd-readers.md) ✅ | Real data | medium–large |
| [16 — Finish the real-archive chapters](16-real-archive-chapters.md) ✅ | Real data | medium |
| ⭐ [17 — Learning-journey map](17-learning-journey-map.md) ◑ | Pedagogy | medium |
| [18 — Worked solutions, onboarding & accessibility](18-solutions-and-accessibility.md) ✅ | Pedagogy | medium–large |

## Outstanding follow-up

- The Plan 04 deferral is **closed**: `jansky.formats.read_sps` / `read_spd` are implemented
  (see [Plan 15](15-sps-spd-readers.md)), with `read_sps` validated byte-for-byte against a real
  Radio JOVE recording. The live Radio-Sky Spectrograph protocol (`RSSClient`) still covers the
  streaming path.

- **Beyond the original 18 plans**, later work added: two new chapters — **Ch 40 Lightning &
  Sferics** (`jansky.lightning`) and **Ch 41 Practical Calibration** (`jansky.interferometry`
  gain solvers) — real **LAB HI** data in Ch 11, a full **worked-solutions** pass across every
  chapter, and a curated **[Radio Astronomy on GitHub](../docs/github.md)** catalogue (with a
  machine-readable `docs/data/radio_github.yml`, a generated stats block, and a scheduled URL check).

- **Genuinely optional, not yet started:** a standalone cosmic-dawn/EoR chapter (Plan 11); a
  polarisation-calibration extension to Ch 41 (Plan 13); Ch 30 RASDR real-`.sps` wiring (Plan 15);
  the guarded `@interact` widgets (Plan 18 — deferred, they need a live kernel); retrofitting the
  prerequisites admonition into the headers of the older notebooks and adding Ch 40 to the
  learning-paths map (Plan 17); and more unit-test coverage for `plotting.py` (Plan 08).

The reusable subagents that built and reviewed all this live in `.claude/agents/`.
