# Start here

Welcome. **jansky** is a hands-on radio-astronomy course — 39 chapters plus a six-part Maths
Lab — and you do **not** have to read it all, or in order. This page helps you pick a path that
fits your goal and your hardware. (Spoiler: a laptop is all you need.)

## 1. Set up (10 minutes)

Install the environment once — local with [uv](https://docs.astral.sh/uv/) or via containers —
following the [Setup](setup.md) page. Then open **Chapter 1** and you're going.

Everything runs **fully offline**: chapters that touch a telescope archive or real hardware fall
back to bundled or simulated data, so nothing stalls without a network connection.

## 2. Choose your track

Pick the row that sounds most like you. Each links to an **ordered** chapter list on the
[Learning Paths](learning-paths.md) page (which also has the full course map).

| If you want to… | Start with | Track |
|---|---|---|
| **Learn the fundamentals first** (recommended) | Chapters 1 → 2 → 3 | Foundations, then branch anywhere |
| **Do everything on a laptop, no hardware** | The laptop-only route | [🛋️ Laptop-only](learning-paths.md#laptop-only-no-hardware-fully-offline) |
| **Use an RTL-SDR you already own** | Chapters 1–6, then the projects | [📡 RTL-SDR](learning-paths.md#i-have-an-rtl-sdr-hands-on-hardware) |
| **Understand interferometers & imaging** | Chapter 7 onward | [🛰️ Interferometry](learning-paths.md#interferometry-imaging) |
| **Chase pulsars, FRBs & the nanohertz sky** | Chapters 13, 18, 20 | [⏱️ Transients](learning-paths.md#pulsars-transients-the-nanohertz-sky) |
| **Just do the physics & maths** | Chapters 1–3 + the Maths Lab | [🔭 Physics & maths](learning-paths.md#just-the-physics-maths) |
| **See pictures before prose** | The Visual Tour | [Visual Tour](visual-tour.md) |

Not sure? Take the **Foundations** track (Chapters 1–3). Almost everything else branches off it,
and you'll know within an hour whether radio astronomy is your thing (it is).

## 3. How to work through a chapter

Each chapter is an executable notebook with the same rhythm:

1. **Read** the orientation and the physics (equations included, motivated not just stated).
2. **Run** the code cells top-to-bottom — change numbers and re-run; that's the point.
3. **Try it yourself** — every chapter ends with exercises. Attempt them before peeking at the
   collapsible **Solution** blocks.
4. **Recap**, then follow the cross-links to where the ideas go next.

The **Maths Lab** appendices (A–F) are the worked maths behind the chapters — dip into one
whenever a derivation feels too fast.

## 4. Where to get unstuck

- The [Glossary](glossary.md) defines every term; [Reading the Notation](notation.md) decodes the
  symbols.
- The [Bibliography](references.md) links the seminal papers each chapter cites.
- Found a bug or a dead link? Open an issue — see [CONTRIBUTING](https://github.com/joebarbere/jansky/blob/main/CONTRIBUTING.md).

Radio astronomy is one of the friendliest corners of astrophysics for a programmer: the data are
signals, the maths is Fourier transforms, and the tools are open source. Welcome aboard. 📡
