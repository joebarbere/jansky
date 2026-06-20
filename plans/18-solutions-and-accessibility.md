# Plan 18 — Worked solutions, onboarding & accessibility 📋 Proposed

> Flagged by **pedagogy (#2 top, plus #4, #5, #6)**. Scope: medium–large (mechanical,
> parallelizable per chapter).

## Context

Three self-learner gaps, all confirmed by inspection across the 36 notebooks: **no worked
solutions** (`<details>` count is 0 — exercises are either open prompts or have answers pre-filled
inline, which spoils the attempt), **no onboarding** for someone facing 36 chapters, and **weak
accessibility** (only 1 notebook has alt text; line colours are raw matplotlib defaults with
red/green pairs; only 1 notebook uses `ipywidgets` despite highly parameter-driven content).

## Deliverables

- **Collapsible worked solutions** — adopt a consistent pattern for "Try it yourself": prompt →
  empty/scaffolded learner cell → a `<details><summary>Solution</summary>…</details>` markdown block
  (renders in both JupyterLab and mkdocs-jupyter). Roll out across chapters; make it a required
  element in `.claude/agents/notebook-author.md`.
- **"Choose your track / Start here" guide** — a new `docs/start-here.md` (linked from
  `index.md`/README) with routes like *laptop-only*, *I have an RTL-SDR*, *interferometry*,
  *pulsars & transients*, *just the physics/maths* — each an ordered chapter list. (Promotes the
  capstone's existing three-track idea to the whole course; pairs with
  [Plan 17](17-learning-journey-map.md).)
- **Accessibility pass** — add a colourblind-safe categorical cycle (Okabe–Ito / Wong) to
  `JANSKY_STYLE` in `src/jansky/plotting.py` (fixes every future figure at once); add alt text /
  descriptive captions to key figures.
- **Lightweight interactivity** — an optional, guarded `@interact` slider cell in ~6–8 high-value
  chapters (Ch 3 integrate-down, Ch 9 CLEAN loop gain, Ch 18 DM butterfly, Maths Lab A windowing),
  with the static render still working.

## Verification

- Solutions reveal/hide in both JupyterLab and the built site; the palette change is colourblind-
  safe (spot-check with a simulator); widget cells degrade gracefully in static render;
  `nbmake` + `mkdocs --strict` green. New standards captured in `notebook-author.md`.
