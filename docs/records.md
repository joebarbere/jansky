# Radio-Astronomy Records

Record-holding radio sources — the brightest, most distant, fastest-spinning, first-discovered, and
more. Every entry cites a source; values change as surveys go deeper, so the **`radio-records`** Claude
skill (`.claude/skills/radio-records/`) re-checks and updates this page against the live catalogues
(ATNF pulsar catalogue, VizieR, SIMBAD/NED, ADS). Entries marked **[verify]** are ones the skill should
re-confirm — don't quote them without checking.

Records are radio-specific (radio flux, radio spin, radio-detected distance). Many categories split by
**source type** (pulsars, AGN/quasars, radio galaxies, supernova remnants, FRBs, masers, solar system),
so a sub-record per type is given where it's meaningful.

## Brightness (flux density)

| Record | Source | Value | Reference |
|---|---|---|---|
| Brightest radio source, all-sky | **The Sun** | up to $>10^{6}$ Jy in bursts (quiet Sun $\sim$10$^4$ Jy at 1 GHz) | Dulk 1985 |
| Brightest beyond the solar system | **Cassiopeia A** (SNR) | $\sim$2720 Jy at 1 GHz (1980; secular decline $\sim$0.5–1%/yr) | Baars et al. 1977 |
| Brightest extragalactic | **Cygnus A** (3C 405) | $\sim$1600 Jy at 1.4 GHz | Baars et al. 1977 |
| Other canonical bright | Virgo A (M87), Centaurus A, Taurus A (Crab) | tens–hundreds of Jy | Baars et al. 1977 |
| Faintest individually detected | deep-field µJy/sub-µJy sources | $\sim$few hundred nJy (stacking reaches nJy) | **[verify]** current deepest field (MeerKAT/VLA) |

## Distance

| Record | Source | Value | Reference |
|---|---|---|---|
| Closest, all-sky | **The Sun** | 1 AU | — |
| Nearest radio-detected star | **Proxima Centauri** (flares) | 1.30 pc | Pérez-Torres et al. 2021 |
| Nearest pulsars | PSR J0437−4715, PSR J1856−3754 | $\sim$130–160 pc | ATNF catalogue **[verify nearest]** |
| Most distant radio-loud quasar | **PSO J172+18** | $z=6.82$ | Bañados et al. 2021 **[verify latest]** |
| Most distant radio galaxy (HzRG) | USS-selected HzRGs | $z\sim5.7$ | Saxena et al. 2018 **[verify]** |

## Pulsar spin

| Record | Source | Value | Reference |
|---|---|---|---|
| Fastest-spinning pulsar | **PSR J1748−2446ad** | 716 Hz (1.40 ms) | Hessels et al. 2006 |
| First millisecond pulsar | **PSR B1937+21** | 642 Hz (1.56 ms) | Backer et al. 1982 |
| Slowest "normal" radio pulsar | **PSR J0250+1749** | $P=23.5$ s | Tan et al. 2018 |
| Long-period radio transients (new class) | **GPM J1839−10**; GLEAM-X J1627−52 | $\sim$1318 s ($\sim$22 min); $\sim$18 min | Hurley-Walker et al. 2023, 2022 |
| First binary pulsar (Nobel 1993) | **PSR B1913+16** (Hulse–Taylor) | $P_b=7.75$ hr | Hulse & Taylor 1975 |

## Firsts (discovery)

| First | Source | Year | Reference |
|---|---|---|---|
| Cosmic radio emission | the **Milky Way** (toward Sagittarius) | 1933 | Jansky 1933 |
| Discrete radio source ("radio star") | **Cygnus A** | 1946 | Hey, Parsons & Phillips 1946 |
| Optically identified radio galaxy | Cygnus A | 1954 | Baade & Minkowski 1954 |
| Quasar (with redshift) | **3C 273** | 1963 | Schmidt 1963 |
| Pulsar | **PSR B1919+21** | 1968 | Hewish, Bell et al. 1968 |
| Fast radio burst | **FRB 20010724** (Lorimer burst) | 2007 | Lorimer et al. 2007 |
| Repeating FRB | **FRB 20121102A** | 2016 | Spitler et al. 2016 |

## Names

- Coordinate-based designations are the longest: pulsars append a discovery suffix (e.g.
  **PSR J1748−2446ad** — the 30th pulsar found in the globular cluster Terzan 5), and survey sources
  encode full sexagesimal positions (e.g. **GLEAM-X J162759.5−523504.3**). **[verify]** the
  skill can scan catalogues for the longest catalogued designation string.

## Notable / iconic sources

- **Sagittarius A\*** — the Galactic-Centre supermassive black hole; first horizon-scale image, EHT 2022.
- **M87\*** — first image of a black hole, EHT 2019.
- **3C 273, Cygnus A, Cassiopeia A, the Crab (Taurus A), Centaurus A, Virgo A** — the canonical sources
  every facility points at first.

## By telescope (signature / "first-light" sources)

| Telescope | Signature radio source(s) |
|---|---|
| Event Horizon Telescope | M87\* (2019), Sgr A\* (2022) |
| Arecibo | Hulse–Taylor binary PSR B1913+16; early FRB repeater work |
| VLA / VLASS | Cygnus A imaging; the deep-field source counts |
| MWA / GLEAM(-X) | long-period radio transients; the southern peaked-spectrum samples used by `jansky-research` |
| CHIME | the FRB catalogue (hundreds of bursts) |
| MeerKAT | Galactic-Centre radio bubbles; deep continuum fields |

## Most cited

**[verify]** — the `radio-records` skill should query ADS for citation counts of candidate sources
and their discovery papers (e.g. NVSS / Condon et al. 1998, Sgr A\*, 3C 273, the Hulse–Taylor pulsar).
Do not assert a "most cited" without a live ADS check.

---

*Maintained with the `radio-records` skill. Many seminal references here are in the
[Bibliography](references.md) and [Landmark Papers by Year](papers-timeline.md).*
