# Plan 02 — Chapters from the projects list ✅ Delivered

Hardware/amateur chapters from [Projects, Kits & Hacks](../docs/projects.md). **All shipped**
(PRs #12, #20, #21), each optional/offline like Chapters 5–6.

| § | Chapter | Helper added |
|---|---|---|
| A | [28 · GNU Radio Flowgraphs](../notebooks/28_gnuradio_flowgraphs.ipynb) | (reuses `jansky.formats`) |
| B | [17 · Coherent Interferometry (KrakenSDR)](../notebooks/17_coherent_interferometry_kraken.ipynb) | `interferometry.simulate_coherent_channels`, `calibrate_phases`, `estimate_source_angle` |
| C | Radio JOVE | covered by the science chapter [23 · Solar & Jupiter](../notebooks/23_solar_and_jupiter.ipynb) (+ SPS path in Plan 04) |
| D | [26 · Meteor Scatter & Passive Radar](../notebooks/26_meteor_scatter.ipynb) | `jansky.meteor` |
| E | [27 · VLF & the Ionosphere (SuperSID)](../notebooks/27_vlf_ionosphere.ipynb) | `jansky.vlf` |
| F | [29 · No-Hardware HI: VIRGO & PICTOR](../notebooks/29_virgo_pictor.ipynb) | (reuses `jansky.data`) |
| G | [30 · RASDR & Radio-Sky Spectrograph](../notebooks/30_rasdr_radio_sky.ipynb) | (reuses `jansky.formats.RSSClient` / `MockRSSServer`) |

Every chapter runs offline with simulated/sample data; real-hardware paths are clearly gated.
Nothing outstanding.
