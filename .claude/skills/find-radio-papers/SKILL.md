---
name: find-radio-papers
description: Find recent or landmark radio-astronomy papers on a topic, via NASA ADS and arXiv. Use when the user wants a literature search, the latest preprints, or the key references on a radio-astronomy subject (FRBs, pulsar timing, VLBI, the CMB, masers, an instrument, etc.).
---

# Find radio-astronomy papers

Produce a short, **link-verified**, cited list of the most relevant papers for the user's topic.

## Procedure

1. **Check what the course already has.** Skim `docs/papers-timeline.md` (year-by-year landmarks)
   and `docs/references.md` (thematic bibliography) — the foundational papers are likely there
   already, with ADS/DOI links. Reuse those rather than re-finding them.
2. **Search for the rest** with WebSearch / WebFetch:
   - **NASA ADS** — `https://ui.adsabs.harvard.edu/` (the authoritative index; search the topic,
     sort by citations for landmarks or by date for recent work).
   - **arXiv** — `http://export.arxiv.org/api/query?search_query=...` for preprints (astro-ph.IM,
     astro-ph.HE, astro-ph.GA, astro-ph.CO as fits the topic). The `scripts/dataset_watch.py`
     module has a `query_arxiv` helper you can reuse.
3. **Verify** each paper exists before citing it: confirm a real ADS bibcode or DOI resolves. Do
   **not** invent citations — omit anything you can't verify.

## Report

For each paper: **authors (et al.), year, title, journal**, a one-line "why it matters", and a
verified **ADS or DOI link**. Group by era or sub-topic; lead with the most influential or most
recent as the user asked. State plainly if the literature is thin or you couldn't verify something.

For a deep, multi-paper review or a question that needs synthesis across many sources, delegate to
the **radio-research-assistant** agent instead of doing it all inline.
