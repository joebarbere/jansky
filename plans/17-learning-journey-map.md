# Plan 17 — Learning-journey map & Maths-Lab wiring 📋 Proposed

> Flagged by **pedagogy (#1 top, plus #3)**. Scope: medium.

## Context

The only journey diagram (the Mermaid in `docs/index.md`) covers just the linear path 1→15.
Chapters 16–36 — half the course, including FRBs, PTAs, SETI, the CMB, the amateur-hardware track,
and the whole Maths Lab appendix — appear only as a flat nav list with non-sequential numbering
(Ch 26–30 in Part II; 17/19/25 in Part III). And only **1 of 30** science notebooks links to a
Maths Lab, despite the README calling them "the worked maths behind the chapters." Learners can't
see that Ch 18 builds on Ch 13 + Maths Lab B.

## Deliverables

- **A master course map** — extend the `docs/index.md` Mermaid (or a new `docs/learning-paths.md`)
  showing **every** chapter, its prerequisites, and themed routes; render it on the homepage.
- **Maths-Lab back-links** — each science chapter that uses a Lab links to it (Ch 18→Lab B, Ch 8/9→
  Lab A/E, Ch 3/33→Lab C, etc.), and each Lab links back to the chapters it serves.
- **Per-chapter header** — a standardized top-of-chapter admonition: *Prerequisites: Ch X, Maths
  Lab Y · ~45 min · Intermediate* (the `admonition` extension is already enabled). Add to
  `.claude/agents/notebook-author.md` as a required element so future chapters comply.
- (Bundles with the "Choose your track" guide in [Plan 18](18-solutions-and-accessibility.md).)

## Verification

- The map renders and every node links to a real chapter; back-links resolve both ways;
  `mkdocs --strict` passes (it validates the internal links/anchors).
