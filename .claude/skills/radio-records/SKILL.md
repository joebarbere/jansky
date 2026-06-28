---
name: radio-records
description: Find, verify, and update record-holding radio sources — brightest/faintest, nearest/most-distant, fastest/slowest-spinning pulsar, firsts, longest name, most-cited, and signature sources per telescope — across catalogues (ATNF pulsar catalogue, VizieR, SIMBAD/NED) and ADS. Use to populate or refresh docs/records.md, or to answer "what is the <-est> radio source".
---

# Radio-astronomy records

Maintain `docs/records.md`: a cited table of record-holding radio sources. Records drift as surveys go
deeper, so **verify against live catalogues** and **never assert a record without a citation**. Entries
marked **[verify]** in the page are the ones most in need of a re-check.

## Procedure by category

1. **Pulsar spin (fastest / slowest / first MSP).** The ATNF Pulsar Catalogue is the authority — on
   VizieR as **`B/psr`** (columns `P0` = spin period s, `F0` = spin frequency Hz). Query it and sort:
   - fastest = min `P0` (currently PSR J1748−2446ad, 716 Hz; Hessels et al. 2006);
   - slowest *rotation-powered* radio pulsar = max `P0` among normal pulsars (J0250+1749, 23.5 s);
   - note the **long-period radio transients** separately (GPM J1839−10 ~22 min; Hurley-Walker 2023)
     — they are a distinct class, not in the classical pulsar tail.
   Use `astroquery.vizier` (or `psrqpy` if available) and report the source name + value + the
   discovery paper.
2. **Brightness (brightest / faintest).** Brightest beyond the Sun is set by the standard flux scale
   (Baars et al. 1977: Cas A, Cyg A, Vir A, Tau A). For the *faintest*, find the current deepest-field
   record from the literature (MeerKAT/VLA µJy–nJy surveys) — search ADS (see `find-radio-papers`); do
   not quote a fixed number without the paper.
3. **Distance (nearest / most distant).** Nearest pulsars: ATNF `B/psr` column `Dist` (kpc). Nearest
   radio star: SIMBAD + the radio-stars literature. Most distant radio-loud quasar / radio galaxy:
   search ADS for the current record (it advances every year or two) and confirm the redshift in the
   discovery paper. Resolve identities with SIMBAD/NED via `astroquery`.
4. **Firsts.** These are historical and stable (Jansky 1933 → Milky Way; Cyg A 1946; 3C 273 1963;
   B1919+21 1968; Lorimer burst 2007; FRB 20121102A first repeater 2016). Keep the citation; only add
   new "first of a kind" rows as the field produces them.
5. **Longest name.** Scan a large catalogue (e.g. `B/psr` names, or a survey component catalogue on
   VizieR) for the longest designation string; report it with the catalogue.
6. **Most cited.** Query **ADS** (via WebFetch/WebSearch or the ADS API) for citation counts of
   candidate sources' discovery/survey papers (NVSS, Sgr A\*, 3C 273, Hulse–Taylor, …) and report the
   leader with its count and date — never assert without the live count.
7. **Per telescope.** Signature/"first-light" sources (EHT → M87\*/Sgr A\*; MWA/GLEAM → long-period
   transients; CHIME → FRBs; …) — confirm from each instrument's landmark paper.

## Updating the page

- Edit `docs/records.md` in place; keep the table format and a **reference** in every row.
- Cross-link seminal references to `docs/references.md` / `docs/papers-timeline.md` where they exist;
  add new ones there if missing.
- Clear a **[verify]** tag only once you've confirmed the value against a live catalogue/paper this run.
- Wrap all network calls in try/except and say so if a source is unreachable; report what would be
  queried rather than guessing.

For a deep multi-paper hunt (e.g. the current most-distant record), hand off to the
**radio-research-assistant** agent; for a single source's full profile use the **radio-source-lookup**
skill.
