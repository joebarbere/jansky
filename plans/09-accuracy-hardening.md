# Plan 09 — Scientific-accuracy hardening ✅ Delivered

> Flagged by **science-rigor (#2 top, plus #3–#6)**. Scope: small–medium.
>
> **Delivered:**
> - **`src/jansky/constants.py`** — single source of truth (`DM_CONST`, `FP_COEFF_MHZ`,
>   `R_SUN_KM`, the Newkirk `A`/`B`, `CO_J10_GHZ`, `MACQUART_SLOPE`), each with a provenance
>   comment; `transients`, `solar`, and `molecular` now import from it (re-exporting their old
>   names for back-compat).
> - **`tests/test_accuracy.py`** — published-value tests: NGC 4258 central mass (~4×10⁷ M☉),
>   the Hellings–Downs 90° value (≈ −0.145, anti-correlated), a 1.4 GHz Tb↔flux Jy anchor, the
>   canonical 4.15 ms dispersion delay, a real-FRB Macquart redshift, and a 1500 km/s type-II
>   shock recovery. Plus a test that the modules share the centralised constants.
> - **YMW16** (Yao, Manchester & Wang 2017) added to `references.md` as the current-standard
>   DM→distance model over NE2001.
> - **Macquart slope** docstring now flags the ~900 pc cm⁻³/z value as cosmology/baryon-fraction
>   *model-dependent*.
>
> **Scoped out (intentionally):** the CMB-dipole reconciliation — notebook 22 is already
> self-consistent (the "≈ 3.4 mK" is an explicit rounded hand-calc immediately followed by the
> precise 3.3615/3.3621 mK from v = 369.82 km/s); the HD normalization is already documented in
> `timing.py`; and Ch 13/18 never call NE2001 "the standard", so there was nothing to soften.
> YMW16 was added to the bibliography but not the year-by-year timeline, which is curated as the
> top-3 papers per year.

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
