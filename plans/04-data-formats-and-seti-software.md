# Plan 04 — Data formats & the radio-astronomy software ecosystem

## Context

This plan responds directly to the provided link set. Those links are not a grab-bag — they
cluster tightly around one real gap in the course: **the data formats and software that radio
astronomers (especially amateurs) use to record, exchange, and analyse data.** The course
currently teaches three formats in passing — FITS, the CASA Measurement Set (Ch 12), and
PSRFITS (Ch 13) — but never the SDR-era and amateur formats the links describe: GUPPI raw,
SIGPROC filterbank, the Radio-Sky Spectrograph `.sps`/`.spd` formats and its live TCP protocol,
SigMF, and the `pyuvdata`/RASG interchange layer. None of the SETI software stack
(`rawspec`/`blimpy`/`turboSETI`) is covered, and VIRGO/PICTOR are linked but never *used*.

### The provided links, mapped

| Link | What it gives us | Status now | Deliverable |
|---|---|---|---|
| Estévez — *Writing GUPPI files with GNU Radio & using SETI tools* | GUPPI raw voltage format; the `rawspec → blimpy → turboSETI` pipeline | ❌ | `formats.read_guppi_header`; SETI section of the new chapter |
| RASG GitHub Pages | `pyuvdata`, `pyradiosky`, RFI tools — the modern interchange ecosystem | ❌ | "ecosystem" section; `formats` extra (`pyuvdata`) |
| pictortelescope.com | PICTOR free online HI telescope (uses VIRGO) | ⚠️ linked only | hands-on HI observation (also [Plan 02-F](02-chapters-from-projects.md)) |
| casa.nrao.edu | CASA | ✅ **Ch 12** | none — already covered; reference it |
| VIRGO docs (install) | `astro-virgo` single-dish package | ⚠️ linked only | `hi` extra; reduce a real HI obs |
| cygnusa.blogspot — Amateur Radio Astronomy | amateur observing; RSS how-to | ❌ | RSS protocol context |
| radiojove.org — *SPS File Format (Typinski 2015)* | the `.sps` spectrograph format spec | ❌ | `formats.read_sps`/`write_sps` |
| radiosky.com — *RSS_Help2.pdf* | Radio-Sky Spectrograph; `.spd` format | ❌ | `formats.read_spd`; RSS reference |
| cygnusa — *How to Talk to Radio-Sky Spectrograph* | the RSS **TCP/IP protocol** | ❌ | `formats.RSSClient` |
| myriadrf/RASDR commit — *TCP socket using RSS protocol* | reference implementation of the RSS socket | ❌ | `RSSClient` protocol details |
| myriadrf/RASDR repo | Radio Astronomy SDR (LimeSDR) | ❌ | hardware context ([Plan 02-G](02-chapters-from-projects.md)) |

**Only CASA is already covered.** Everything else is new and coherent — this plan makes it a
single chapter plus a reusable helper module.

## Already covered (do not duplicate)

- **FITS / Measurement Set / CASA** — Ch 12 + [`resources.md`](../docs/resources.md). The new
  chapter *references* the MS as one node in the format landscape and uses `pyuvdata` to convert
  to/from it, but does not re-teach CASA imaging.
- **PSRFITS, dedispersion, folding** — Ch 13.
- **IQ data & SDR basics** — Ch 5. GUPPI raw is introduced as "what you write *after* the IQ
  stream is channelized."
- **VIRGO/PICTOR as catalogue links** — `resources.md`, `field-notes.md`. This plan *uses* them.

## Deliverable 1 — `src/jansky/formats.py` (new helper module)

A small, dependency-light module with readers/writers for the formats above; heavy tools are
optional imports guarded with a clear message.

```text
read_guppi_header(path) -> dict          # parse the 80-char ASCII cards of a GUPPI raw file
iter_guppi_blocks(path)                  # yield (header, voltage_block) lazily
read_filterbank(path)                    # thin wrapper over blimpy (optional); numpy header fallback
read_sps(path) -> Spectrogram            # Radio-Sky Spectrograph .sps  (Typinski 2015 spec)
write_sps(path, data, meta)              # round-trippable .sps writer
read_spd(path)                           # Radio-SkyPipe strip-chart .spd
read_sigmf(path) / write_sigmf(...)      # SigMF (via `sigmf` if present, else minimal JSON+raw)
class RSSClient:                         # speak the Radio-Sky Spectrograph TCP/IP protocol
    connect(host, port); send_spectrum(freqs, power); close()
```

Notes for the implementer:
- **GUPPI raw**: header is FITS-like 80-byte ASCII cards (`BLOCSIZE`, `OBSNCHAN`, `NPOL`,
  `OBSFREQ`, `TBIN`, …) terminated by `END`, then a binary data block of `BLOCSIZE` bytes;
  repeat. Parse headers without a heavy dep; only touch the voltages lazily. Follow the field
  set used in the Estévez write-up / the GBT GUPPI spec.
- **SPS**: implement strictly to *Typinski (2015), "SPS File Format Description"* (radiojove.org)
  — header block + per-record spectra. Provide `write_sps` so `read_sps(write_sps(x)) == x`
  (the basis of the unit test).
