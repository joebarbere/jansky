# Plan 18 — Worked solutions, onboarding & accessibility ◑ Infrastructure delivered

> Flagged by **pedagogy (#2 top, plus #4, #5, #6)**. Scope: medium–large (mechanical,
> parallelizable per chapter).
>
> **Delivered (the cross-cutting infrastructure):**
> - **Colourblind-safe palette** — `src/jansky/plotting.py` now sets an Okabe–Ito (Wong 2011)
>   `axes.prop_cycle` in `JANSKY_STYLE` (exposed as `plotting.COLORBLIND_CYCLE`), so every figure
>   that calls `use_jansky_style()` gets a colour-vision-safe line cycle for free — no red/green
>   reliance. Unit-tested.
> - **Onboarding** — new **`docs/start-here.md`** "choose your track" guide (set-up → pick a route →
>   how to work a chapter → where to get unstuck), wired into the nav (second item), the homepage,
>   and the README, and cross-linked to the [Plan 17](17-learning-journey-map.md) track anchors.
> - **Author standards** — `.claude/agents/notebook-author.md` now *requires* the collapsible
>   `<details><summary>Solution</summary>…</details>` pattern for every exercise (prompt →
>   scaffold → hidden solution, not a pre-filled answer), descriptive figure captions / alt text,
>   and the colourblind cycle. Future chapters comply by default.
>
> **Worked-solutions rollout — done.** Collapsible `<details>Solution` blocks were retrofitted into
> the "Try it yourself" sections of **every chapter that has exercises** (PRs #52–#58, via parallel
> `claude` agents that verified each answer against the venv) — 85+ solution blocks across the course.
> The two chapters added since (Ch 40 Lightning, Ch 41 Calibration) ship with solutions by default.
> **Optional remaining:** a sweep of alt-text captions on older figures.

## Context

Three self-learner gaps, all confirmed by inspection across the 36 notebooks: **no worked
solutions** (`<details>` count is 0 — exercises are either open prompts or have answers pre-filled
inline, which spoils the attempt), **no onboarding** for someone facing 36 chapters, and **weak
accessibility** (only 1 notebook has alt text; line colours are raw matplotlib defaults with
red/green pairs).

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

## Verification

- Solutions reveal/hide in both JupyterLab and the built site; the palette change is colourblind-
  safe (spot-check with a simulator); `nbmake` + `mkdocs --strict` green. New standards captured in
  `notebook-author.md`.
