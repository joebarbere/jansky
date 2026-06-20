# Resources: Observatories, Archives & University Groups

Radio astronomy runs on shared, open infrastructure: a handful of great
telescopes, public data archives anyone can query, and free software written by
the community that uses it. This page is a curated index of the *places and sites*
a working radio astronomer actually uses — where the data come from, where they
live, and where the people are.

It's **representative, not exhaustive** — the field is too large to list in full,
and links drift. For the **seminal-paper bibliography and the textbooks** the
course is built around, see the [References](references.md) page; this page
deliberately complements it by pointing at institutions, facilities, and
communities rather than repeating the paper list.

All URLs below were verified live in June 2026.

## Major radio observatories & facilities

This page lists the *organisations*; for a detailed instrument-by-instrument catalogue (sizes,
bands, locations), see **[Radio Telescopes of the World](telescopes.md)**.

| Facility | What it is | Link |
|---|---|---|
| **NRAO** (VLA, VLBA) | US national radio observatory (NSF/AUI); operates the Very Large Array and Very Long Baseline Array | [public.nrao.edu](https://public.nrao.edu/) |
| **ALMA** | 66-antenna mm/sub-mm array on Chajnantor, Chile; ESO/NSF/NINS partnership | [almaobservatory.org](https://www.almaobservatory.org/) |
| **Green Bank Observatory** (GBT) | Home of the Green Bank Telescope, the largest fully steerable dish, West Virginia | [greenbankobservatory.org](https://greenbankobservatory.org/) |
| **ngVLA** | NRAO's next-generation array, succeeding the VLA in sensitivity and resolution | [ngvla.nrao.edu](https://ngvla.nrao.edu/) |
| **SKAO** (SKA) | Intergovernmental observatory building SKA-Mid (South Africa) and SKA-Low (Australia) | [skao.int](https://www.skao.int/) |
| **ASTRON / LOFAR** | Netherlands Institute for Radio Astronomy; operates the LOFAR low-frequency array and Westerbork | [astron.nl](https://www.astron.nl/) |
| **MPIfR / Effelsberg** | Max Planck Institute for Radio Astronomy, Bonn; operates the 100 m Effelsberg telescope | [mpifr-bonn.mpg.de](https://www.mpifr-bonn.mpg.de/) |
| **JIVE** (EVN/VLBI) | Joint Institute for VLBI ERIC; correlation and support for the European VLBI Network | [jive.eu](https://www.jive.eu/) · [evlbi.org](https://www.evlbi.org/) |
| **CSIRO / ATNF** | Australia Telescope National Facility — ATCA, Parkes "Murriyang", and ASKAP | [atnf.csiro.au](https://www.atnf.csiro.au/) |
| **SARAO / MeerKAT** | South African Radio Astronomy Observatory; operates MeerKAT and leads SA's SKA role | [sarao.ac.za](https://www.sarao.ac.za/) |
| **NAOJ Nobeyama** | National Astronomical Observatory of Japan; home of the Nobeyama 45 m mm-wave telescope | [nro.nao.ac.jp](https://www.nro.nao.ac.jp/en/) |
| **FAST** | Five-hundred-metre Aperture Spherical Telescope, the largest single dish, Guizhou, China | [fast.bao.ac.cn](https://fast.bao.ac.cn/en/) |
| **Arecibo / NAIC** | Legacy site of the 305 m Arecibo dish (collapsed 2020), now an educational facility | [naic.edu](https://www.naic.edu/) |
| **IRAM** (NOEMA, 30 m) | Institut de Radioastronomie Millimétrique, Grenoble; operates the 30 m and NOEMA | [iram-institute.org](https://iram-institute.org/) |
| **Jodrell Bank / e-MERLIN** | University of Manchester; the Lovell Telescope and the UK e-MERLIN array | [jodrellbank.manchester.ac.uk](https://www.jodrellbank.manchester.ac.uk/) |
| **GMRT** | Giant Metrewave Radio Telescope (NCRA-TIFR), near Pune, India | [gmrt.ncra.tifr.res.in](http://www.gmrt.ncra.tifr.res.in/) |
| **MIT Haystack** | Radio science research center in Westford, Massachusetts (EHT, geodesy, EDGES) | [haystack.mit.edu](https://www.haystack.mit.edu/) |

## Data archives & virtual observatory

The [References](references.md) page already links the **NRAO Science Data
Archive**, **HEASARC**, and **astroquery / pyvo**. A fuller set of archives and
Virtual Observatory entry points:

| Archive | Contents | Link |
|---|---|---|
| **NRAO Science Data Archive** | VLA, VLBA and related NRAO data (see References) | [data.nrao.edu](https://data.nrao.edu/) |
| **ALMA Science Archive** | All ALMA observations; the `.org` query tool routes to a regional mirror | [almascience.org/aq](https://almascience.org/aq/) |
| **CASDA** | CSIRO ASKAP Science Data Archive, with VO services | [research.csiro.au/casda](https://research.csiro.au/casda/) |
| **MeerKAT / SARAO archive** | MeerKAT observational data | [archive.sarao.ac.za](https://archive.sarao.ac.za/) |
| **LOFAR LTA** | The LOFAR Long Term Archive search and retrieval interface | [lta.lofar.eu](https://lta.lofar.eu/) |
| **HEASARC** | NASA multi-mission high-energy archive, software and tools (see References) | [heasarc.gsfc.nasa.gov](https://heasarc.gsfc.nasa.gov/) |
| **CDS** (SIMBAD, VizieR) | Strasbourg data centre; object database, catalogue service, Aladin | [cds.unistra.fr](https://cds.unistra.fr/) · [SIMBAD](https://simbad.cds.unistra.fr/simbad/) · [VizieR](https://vizier.cds.unistra.fr/) |
| **MAST** | STScI archive for Webb, Hubble, TESS, Kepler, Roman and more | [archive.stsci.edu](https://archive.stsci.edu/) |
| **IVOA / the VO** | International Virtual Observatory Alliance; defines the VO standards | [ivoa.net](https://www.ivoa.net/) |
| **ATNF Pulsar Catalogue** | The `psrcat` catalogue with an interactive query interface | [atnf.csiro.au/.../psrcat](https://www.atnf.csiro.au/research/pulsar/psrcat/) |
| **LAMBDA** | NASA's Legacy Archive for Microwave Background Data Analysis | [lambda.gsfc.nasa.gov](https://lambda.gsfc.nasa.gov/) |

## Software & tools

The [References](references.md) page covers **CASA**, **astropy/astroquery**,
**spectral-cube**, **radio-beam**, **PINT**, and **pyvo**. The wider radio
toolbox:

| Tool | Use | Link |
|---|---|---|
| **CASA** | Calibration, imaging and analysis for ALMA and the VLA | [casa.nrao.edu](https://casa.nrao.edu/) |
| **WSClean** | Fast wide-field interferometric imager (w-stacking CLEAN) | [gitlab.com/aroffringa/wsclean](https://gitlab.com/aroffringa/wsclean) |
| **AOFlagger** | RFI detection and flagging | [gitlab.com/aroffringa/aoflagger](https://gitlab.com/aroffringa/aoflagger) |
| **CARTA** | Interactive image/cube visualization for ALMA, VLA and SKA pathfinders | [cartavis.org](https://cartavis.org/) |
| **astropy / astroquery** | Core Python astronomy library and archive-query package | [astropy.org](https://www.astropy.org/) · [astroquery](https://astroquery.readthedocs.io/) |
| **VIRGO** | Open-source Python package for amateur spectral-line radio astronomy (powers PICTOR) | [github.com/0xCoto/VIRGO](https://github.com/0xCoto/VIRGO) |
| **pyuvdata** (RASG) | Read/write & convert interferometer visibilities (MS ↔ UVFITS ↔ UVH5) | [radioastronomysoftwaregroup.github.io](https://radioastronomysoftwaregroup.github.io/) |
| **blimpy / turboSETI** | Breakthrough Listen filterbank/GUPPI I/O and the Doppler-drift SETI search | [github.com/UCBerkeleySETI/blimpy](https://github.com/UCBerkeleySETI/blimpy) |
| **RASDR** | Radio Astronomy SDR (LimeSDR-based); feeds Radio-Sky Spectrograph | [github.com/myriadrf/RASDR](https://github.com/myriadrf/RASDR) |
| **PRESTO** | Pulsar search and analysis toolkit | [github.com/scottransom/presto](https://github.com/scottransom/presto) |
| **PINT** | High-precision pulsar timing (NANOGrav) | [github.com/nanograv/PINT](https://github.com/nanograv/PINT) |
| **DSPSR / PSRCHIVE** | Pulsar signal processing and data archiving libraries | [dspsr](http://dspsr.sourceforge.net/) · [psrchive](http://psrchive.sourceforge.net/) |
| **Miriad** | ATNF interferometry reduction package (notably for ATCA) | [atnf.csiro.au/.../miriad](https://www.atnf.csiro.au/computing/software/miriad/) |
| **AIPS** | NRAO's classic interferometry reduction and imaging system | [aips.nrao.edu](http://www.aips.nrao.edu/index.shtml) |

## University & research groups in radio astronomy

A **representative** international sample of groups, departments, and institutes
with strong radio-astronomy programmes — far from a complete list, but a good
sense of where the work happens.

| Group | Country | Link |
|---|---|---|
| MIT Haystack Observatory | US | [haystack.mit.edu](https://www.haystack.mit.edu/astronomy/) |
| Caltech / OVRO | US | [ovro.caltech.edu](https://www.ovro.caltech.edu/) |
| UC Berkeley — Breakthrough Listen / SETI | US | [seti.berkeley.edu](https://seti.berkeley.edu/) |
| Cornell — Department of Astronomy | US | [astro.cornell.edu](https://astro.cornell.edu/) |
| NRAO & University of Virginia | US | [science.nrao.edu](https://science.nrao.edu/) · [astronomy.as.virginia.edu](https://astronomy.as.virginia.edu/) |
| Jodrell Bank Centre, Univ. of Manchester | UK | [jodrellbank.manchester.ac.uk](https://www.jodrellbank.manchester.ac.uk/) |
| Cavendish Radio Astronomy & Cosmology (MRAO), Cambridge | UK | [cavendishradiocosmology.com](https://www.cavendishradiocosmology.com/) |
| Oxford — Astrophysics | UK | [physics.ox.ac.uk/.../astrophysics](https://www.physics.ox.ac.uk/research/subdepartment/astrophysics) |
| ASTRON | NL | [astron.nl](https://www.astron.nl/) |
| Leiden Observatory | NL | [universiteitleiden.nl/.../astronomy](https://www.universiteitleiden.nl/en/science/astronomy) |
| Kapteyn Institute, Univ. of Groningen | NL | [rug.nl/research/kapteyn](https://www.rug.nl/research/kapteyn/?lang=en) |
| MPIfR Bonn | DE | [mpifr-bonn.mpg.de](https://www.mpifr-bonn.mpg.de/) |
| ICRAR (Curtin & UWA) | AU | [icrar.org](https://www.icrar.org/) |
| Sydney Institute for Astronomy, Univ. of Sydney | AU | [sifa.sydney.edu.au](https://sifa.sydney.edu.au/) |
| NCRA-TIFR | IN | [ncra.tifr.res.in](https://www.ncra.tifr.res.in/) |
| Dunlap Institute, Univ. of Toronto | CA | [dunlap.utoronto.ca](https://www.dunlap.utoronto.ca/) |
| ESO (ALMA partner) | DE / intl. | [eso.org](https://www.eso.org/public/) |

## Learning resources, communities & careers

- **NRAO Synthesis Imaging Workshop** — the biennial graduate-level school on
  aperture synthesis, calibration and imaging —
  [science.nrao.edu/opportunities/courses](https://science.nrao.edu/opportunities/courses)
- **ERIS** (European Radio Interferometry School) — a week of lectures and
  hands-on interferometry tutorials — [jive.eu/eris](https://www.jive.eu/eris2022/)
- **CASA Guides** — step-by-step CASA reduction tutorials for VLA, ALMA and VLBI —
  [casaguides.nrao.edu](https://casaguides.nrao.edu/)
- **AAS** — American Astronomical Society — [aas.org](https://aas.org/)
- **IAU** — International Astronomical Union — [iau.org](https://www.iau.org/),
  including [Commission B4 (Radio Astronomy)](https://www.iau.org/science/scientific_bodies/commissions/B4/)
- **URSI** — International Union of Radio Science — [ursi.org](https://www.ursi.org/)
- **arXiv astro-ph** — the open-access preprint server's astrophysics listing —
  [arxiv.org/list/astro-ph/recent](https://arxiv.org/list/astro-ph/recent)
- **ADS** — NASA Astrophysics Data System, the literature search portal —
  [ui.adsabs.harvard.edu](https://ui.adsabs.harvard.edu/)
- **NRAO REU / summer students** — NSF-funded undergraduate research —
  [science.nrao.edu/.../summerstudents](https://science.nrao.edu/opportunities/student-programs/summerstudents)
- **NRAO Science Helpdesk** — ticketed support for VLA/VLBA/GBT/CASA —
  [help.nrao.edu](https://help.nrao.edu/) (ALMA: [help.almascience.org](https://help.almascience.org/))

## Key journals

| Journal | Link |
|---|---|
| **ApJ** — The Astrophysical Journal | [iopscience.iop.org](https://iopscience.iop.org/journal/0004-637X) |
| **AJ** — The Astronomical Journal | [iopscience.iop.org](https://iopscience.iop.org/journal/1538-3881) |
| **A&A** — Astronomy & Astrophysics | [aanda.org](https://www.aanda.org/) |
| **MNRAS** — Monthly Notices of the RAS | [academic.oup.com/mnras](https://academic.oup.com/mnras) |
| **PASA** — Publications of the Astron. Soc. of Australia | [cambridge.org/.../pasa](https://www.cambridge.org/core/journals/publications-of-the-astronomical-society-of-australia) |
| **PASP** — Publications of the Astron. Soc. of the Pacific | [iopscience.iop.org](https://iopscience.iop.org/journal/1538-3873) |
| **RAS journals** (MNRAS, GJI, RASTI) | [ras.ac.uk/journals](https://ras.ac.uk/journals) |
| **Nature** | [nature.com](https://www.nature.com/) |
| **Science** | [science.org](https://www.science.org/) |

---

> Radio astronomy is an unusually open and collaborative field: most of the great
> telescopes are public facilities, the archives are free to query, and the core
> software is open source. If a link here has moved, search for the institution by
> name — and for the landmark papers and textbooks behind the course, head to
> [References](references.md).
