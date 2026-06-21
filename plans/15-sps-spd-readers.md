# Plan 15 — Implement the SPS/SPD readers ✅ Delivered

> Flagged by **archive/real-data (#2 top)**. Scope: medium–large. Closes the one outstanding item
> from [Plan 04](04-data-formats-and-seti-software.md).
>
> **Delivered (2026-06-21):**
> - **`jansky.formats.read_sps` / `read_spd`** implemented, returning the `Spectrogram` dataclass.
>   The layout was recovered clean-room from the open reference (`maserlib/maser4py`) — see the
>   *Confidence* section below for the full spec. `read_sps` handles single- and dual-polarisation
>   files (feeds in `meta["feeds"]`, descending Hz axis, sync-delimiter check); `read_spd` handles
>   the int16/float64 × timestamp/no-timestamp variants.
> - **Validated byte-for-byte against a real recording:** a network-gated test fetches the real
>   AJ4CO/Typinski Jupiter `.sps` (registered as the `radiojove-sps` dataset in `jansky.data`) and
>   confirms author, 300 channels, dual-pol, 16–32 MHz, the 0xFEFE sync on every sweep, and that
>   the recovered `nstep` (10412) equals the `SWEEPS` metadata. `read_spd` is round-trip tested
>   against synthetic files built to the documented layout (no public real `.spd` sample found yet).
> - **Docs/records updated:** `docs/data-formats.md` (deferral note → "implemented"); Plan 04's
>   outstanding item marked resolved.
>
> **Chapter wiring (Ch 23):** Chapter 23 (Solar & Jupiter) now ends its Jupiter section by loading
> the **real** AJ4CO `.sps` recording with `read_sps`, background-subtracting it, and plotting the
> 16–32 MHz dynamic spectrum — so the course shows a genuine Radio JOVE observation alongside the
> simulated storms (offline fallback preserved).
>
> **Remaining follow-up:** the same wiring for Ch 30 (RASDR) if desired; and validating `read_spd`
> against a real `.spd` if one surfaces. Verification: `ruff` + `mypy` + full `pytest` (incl. the
> real-sample test) + `nbmake` on Ch 23 + `mkdocs --strict` green.

## Context

`jansky.formats.read_sps` / `read_spd` currently raise `NotImplementedError` — we deferred them in
Plan 04 because the authoritative binary specs weren't machine-readable and we don't guess binary
layouts. That deferral was correct, but the archive review **verified a real, openly-browsable
sample now exists** to validate against: the **MASER Radio JOVE PDS4 bundle**
(`maser.obspm.fr/data/radiojove/radiojove-aj4co-dps/`, live), which ships a `Readme_2.0.txt` + a
`data/` tree of real `.sps`/`.spd`/CDF files. This is the format for the amateur, do-it-yourself
decametric data the course champions (Radio JOVE).

## Deliverables

- **Implement `read_sps` / `read_spd`** in `src/jansky/formats.py`, reverse-engineered and
  **validated byte-for-byte against the real MASER sample** (cross-checked with the SPS/SPD format
  notes on `radiojove.gsfc.nasa.gov`). Return the existing `Spectrogram` dataclass.
- Register **one small real `.spd`/`.sps`** sample in `jansky.data` (see
  [Plan 14](14-real-data-starter-set.md)).
- **Round-trip / parse tests** against the real sample (header fields, channel count, time axis).
- **Wire into chapters** — Ch 23 (Solar & Jupiter) and Ch 30 (RASDR) read a real Jupiter/solar
  observation instead of only streaming a simulation.
- Update `docs/data-formats.md` (remove the "deferred" note for the file readers) and the Plan 04
  delivered record.

## Confidence: HIGH — the format is fully specified (GitHub research, 2026-06-21)

The deferral in Plan 04 assumed no machine-readable spec. That is **no longer true**: the
**`maserlib/maser4py`** package ships an authoritative, openly-licensed RadioJOVE SPS/SPD parser at
`src/maser_data/src/maser/data/radiojove/data.py`
([raw](https://raw.githubusercontent.com/maserlib/maser4py/master/src/maser_data/src/maser/data/radiojove/data.py)),
which — together with the MASER sample and `radiosky.com/skypipehelp/V2/datastructure.html` — pins
down every field. maser4py is CeCILL (copyleft), so we **clean-room reimplement from the format
facts** (struct layouts and field meanings are not copyrightable), not copy its code.

### Primary header — 156 bytes, **little-endian**, `struct` fmt `"<10s6d1h10s20s20s40s1h1i"`

| field | type | notes |
|---|---|---|
| `sft` | `10s` | software ID string |
| `start`, `stop` | `2 × d` | decimal days since 1899-12-30 00:00; **+2415018.5 → Julian Date** |
| `lat`, `lon`, `chartmax`, `chartmin` | `4 × d` | |
| `timezone` | `h` | |
| `source`,`author`,`obsname`,`obsloc` | `10s,20s,20s,40s` | strip `\x00` and spaces |
| `nchannels` | `h` | |
| `note_length` | `i` | length (bytes) of the notes block that follows |

### Notes block (`note_length` bytes)
Free text, then KV pairs bracketed by `*[[*` … `*]]*`, **pairs delimited by `0xFF`**.
- **SPS keys:** `SWEEPS, LOWF, HIF, STEPS, RCVR, DUALSPECFILE, COLORGAIN, COLOROFFSET, BANNER, ANTENNATYPE, COLORFILE, CAXF/CAX1/CAX2, …` (some multi-value, some int/float).
- **SPD keys:** `CHL<n>`, `CHO<n>`, `Logged Using UT`, `No Time Stamps`, `Integer Save`, `XALABEL`, `YALABEL`, `MetaData_<key>\xc8<value>`.

### Data records (after header + notes)
- **SPS (spectrogram):** `nfreq = nchannels`; `nfeed = 2 if DUALSPECFILE else 1`. Each step =
  `nfreq·nfeed + 1` samples of **big-endian `uint16` (`>H`)** — the **+1 trailing sync value per
  sweep, and the samples are big-endian even though the header is little-endian** (the non-obvious
  gotcha that makes validating against the real sample essential). `nstep = data_length //
  bytes_per_step`. Frequency axis: linear `HIF → LOWF` over `nfreq` (Hz → MHz). Time axis: linear
  `start → stop` over `nstep`.
- **SPD (time series, JOVE kits):** `nfreq = 1`, `nfeed = nchannels`. Sample dtype is `int16` if
  *Integer Save* else `float64`; each step is optionally prefixed by an `8-byte float64` UT
  timestamp unless *No Time Stamps*. Fixed `frequency = 20.1 MHz`.

(Note: maser4py's own SPD branch has a key-name mismatch — it reads `INTEGER_SAVE_FLAG` /
`NO_TIME_STAMPS_FLAG` but the note extractor writes `Integer Save` / `No Time Stamps` — so SPD
needs care; normalise the note keys in our reader and test SPD explicitly.)

## Approach

- Validate on real bytes to avoid guessing — the binary layout edge-cases (big-endian samples, the
  per-sweep trailing value, the SPD timestamp/integer flags) are the main risk, which the real
  sample plus the maser4py reference now mitigate. If a field remains ambiguous, parse what's safe
  and mark the rest `TODO` rather than fabricate (the Plan 04 principle still holds).

## Verification

- `read_sps`/`read_spd` parse the bundled real sample and the round-trip/field tests pass; Ch 23/30
  render real data; `ruff` + `nbmake` + `mkdocs --strict` green.
