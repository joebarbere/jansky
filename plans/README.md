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
| [04 — data formats & SETI software](04-data-formats-and-seti-software.md) | ◑ Mostly complete | Chapter 16 + `jansky.formats`; **`.sps`/`.spd` file readers deferred** (no verifiable spec) |

## What the plans added

**10 new helper modules / capabilities** in `src/jansky/`: `formats`, `transients`, `timing`,
`seti`, `solar`, `molecular`, `meteor`, `vlf`, `rfi`, plus coherent-interferometry, closure
quantities, HBT intensity interferometry, a point-source gain solver, and `units.planck_brightness`.

**21 new chapters** (16–36) taking the course from 15 → 36 chapters, every one runnable fully
offline, all covered by `pytest`/`nbmake` and the strict docs build.

## Outstanding follow-up

- **Plan 04:** `jansky.formats.read_sps` / `read_spd` remain `NotImplementedError` stubs — the
  authoritative SPS (Typinski 2015) and SPD binary specs were not machine-readable, and we don't
  guess binary layouts. The live Radio-Sky Spectrograph protocol (`RSSClient`) covers the data
  path. Revisit if a readable spec surfaces.

The reusable subagents that built and reviewed all this live in `.claude/agents/`.
