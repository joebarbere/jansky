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

## ✅ Resolved — the SPS/SPD readers (was deferred)

`jansky.formats.read_sps` and `read_spd` were initially deferred (the binary spec was not
machine-readable at the time). They are now **implemented** — see
[Plan 15](15-sps-spd-readers.md). The layout was recovered from an open reference
implementation (`maserlib/maser4py`) and `read_sps` is validated byte-for-byte against a real
Radio JOVE recording (AJ4CO/Typinski via MASER, registered as the `radiojove-sps` dataset). The
live `RSSClient` protocol still covers the streaming Radio-Sky data path.
