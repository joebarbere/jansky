# Plan 02 — New chapters from the projects list

## Context

The [Projects, Kits & Hacks](../docs/projects.md) page catalogues dozens of buildable
instruments and hacks, but the course only *teaches* two hardware paths: SDR basics (Ch 5) and
the hydrogen-line telescope (Ch 6). Everything else on that page — Radio JOVE, SuperSID, meteor
scatter, KrakenSDR interferometry, RASDR, the VIRGO/PICTOR software path — is a project a
learner could do but the course never walks them through. This plan turns the most pedagogically
valuable projects into hands-on chapters.

These chapters are **optional/hardware-flavoured** like Ch 5–6: each must run end-to-end on a
plain laptop using simulated or sample data, with the real-hardware path clearly marked.

## Already covered (do not duplicate)

- **SDR fundamentals, sampling, IQ, power spectra** — Ch 5. New chapters consume SDR data, they don't re-teach the dongle.
- **Hydrogen-line horn/dish build** — Ch 6.
- **Why amateur interferometry is hard (clocks, KrakenSDR, intensity interferometry)** — discussed in [`field-notes.md`](../docs/field-notes.md); this plan turns the KrakenSDR path into an actual exercise.
- **The catalogue of kits/suppliers** — `projects.md` (reference, not a tutorial).

## Proposed chapters / hands-on modules

### A. GNU Radio flowgraphs for radio astronomy
- **From:** the GNU Radio container (`containers/gnuradio.Dockerfile`) and DSPIRA/CCERA references in `projects.md`/`field-notes.md`.
- **Goal:** build a total-power radiometer and a simple spectrometer flowgraph; understand blocks (source → filter → FFT → integrate → sink); export to a file format (hooks into [Plan 04](04-data-formats-and-seti-software.md): write GUPPI/SigMF/filterbank).
- **Runs offline:** ship a saved `.grc` + a Python-exported flowgraph that processes a bundled IQ capture; the live-SDR source is the only hardware-gated block.

### B. Coherent interferometry with KrakenSDR
- **From:** KrakenSDR entry in `projects.md`; the phase-coherence discussion in `field-notes.md`.
- **Goal:** the first *real* amateur interferometer in the course — five phase-coherent channels, calibration on a reference tone, fringes between two elements, a 1-D correlation. Connects directly back to Ch 7–8 (fringes, baselines).
- **Runs offline:** simulate 5 coherent channels with a controllable phase offset; the KrakenSDR capture path is hardware-gated.

### C. Radio JOVE — observing Jupiter & the Sun
- **From:** Radio JOVE (the flagship kit, mentioned 4× in `projects.md`). The *science* lives in [Plan 01-G](01-chapters-from-research-and-videos.md); this is the *observing/data* chapter.
- **Goal:** decametric (~20 MHz) observing; reading **SPS spectrograph files** and **Radio-SkyPipe** data ([Plan 04](04-data-formats-and-seti-software.md) provides the readers); identifying Io-related Jovian storms and solar bursts in a spectrogram; submitting to the Radio JOVE archive.
- **Runs offline:** parse and plot a bundled sample SPS/`.spd` file.

### D. Meteor scatter & passive radar
- **From:** the GRAVES/FM meteor-scatter and passive-radar hacks in `projects.md` (8 "meteor" mentions) and the `blah2` reference.
- **Goal:** detect meteor "pings" via forward-scatter off a distant transmitter; the Doppler signature; simple event detection; (stretch) cross-correlation passive radar to localize aircraft.
- **Runs offline:** simulate a meteor-ping spectrogram (rising/falling Doppler) + detection; bundle a short real capture if a clearly-licensed one exists.

### E. VLF & the ionosphere (SuperSID / INSPIRE)
- **From:** SuperSID and INSPIRE entries in `projects.md`.
- **Goal:** monitor distant VLF transmitters; detect a sudden ionospheric disturbance (SID) from a solar flare; understand sferics/tweeks/whistlers conceptually.
- **Runs offline:** simulate a VLF amplitude time-series with a flare-induced step; detect it. Optionally read a real SuperSID CSV log.

### F. The VIRGO / PICTOR software path (no-hardware HI)
- **From:** VIRGO and PICTOR (linked in `resources.md`/`field-notes.md`, never used).
- **Goal:** a zero-hardware route to a *real* hydrogen-line observation — drive the PICTOR online telescope and/or reduce data with the `astro-virgo` package — complementing the build-it-yourself Ch 6. See [Plan 04](04-data-formats-and-seti-software.md) for the dependency/extras details.
- **Runs offline:** use a cached PICTOR observation; the live request is wrapped in try/except with the cached fallback.

### G. RASDR (Radio Astronomy SDR) — overview & interop
- **From:** the `myriadrf/RASDR` repo and its RSS-protocol commit in the provided links.
- **Goal:** what RASDR is (LimeSDR-based amateur RA receiver), how it streams to **Radio-Sky Spectrograph** over the RSS TCP/IP protocol. The protocol/client implementation is specified in [Plan 04](04-data-formats-and-seti-software.md); this chapter is the hardware/context wrapper.

## Cross-cutting deliverables

- A small `jansky.sdrsim` helper (or extend `jansky.signals`) for the simulated multi-channel /
  spectrogram captures the above reuse, so each chapter stays short.
- Optional `pyproject.toml` extras already exist (`sdr`); add `sdr-extra` for `pyrtlsdr`-adjacent
  tooling only if needed. Hardware-heavy tools stay in the containers.
- Update `projects.md` to link each project entry to its new walkthrough chapter once written.
- Extend the [Visual Tour](../docs/visual-tour.md) and `videos.md` "Build it yourself" pointers.

## Verification

- Every chapter executes on the base env with simulated/sample data, hardware paths gated behind
  an availability flag (the Ch 5/12 pattern).
- `pytest --nbmake` on the lightweight ones; unit tests for any new helper (e.g. the KrakenSDR
  fringe simulator recovers the injected phase offset).
- `mkdocs build --strict` passes with new nav entries and cross-links.
