# jansky — expansion plans

This directory holds **plans**, not implementation. Each plan proposes additions to the
`jansky` course and maps them to gaps in the current content. A future session (or a
contributor) can pick up any plan and execute it; nothing here changes the shipped course
until a plan is implemented and merged.

The plans were derived by mining the course's own reference pages for topics that are
*pointed at but not yet taught*, plus a specific request to fold in a set of external
resources on amateur data formats and SETI software.

## The plans

| Plan | Source it expands from | What it proposes |
|---|---|---|
| [01 — chapters from research & videos](01-chapters-from-research-and-videos.md) | [`papers-timeline.md`](../docs/papers-timeline.md), [`videos.md`](../docs/videos.md), [`field-notes.md`](../docs/field-notes.md) | New/expanded chapters: FRBs & transients, the EHT & VLBI, SETI, pulsar-timing-array nanohertz GW, the CMB, molecular-line & masers, solar & Jupiter radio, intensity interferometry |
| [02 — chapters from the projects list](02-chapters-from-projects.md) | [`projects.md`](../docs/projects.md) | Hardware/amateur chapters: GNU Radio flowgraphs, RASDR, KrakenSDR coherent interferometry, meteor scatter & passive radar, VLF/SuperSID, Radio JOVE (Jupiter), the VIRGO/PICTOR observing path |
| [03 — appendices from math preliminaries](03-appendices-from-math-preliminaries.md) | [`math-preliminaries.md`](../docs/math-preliminaries.md) | Deeper math modules: Fourier/convolution deep-dive, detection theory & matched filtering (dedispersion/FRB search), statistics & RFI excision, coordinates & time systems, calibration linear algebra |
| [04 — data formats & SETI software](04-data-formats-and-seti-software.md) | the **provided link set** (below) | Fold in GUPPI + SETI tools, RASDR, Radio-Sky Spectrograph (SPS/SPD/RSS), VIRGO, the RASG ecosystem, and PICTOR — via a new `jansky.formats` helper, a "Data formats & the ecosystem" chapter, and doc updates |

## How the plans are scoped

Each plan states, up front, **what is already covered** (with file references) so nothing is
duplicated. The current course is 15 chapters (`notebooks/01…15`), a helper package
(`src/jansky/`), containers, and a deep docs/reference library. Existing coverage that the
plans build on rather than repeat:

- **Single-dish & emission physics** — Ch 1–4, 6 · **noise/radiometer** — Ch 3
- **SDR basics & IQ data** — Ch 5 · **hydrogen line** — Ch 6
- **Interferometry, the uv-plane, CLEAN** — Ch 7–9 · **Measurement Sets / CASA** — Ch 12
- **Archives (astroquery/pyvo)** — Ch 10 · **HI cubes / rotation** — Ch 11
- **Pulsars & PSRFITS, dedispersion, folding** — Ch 13 · **multi-wavelength** — Ch 14
- Reference pages: glossary, notation, math-preliminaries, projects/kits/hacks, field-notes,
  telescopes, Mastodon, videos, the visual tour, and the year-by-year papers timeline.

## Coverage of the provided resource links (drives plan 04)

The request included a specific set of links. Status against the current course:

| Resource | Topic | Covered today? | Where it lands |
|---|---|---|---|
| Estévez — *Writing GUPPI files with GNU Radio & using SETI tools* | GUPPI raw voltage format; `rawspec`/`blimpy`/`turboSETI` | ❌ not covered | Plan 04 (formats + SETI chapter) |
| RadioAstronomySoftwareGroup (RASG) GitHub Pages | `pyuvdata`, `pyradiosky`, RFI tools ecosystem | ❌ not covered | Plan 04 (ecosystem section) |
| pictortelescope.com | PICTOR free online HI telescope | ⚠️ linked only (`projects.md`, `field-notes.md`) | Plan 02 + 04 (hands-on observation) |
| casa.nrao.edu | CASA imaging/calibration | ✅ Ch 12 + `resources.md` | — (already covered) |
| VIRGO docs (install) | `astro-virgo` single-dish HI/continuum package | ⚠️ linked only (`resources.md`, `field-notes.md`) | Plan 04 (use it, not just link it) |
| cygnusa.blogspot — Amateur Radio Astronomy | amateur observing; Radio-Sky Spectrograph how-to | ❌ not covered | Plan 04 (RSS protocol) |
| radiojove.org — *SPS File Format (Typinski 2015)* | SPS spectrograph file format | ❌ not covered | Plan 04 (`jansky.formats`) |
| radiosky.com — *RSS_Help2.pdf* | Radio-Sky Spectrograph; SPD format | ❌ not covered | Plan 04 (`jansky.formats` + RSS client) |
| cygnusa — *How to Talk to Radio-Sky Spectrograph* | RSS TCP/IP protocol | ❌ not covered | Plan 04 (RSS socket client) |
| myriadrf/RASDR commit — *TCP socket using RSS protocol* | RASDR ↔ RSS interop | ❌ not covered | Plan 04 (protocol reference) |
| myriadrf/RASDR repo | Radio Astronomy SDR (LimeSDR) | ❌ not covered | Plan 02 (hardware) + Plan 04 (interop) |

**Bottom line:** of the provided links, only CASA is already taught. The rest cluster around
**amateur data formats and the radio-astronomy software ecosystem** — a genuine, coherent gap
that Plan 04 addresses directly, with Plan 02 covering the matching hardware.

## Suggested sequencing

1. **Plan 04** first — it is the explicit request and adds a reusable `jansky.formats` helper
   that later chapters can build on.
2. **Plan 02** — hardware chapters that produce the data those formats describe.
3. **Plan 01** — science chapters (mostly archival/simulated, lower hardware burden).
4. **Plan 03** — math appendices, woven in as the chapters that need them land.

Each plan is independently executable; this is only a recommended order.
