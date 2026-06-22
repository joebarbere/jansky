# Plan 20 — Free-free radiation & HII regions chapter 📋 Proposed

> Flagged by the **ERA gap analysis** (emission mechanisms). Scope: medium.
> Pairs with [Plan 19](19-synchrotron-radiation.md) (synchrotron) as "the two continuum mechanisms".

## Context

*Essential Radio Astronomy* devotes **ERA Ch 4** to **free-free (thermal bremsstrahlung)
radiation** — the continuum from ionized gas: HII regions, planetary nebulae, the thermal Galactic
background. The jansky course mentions "free-free / thermal" only in passing in Ch 2; the key
concept **emission measure** ($\mathrm{EM} = \int n_e^2\,\mathrm{d}l$) appears in **zero**
notebooks, and there is no treatment of the optically-thick→thin turnover or the ionization balance
of an HII region. Together with [Plan 19](19-synchrotron-radiation.md) this gives the course the two
canonical continuum mechanisms — the steep, polarised, non-thermal one and the flat, unpolarised,
thermal one — and lets a learner tell them apart from a spectrum.

## Deliverables

- **New chapter** `notebooks/44_free_free_and_hii.ipynb` — suggested placement in **Part I —
  Foundations**, immediately after the synchrotron chapter ([Plan 19](19-synchrotron-radiation.md)).
- **Helper** `src/jansky/freefree.py` (tested), e.g.:
  - `freefree_optical_depth(nu_ghz, em, t_e)` — τ_ff(ν) from the emission measure and electron
    temperature.
  - `freefree_spectrum(nu_ghz, em, t_e, ...)` — brightness temperature / flux across the
    **optically-thick (T_B → T_e, S ∝ ν²) → optically-thin (flat, α ≈ −0.1)** turnover.
  - `emission_measure(...)` and `turnover_frequency(em, t_e)`.
  - `stromgren_radius(q_ionizing, n_e, ...)` — the ionization-balance radius of an HII region.
- **Notebook content:** the free-free emission/absorption coefficients (motivated, not fully
  derived); the EM and the thick→thin spectral turnover; fit EM and T_e from a model spectrum;
  Strömgren-sphere ionization balance and the ionizing-photon rate; and a **side-by-side
  flat-free-free vs steep-synchrotron** comparison (the diagnostic that separates the mechanisms,
  tying back to [Plan 19](19-synchrotron-radiation.md) and Ch 2). 5–6 captured figures.
- **Real data:** an **HII region (Orion Nebula / M42)** radio flux-vs-frequency from VizieR, fit for
  EM/T_e (offline fallback). Optionally a short **radio recombination line (RRL)** section — this
  also closes ERA Ch 7's RRL gap.
- **3 "Try it yourself" exercises** with collapsible worked solutions.
- **Wiring:** nav; references (ERA Ch 4; Mezger & Henderson 1967; Osterbrock & Ferland *AGN²*;
  Rohlfs & Wilson; Strömgren 1939); glossary (*free-free / thermal bremsstrahlung*, *emission
  measure*, *Strömgren sphere*, *radio recombination line*); learning-paths node; cross-links to
  Ch 2, Plan 19's chapter, Ch 24 (molecular/masers).

## Approach

- Build and unit-test `jansky.freefree` first (τ ∝ ν^−2.1; the T_B → T_e thick limit; flat thin
  limit; Strömgren scaling), then author the notebook, then `science-reviewer`.

## Verification

- `ruff` + `mypy` + `pytest` green; `nbmake` **fully offline** (real HII spectrum guarded);
  `mkdocs build --strict` + doc-link test green; new citation URLs verified live.
