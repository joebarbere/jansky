# Plan 19 — Synchrotron radiation chapter 📋 Proposed

> Flagged by the **ERA gap analysis** (emission mechanisms). Scope: medium.
> Pairs with [Plan 20](20-free-free-and-hii.md) (free-free) as "the two continuum mechanisms".

## Context

*Essential Radio Astronomy* (Condon & Ransom) — the course's cited companion text — devotes a
whole chapter (**ERA Ch 5**) to **synchrotron radiation**, the dominant *non-thermal* continuum
mechanism: supernova remnants, AGN jets and lobes, radio galaxies, and the diffuse Galactic
background. The jansky course only *names* it (Ch 2 introduces "thermal vs non-thermal" and the
spectral index, and `equipartition` appears nowhere else; there is no derivation of the spectrum,
no spectral aging, no minimum-energy field). This is the single clearest physics gap relative to
ERA, and it connects backward to Ch 2 and forward to Ch 19 (AGN), Ch 22/42 (synchrotron
foregrounds), and Ch 37 (synchrotron polarisation).

## Deliverables

- **New chapter** `notebooks/43_synchrotron_radiation.ipynb` — suggested placement in **Part I —
  Foundations** right after Ch 2 (the emission-physics deepening it promises), or as the head of a
  small "emission mechanisms" pairing with Plan 20.
- **Helper** `src/jansky/synchrotron.py` (tested), e.g.:
  - `spectral_index(p)` → α = −(p−1)/2, and `electron_index(alpha)` (the inverse).
  - `synchrotron_spectrum(nu, s_norm, alpha, nu_ssa=None)` — a power law with an optional
    synchrotron-self-absorption (SSA) low-frequency turnover (∝ ν^{5/2} below ν_ssa).
  - `spectral_break(...)` / an aged spectrum — the steepening above the break frequency from
    radiative losses (a simplified JP/KP injection-vs-aged model).
  - `equipartition_field(flux, ang_size, distance, alpha, ...)` — the minimum-energy / equipartition
    magnetic field.
  - `brightness_temperature_limit()` ≈ 10¹² K — the inverse-Compton-catastrophe ceiling.
- **Notebook content:** the relativistic electron energy spectrum N(E) ∝ E^−p → the emitted
  power-law S ∝ ν^α (derive α ↔ p); the SSA turnover (why compact sources self-absorb at low ν);
  spectral aging / the cooling break (injection vs aged spectra); the minimum-energy field from
  flux + size + spectrum; and the 10¹² K limit / inverse Compton. 5–6 captured figures.
- **Real data:** fit a real **supernova-remnant (Cas A)** or **radio-galaxy (Cygnus A / 3C
  sources)** radio spectrum from VizieR/NED (reuse the `astroquery` cone-search pattern from
  Ch 10/14), recover the spectral index and electron index, with an offline fallback.
- **3 "Try it yourself" exercises** with collapsible worked solutions.
- **Wiring:** nav; references (ERA Ch 5; Rybicki & Lightman 1979; Pacholczyk 1970; Burbidge 1956
  on equipartition); glossary (*synchrotron self-absorption*, *spectral aging / cooling break*,
  *equipartition / minimum-energy field*, *inverse-Compton catastrophe*); learning-paths node;
  cross-links to Ch 2, 19, 22, 37, 42; a Maths-Lab back-link if one applies.

## Approach

- Build and unit-test `jansky.synchrotron` first (α↔p round-trip; SSA turnover shape; equipartition
  scaling; the IC limit), then author the notebook (`notebook-author`), then `science-reviewer`.
- Keep the radiative-transfer / spectral-aging treatment at the standard teaching level (simplified
  JP/KP), clearly flagged.

## Verification

- `ruff` + `mypy` + `pytest` (incl. the helper tests) green; `nbmake` runs the chapter **fully
  offline** (the real spectrum guarded with a fallback); `mkdocs build --strict` + the doc-link test
  green; every new reference/citation URL verified live.
