# Plan 09 — Scientific-accuracy hardening 📋 Proposed

> Flagged by **science-rigor (#2 top, plus #3–#6)**. Scope: small–medium.

## Context

The test suite is strong on *internal* consistency (round-trips, scaling laws, monotonicity) but
rarely anchors to a *published* value — and a wrong shared constant round-trips happily. A few
specific accuracy/currency issues also stand out across chapters and helpers.

## Deliverables

### Published-value tests (the core)

Add targeted `assert np.isclose(..., literature_value)` tests:

- `molecular`: NGC 4258 masers (r ≈ 0.2 pc, v ≈ 1000 km/s) → central mass ≈ **4×10⁷ M☉**.
- `timing`: the Hellings–Downs minimum near **90° (≈ −0.13 / anti-correlation)**, not just Γ(0).
- `units`: a hand-computed brightness-temperature ↔ flux at 1.4 GHz lands on the expected **Jy**.
- `transients`: `macquart_redshift` gives a sensible **z** for a real burst's DM.
- `solar`: a type-II drift for a known shock speed recovers it (already partly covered — pin to a
  published CME example).

### Targeted fixes

- **YMW16** — add Yao, Manchester & Wang (2017) to `references.md`/`papers-timeline.md` and note it
  (not NE2001) is the current standard DM→distance model; soften "the standard" wording in Ch 13/18.
- **CMB dipole** (`notebooks/22`) — reconcile the two stated amplitudes (3.36 vs 3.4 mK) to the
  Planck 2018 value (v = 369.8 km/s, ΔT = 3.362 mK); optionally bump T₀ to 2.72548 K (Fixsen 2009).
- **Hellings–Downs normalization** — state the convention (`Γ(0)=1`, cross-term ½ at 0⁺) in
  `timing.py` and `notebooks/20`, and how it maps to the NANOGrav 15 yr figure.
- **Macquart slope** — flag the hard-coded `900 pc cm⁻³ per z` in `transients.macquart_redshift` and
  Ch 18 as cosmology/baryon-fraction *model-dependent*, not a universal constant.

### Single source of truth for constants

- New **`src/jansky/constants.py`** collecting `DM_CONST` (4148.808), the plasma-frequency
  coefficient (8.977e-3), `R_SUN_KM`, `CO_J10`, etc., each with a provenance comment; re-import them
  in `transients`, `solar`, `molecular`, … so the package and the prose can't silently diverge.

## Verification

- New tests pass and would fail if a shared constant were perturbed; `mkdocs --strict` ok; the
  reconciled CMB numbers agree across the chapter.
