# Plan 01 — Chapters from the research & videos lists ✅ Delivered

Science chapters mined from the [papers timeline](../docs/papers-timeline.md) and
[YouTube library](../docs/videos.md). **All eight shipped** (PRs #13–#19), each runnable offline.

| § | Chapter | Helper added |
|---|---|---|
| A | [18 · Fast Radio Bursts](../notebooks/18_fast_radio_bursts.ipynb) | `jansky.transients` (DM search, matched filter, Macquart) |
| B | [19 · The EHT & VLBI](../notebooks/19_eht_and_vlbi.ipynb) | `interferometry.closure_phase` / `closure_amplitude` |
| C | [21 · SETI](../notebooks/21_seti.ipynb) | `jansky.seti` (Doppler-drift search, ON/OFF cadence) |
| D | [20 · Pulsar Timing Arrays](../notebooks/20_pulsar_timing_arrays.ipynb) | `jansky.timing` (Hellings–Downs) |
| E | [22 · Cosmic Microwave Background](../notebooks/22_cosmic_microwave_background.ipynb) | `units.planck_brightness` |
| F | [24 · Molecular Lines & Masers](../notebooks/24_molecular_and_masers.ipynb) | `jansky.molecular` (CO ladder, Keplerian maser mass) |
| G | [23 · Solar & Jupiter](../notebooks/23_solar_and_jupiter.ipynb) | `jansky.solar` (Newkirk density, CME shock speed) |
| H | [25 · Intensity Interferometry](../notebooks/25_intensity_interferometry.ipynb) | `interferometry.disk_visibility` / `hbt_g2` |

Each chapter cites its seminal papers, reuses the helper module above, and is covered by unit
tests + an `nbmake` smoke test. Nothing outstanding.
