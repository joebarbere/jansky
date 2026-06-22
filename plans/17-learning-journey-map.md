# Plan 17 — Learning-journey map & Maths-Lab wiring ◑ Mostly delivered

> Flagged by **pedagogy (#1 top, plus #3)**. Scope: medium.
>
> **Delivered:**
> - **Master course map** — new **`docs/learning-paths.md`**: a full Mermaid over **all 36
>   chapters** with prerequisites and dashed edges to the Maths Lab, plus five **themed routes**
>   (laptop-only, RTL-SDR, interferometry, pulsars & transients, just the physics) and a
>   **Maths-Lab → chapter** service table (the "Ch 18 builds on Ch 13 + Lab B" visibility, in one
>   page). Wired into `mkdocs.yml` nav and linked from `docs/index.md`.
> - **Per-chapter header standard** — added the standardized prerequisites admonition
>   (*Prerequisites · Maths Lab · time · difficulty*) and the Maths-Lab back-link requirement to
>   `.claude/agents/notebook-author.md`, so every future chapter complies.
>
> **Prerequisites admonition — retrofitted (done).** The standard "Before you start" admonition
> (*Prerequisites · Maths Lab · time · difficulty*) is now in the header of **every** notebook: the
> 36 older chapters were back-filled via an agent fan-out (prerequisites derived from this plan's
> map and Maths-Lab service table), and Ch 40–42 ship with it by default. Additive (title cell only),
> `nbmake` + `mkdocs --strict` green. The map also now includes the Ch 40 node.
>
> **Remaining (optional):** the **bidirectional in-notebook back-links** between each science chapter
> and the Lab(s) it uses — the map and the service table already give learners this centrally.

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
