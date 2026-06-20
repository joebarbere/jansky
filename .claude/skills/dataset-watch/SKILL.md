---
name: dataset-watch
description: Check whether new radio-astronomy datasets, data releases, or preprints have appeared in the sources this project tracks (NRAO, ALMA, the ATNF pulsar catalogue, NASA LAMBDA, the Radio JOVE / SkyPipe archive, MASER, and arXiv feeds). Use when the user asks "what's new", wants to monitor the data sources, or check for fresh data or papers.
---

# Watch the data sources for new data

Two layers: an automated checker for the feeds that have an API or a stable page, and a manual
checklist for archives that don't.

## 1. Run the automated check

```bash
uv run python scripts/dataset_watch.py          # report what's new since last run
uv run python scripts/dataset_watch.py --list   # show the watched sources
uv run python scripts/dataset_watch.py --json    # machine-readable
uv run python scripts/dataset_watch.py --reset   # forget state and re-baseline
```

It (a) queries **arXiv** feeds (astro-ph.IM radio, FRBs, pulsar timing arrays) and reports
preprints whose IDs are new since the last run, and (b) **change-detects** archive landing pages
(NRAO, ALMA, ATNF psrcat, LAMBDA, the Radio JOVE/SkyPipe archive, MASER) by hashing them, flagging
any that changed for a manual look. State lives in `.cache/dataset_watch.json`, so the **first run
just sets a baseline** — run it again later to see deltas.

## 2. Report

- Summarise new preprints (title + arXiv link) and any changed archive pages (with what to look
  for, e.g. "ATNF psrcat — check the version number").
- For a flagged page, optionally fetch it (WebFetch) to say *what* changed.

## 3. Archives without an automatable feed

For targeted "is there new data on X" questions, check the relevant archive directly (these are
catalogued in `docs/resources.md` and `docs/telescopes.md`), e.g.:

- **NRAO** data.nrao.edu · **ALMA** almascience.org/aq · **HEASARC** · **CASDA** (ASKAP) ·
  **SARAO** (MeerKAT) · **LOFAR LTA** · **MAST** · **VizieR/CDS**.
- **Radio JOVE / SkyPipe (.spd/.sps)** data: the live archive is **radiojove.net** (the old
  radiojove.org is dead), plus the **MASER / VESPA** collection at Paris Observatory
  (maser.obspm.fr, vespa.obspm.fr). See `docs/data-formats.md`.

Programmatic archive queries (observations of a target, recent releases) are the
**archive-scout** agent's job — delegate there for anything beyond this watch.
