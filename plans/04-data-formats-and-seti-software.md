# Plan 04 — Data formats & the ecosystem ◑ Mostly delivered

Folded the provided link set (GUPPI, SETI tools, RASDR, Radio-Sky Spectrograph, SigMF, RASG,
VIRGO/PICTOR) into the course. **Shipped** (PR #11):

- **`src/jansky/formats.py`** — GUPPI raw (`read_guppi_header` / `write_guppi` /
  `iter_guppi_blocks`), SigMF (`read_sigmf` / `write_sigmf`), the Radio-Sky Spectrograph TCP
  protocol (`RSSClient` + in-process `MockRSSServer`), a `Spectrogram` container, and an optional
  `blimpy` wrapper.
- **[Chapter 16 · Data Formats & the Ecosystem](../notebooks/16_data_formats_and_ecosystem.ipynb)**
  and the [Data Formats reference page](../docs/data-formats.md).
- `pyproject` extras `seti` / `formats` / `hi`; doc cross-links from field-notes & resources.

The RSS protocol is reused again in [Chapter 30 (RASDR)](../notebooks/30_rasdr_radio_sky.ipynb),
and the VIRGO/PICTOR path in [Chapter 29](../notebooks/29_virgo_pictor.ipynb).

## ⚠ Outstanding (deferred on purpose)

`jansky.formats.read_sps` and `read_spd` raise `NotImplementedError`. The authoritative `.sps`
(Typinski 2015) and `.spd` binary layouts were not machine-readable at implementation time (the
spec link now redirects to a parked domain; RSS_Help2 is a scanned image), and we do not guess
binary formats. The live `RSSClient` protocol covers the Radio-Sky data path. **Revisit the file
readers when a verifiable spec is available.**
