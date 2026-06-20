# Plan 01 — New chapters from the research & videos lists

## Context

The course's [year-by-year papers timeline](../docs/papers-timeline.md) and
[YouTube library](../docs/videos.md) surface whole subfields of radio astronomy that the
15 chapters reference but never teach. Each video topic group and each cluster of landmark
papers is, in effect, a chapter the course is missing. This plan proposes science chapters to
close those gaps. They are mostly **archival/simulated**, so they need little or no hardware —
fitting the course's "runs on a laptop" promise.

The video groups (`videos.md`) map almost one-to-one onto the gaps: *Pulsars, FRBs &
transients*, *Black holes & the EHT*, *SETI & the search* have no dedicated chapter; the papers
timeline adds *the CMB*, *molecular-line/maser astronomy*, *solar & Jupiter radio*, and
*pulsar-timing-array nanohertz gravitational waves* as recurring landmark themes.

## Already covered (do not duplicate)

- Pulsars themselves — dispersion, dedispersion, folding — are **Ch 13**. The new transient
  chapter extends that to **FRBs and searching**, not pulsar basics.
- Interferometry and the uv-plane — **Ch 7–9**. The EHT/VLBI chapter is an *application*
  (very long baselines, closure quantities), not a re-teach of aperture synthesis.
- Multi-wavelength context — **Ch 14**.

## Proposed chapters

Each is a notebook (`notebooks/NN_slug.ipynb`) + a `videos.md`/`papers-timeline.md`
cross-reference. Suggested numbering continues after 15, or inserts into Part IV; final
ordering is the implementer's call.

### A. Fast Radio Bursts & the transient radio sky
- **Builds on:** Ch 13 (dedispersion/DM). **Pairs with:** videos "Pulsars, FRBs & transients"; papers 2007 Lorimer, 2013 Thornton, 2016 Spitler, 2020 CHIME/STARE2.
- **Learning goals:** what an FRB is; the DM–distance (Macquart) relation; single-pulse vs periodicity searches; repeaters vs one-offs; the RFI-vs-astrophysical discipline (tie to [`field-notes.md` RFI section](../docs/field-notes.md)).
- **Code:** simulate a dispersed single pulse in a dynamic spectrum (reuse `jansky` dedispersion helpers from Ch 13), run a brute-force DM search, plot the "butterfly" S/N–vs–DM. Use a real published burst profile if a small public sample can be fetched via `jansky.data`.
- **Helper additions:** `jansky.transients` (DM trial grid, boxcar matched filter, S/N) — overlaps Plan 03's matched-filter module.

### B. The Event Horizon Telescope & VLBI
- **Builds on:** Ch 8 (Fourier/uv-plane). **Pairs with:** videos "Black holes & the EHT"; papers 2019/2022 EHT.
- **Learning goals:** why VLBI reaches µas resolution; sparse uv-coverage and why imaging is hard; **closure phase & closure amplitude** (robust to station errors); the idea behind regularised imaging (the "many priors agree" approach).
- **Code:** build an Earth-scale sparse uv-coverage with `jansky.interferometry.uv_coverage`; show the dirty beam of a handful of global sites; demonstrate closure phase on a 3-station triangle being immune to per-station phase errors; CLEAN/regularise a toy ring source → recover a shadow.
- **Helper additions:** `closure_phase()`, `closure_amplitude()` in `jansky.interferometry`.

### C. SETI & technosignatures
- **Pairs with:** videos "SETI & the search"; papers context (Drake, Breakthrough Listen). Also the natural home for the **GUPPI/SETI-tools** material in [Plan 04](04-data-formats-and-seti-software.md).
- **Learning goals:** the search space (frequency × time × drift × sky); the waterfall and the **Doppler-drift** matched filter; narrowband vs broadband; RFI rejection by on/off cadence; the Drake equation as a back-of-envelope.
- **Code:** simulate a drifting narrowband tone in a high-resolution waterfall + noise; implement a simple de-drift/integrate detector; recover the injected signal; (optional, Plan 04) run `turboSETI`/`blimpy` on a real Breakthrough Listen sample.
- **Cross-link:** Allen Telescope Array in [`telescopes.md`](../docs/telescopes.md); SETI projects in [`projects.md`](../docs/projects.md).