- **RSSClient**: implement the framing/protocol documented in *"How to Talk to Radio-Sky
  Spectrograph"* and the `myriadrf/RASDR` commit (`61676c4`, "serve a TCP/IP socket using the
  RSS protocol"). Ship a **mock RSS server** in the test/notebook so the client path runs with
  no external software.
- Return small dataclasses (e.g. `Spectrogram(times, freqs, power, meta)`) consistent with the
  rest of `jansky`.

## Deliverable 2 — new chapter notebook

`notebooks/16_data_formats_and_ecosystem.ipynb` — **"Data formats & talking to the ecosystem."**
Builds on Ch 5 (IQ), Ch 12 (MS), Ch 13 (PSRFITS). Sections, all runnable offline:

1. **The format landscape** — a diagram (Mermaid in the docs page) of the pipeline:
   raw voltages (**GUPPI raw**) → channelized (**filterbank / HDF5 / UVH5**) → spectra
   (**.sps / .spd**) → calibrated visibilities (**UVFITS / Measurement Set**), with **SigMF** as
   the open interchange and **PSRFITS** for pulsars.
2. **GUPPI raw, hands-on** — write a tiny GUPPI raw file (header cards + a few simulated complex
   voltage blocks, following Estévez's GNU Radio approach conceptually), then `read_guppi_header`
   it back. Optionally reduce to a filterbank with `rawspec`/`blimpy` (guarded `seti` extra).
3. **A SETI drift search** — load a bundled tiny waterfall (or the Plan 01-C simulation); run a
   Doppler-drift detector; optionally run real `turboSETI` on a small Breakthrough Listen sample
   (guarded). Cross-links [Plan 01-C SETI](01-chapters-from-research-and-videos.md).
4. **Radio JOVE / Radio-Sky Spectrograph** — read & plot a bundled `.sps` Jupiter/solar
   spectrogram with `read_sps`; then **stream a simulated spectrum to Radio-Sky Spectrograph**
   with `RSSClient` against the in-notebook mock server (so it runs with nothing installed).
   Cross-links [Plan 02-C Radio JOVE](02-chapters-from-projects.md).
5. **The ecosystem (`pyuvdata`/RASG)** — round-trip a small visibility dataset
   UVFITS ↔ Measurement Set ↔ UVH5 with `pyuvdata` (guarded `formats` extra); point to the RASG
   org for `pyradiosky`/RFI tooling.
6. **No-hardware HI with VIRGO/PICTOR** — reduce a cached PICTOR/`astro-virgo` HI observation;
   the live request is wrapped in try/except with the cached fallback. Cross-links
   [Plan 02-F](02-chapters-from-projects.md) and Ch 6/11.

## Deliverable 3 — `pyproject.toml` optional extras

```toml
seti     = ["blimpy", "turbo_seti"]   # GUPPI/filterbank I/O + Doppler-drift search
formats  = ["pyuvdata", "sigmf"]      # visibility interchange + SigMF
hi       = ["astro-virgo"]            # VIRGO single-dish HI/continuum (PICTOR's engine)
```

Keep them optional (some need compilers/GPU); document a container path for the heavy ones,
mirroring the CASA/GNU Radio container pattern. The base chapter must run without any of them.

## Deliverable 4 — docs

- **New page `docs/data-formats.md`** — a reference table of radio-astronomy data formats
  (GUPPI raw, SIGPROC filterbank, UVH5/HDF5, PSRFITS, Measurement Set, UVFITS, SigMF, `.sps`,
  `.spd`) with *what / produced by / read with / spec link*, citing the provided primary
  sources (Typinski 2015, RSS_Help2, the Estévez post, RASG). Add to the Reference nav.
- **Extend `field-notes.md`** "Software & tools the community actually uses" with GUPPI/SETI
  tools, RASDR, the RSS protocol, and `pyuvdata`/RASG.
- **Extend `resources.md`** software table with `blimpy`, `turbo_seti`, `pyuvdata`, `astro-virgo`,
  and RASDR; add RASG to communities.
- **Add the provided links** to `references.md` (data & software section) as authoritative
  format references.

## Verification

- `read_sps`/`write_sps` round-trip is exact (unit test); `read_guppi_header` parses a
  fixture file's cards correctly; `RSSClient` exchanges a frame with the bundled mock server.
- The chapter runs end-to-end on the **base env with no network and no optional extras** (all
  heavy tools and live services gated with cached/mock fallbacks); `pytest --nbmake` covers it.
- `uv run pytest` (new `tests/test_formats.py`) and `uv run ruff check .` pass.
- `mkdocs build --strict` passes with the new `data-formats.md` page and cross-links.

## Out of scope / cautions

- Do **not** vendor large sample datasets into the repo — fetch small samples via `jansky.data`
  with offline synthetic fallbacks (the existing pattern).
- Implement `read_sps`/RSS strictly from the cited specs; if a detail is ambiguous, ship the
  reader with a clearly-marked TODO rather than guessing the binary layout.
- `turboSETI`/`blimpy`/`pyuvdata` are optional by design — never let the base course depend on them.
