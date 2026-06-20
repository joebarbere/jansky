# Plan 15 — Implement the SPS/SPD readers 📋 Proposed

> Flagged by **archive/real-data (#2 top)**. Scope: medium–large. Closes the one outstanding item
> from [Plan 04](04-data-formats-and-seti-software.md).

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

## Approach

- Validate on real bytes to avoid guessing — the binary layout edge-cases are the main risk, which
  having the sample mitigates. If a field remains ambiguous after the sample + spec notes, parse
  what's safe and mark the rest `TODO` rather than fabricate (the Plan 04 principle still holds).

## Verification

- `read_sps`/`read_spd` parse the bundled real sample and the round-trip/field tests pass; Ch 23/30
  render real data; `ruff` + `nbmake` + `mkdocs --strict` green.