### D. Pulsar timing arrays & nanohertz gravitational waves
- **Builds on:** Ch 13. **Pairs with:** papers 1982 Backer, 1990 Foster & Backer, 2023 NANOGrav/PPTA.
- **Learning goals:** timing residuals; why an array of millisecond pulsars is a galactic-scale GW detector; the **Hellings–Downs** angular correlation as the smoking gun.
- **Code:** simulate timing residuals for many pulsars with a common red-noise signal; compute and plot the Hellings–Downs curve from the cross-correlations.

### E. The Cosmic Microwave Background (radio/microwave view)
- **Pairs with:** papers 1965 Penzias & Wilson, 1992 COBE, 2003 WMAP.
- **Learning goals:** the CMB as the most famous radio-astronomy discovery; blackbody at 2.725 K (ties to Ch 2 Rayleigh–Jeans/brightness temperature); the dipole; anisotropy and the angular power spectrum (concept, not derivation).
- **Code:** plot the CMB blackbody with `astropy`; reuse `jansky.units` brightness-temperature tooling; show a toy anisotropy map and its power spectrum with `healpy` (optional extra).

### F. Molecular-line & maser astronomy
- **Pairs with:** papers 1968–69 NH₃/H₂O, 1970 CO, 1995 NGC 4258 maser.
- **Learning goals:** rotational transitions; CO as the tracer of molecular gas; spectral-line cubes (reuse Ch 11 `spectral-cube`); masers as compact bright probes (e.g. the NGC 4258 black-hole disk).
- **Code:** synthesize/inspect a CO position–velocity diagram; extract a rotation signature from a maser disk toy model.

### G. Solar & Jupiter radio astronomy
- **Pairs with:** papers 1946 Hey/Southworth, 1955 Burke & Franklin; **the Radio JOVE project** in [`projects.md`](../docs/projects.md) (this is the science chapter behind that hardware).
- **Learning goals:** solar radio bursts (types I–V) and the dynamic spectrum; CME shock velocity from frequency drift (a real amateur result noted in `field-notes.md`); Jupiter's decametric emission and the Io–Jupiter interaction.
- **Code:** simulate a type-II burst frequency drift and derive a shock speed; model Jovian decametric "L-bursts/S-bursts" in a spectrogram. Reads Radio JOVE **SPS** files once [Plan 04](04-data-formats-and-seti-software.md) lands the reader.

### H. Intensity interferometry (optional, advanced)
- **Pairs with:** papers 1954 Hanbury Brown & Twiss; the `field-notes.md` "interferometry is hard" discussion (HBT as a way around phase coherence).
- **Learning goals:** correlating intensity instead of amplitude+phase; why timing need only match the bandwidth; trade-offs vs amplitude interferometry.
- **Code:** simulate two detectors seeing a partially-coherent source; show the intensity correlation recovering angular size.

## Cross-cutting deliverables

- Update [`videos.md`](../docs/videos.md) and [`papers-timeline.md`](../docs/papers-timeline.md) "Pairs with" lines to point at the new chapters once they exist.
- Extend `mkdocs.yml` nav (a possible new "Part V — Frontiers" grouping for A–H).
- New optional extras in `pyproject.toml` as needed: `cmb = ["healpy"]`; SETI tools come from Plan 04.

## Verification

- Each notebook runs end-to-end on the base env (or a clearly-marked optional extra) with no
  network, via simulated/synthetic data + graceful archival fallbacks — matching the existing
  chapters' contract.
- `pytest --nbmake` smoke-tests for any chapter added to Part I-style "must run" set.
- New helper functions get unit tests in `tests/` (e.g. closure phase invariance under
  per-station phase errors; HBT correlation recovers a known angular size).
- `mkdocs build --strict` passes with the new nav entries and cross-links.
