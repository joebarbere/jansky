# Radio Astronomy on GitHub

A curated, link-verified field guide to **radio-astronomy source code** — the organizations that
publish it, the repositories worth knowing, and the people who maintain them. Any language counts:
the field's tools are a mix of C++, Python, CUDA, Fortran, and HDL.

This page complements the institution-focused [Resources](resources.md), the hardware-focused
[Projects, Kits & Hacks](projects.md), the instrument catalogue [Radio Telescopes](telescopes.md),
and the [Bibliography](references.md). Where a tool is **used or taught in the course**, the chapter
is cross-linked; where a tool has a **canonical paper**, it is cited.

!!! note "Verified mid-2026 — and a caveat on hosting"
    Every GitHub link below was checked live. But radio astronomy predates GitHub, so several
    *major* tools live elsewhere — **CASA** (pip wheels), **WSClean** and **AOFlagger** (GitLab),
    **RASCIL** and **SatNOGS** (GitLab), **PSRCHIVE / DSPSR / heimdall** (SourceForge), **tempo2**
    (Bitbucket). Those are gathered under [Beyond GitHub](#beyond-github-gitlab-sourceforge-bitbucket)
    so the picture is honest, not just GitHub-shaped.

---

## Organizations & collaborations

The institutional and collaboration accounts that publish the field's software.

### Interferometry & imaging software groups

- **[casacore](https://github.com/casacore)** — the foundational C++ data model (Measurement Set,
  Tables, coordinates, images) that nearly every interferometry pipeline links against. Repos:
  [casacore](https://github.com/casacore/casacore), [python-casacore](https://github.com/casacore/python-casacore).
  *Paper:* [CASA Team 2022, PASP 134, 114501](https://doi.org/10.1088/1538-3873/ac9642). *In the course:*
  [Ch 12](notebooks/12_vla_imaging.ipynb), [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[casangi](https://github.com/casangi)** — NRAO's next-generation, Python-native CASA stack
  ([xradio](https://github.com/casangi/xradio) xarray/Zarr I/O, [graphviper](https://github.com/casangi/graphviper)
  Dask parallelism, [casadocs](https://github.com/casangi/casadocs)). The successor to the CASA monolith.
  *Paper:* [McMullin et al. 2007, ASPC 376, 127](https://ui.adsabs.harvard.edu/abs/2007ASPC..376..127M/abstract).
- **[RadioAstronomySoftwareGroup](https://github.com/RadioAstronomySoftwareGroup)** (RASG) — the
  Python visibility ecosystem: [pyuvdata](https://github.com/RadioAstronomySoftwareGroup/pyuvdata),
  [pyuvsim](https://github.com/RadioAstronomySoftwareGroup/pyuvsim),
  [pyradiosky](https://github.com/RadioAstronomySoftwareGroup/pyradiosky), and the
  [rasg-datasets](https://github.com/RadioAstronomySoftwareGroup/rasg-datasets) the course fetches from.
  *Paper:* [Hazelton et al. 2017, JOSS 2, 140](https://doi.org/10.21105/joss.00140). *In the course:*
  [Ch 12](notebooks/12_vla_imaging.ipynb), [Ch 16](notebooks/16_data_formats_and_ecosystem.ipynb).
- **[ratt-ru](https://github.com/ratt-ru)** — Rhodes University's MeerKAT/SKA-era calibration & imaging
  algorithms: [codex-africanus](https://github.com/ratt-ru/codex-africanus) (RIME building blocks),
  [QuartiCal](https://github.com/ratt-ru/QuartiCal) (Dask Jones-matrix calibration),
  [dask-ms](https://github.com/ratt-ru/dask-ms), [tigger](https://github.com/ratt-ru/tigger) (sky-model
  viewer). Home of the open textbook *Fundamentals of Radio Interferometry*. *In the course:*
  [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[lofar-astron](https://github.com/lofar-astron)** — ASTRON's LOFAR stack:
  [DP3](https://github.com/lofar-astron/DP3) (streaming calibration/flagging),
  [PyBDSF](https://github.com/lofar-astron/PyBDSF) (source finder),
  [RMextract](https://github.com/lofar-astron/RMextract) (ionospheric RM correction). *Paper:*
  [van Haarlem et al. 2013, A&A 556, A2](https://doi.org/10.1051/0004-6361/201220873). *In the course:*
  [Ch 37](notebooks/37_polarisation_faraday.ipynb), [Ch 39](notebooks/39_rfi_mitigation.ipynb).
- **[ska-sa](https://github.com/ska-sa)** — SARAO / MeerKAT software: [katdal](https://github.com/ska-sa/katdal)
  (data access), [katpoint](https://github.com/ska-sa/katpoint) (pointing/coordinates),
  [montblanc](https://github.com/ska-sa/montblanc) (GPU RIME). *Paper:*
  [Jonas 2009, IEEE Proc. 97, 1522](https://doi.org/10.1109/JPROC.2009.2020713).
- **[ska-telescope](https://github.com/ska-telescope)** — the SKA Observatory's GitHub presence
  (operational subsystems, global sky model). Note: most SKA code is on
  [GitLab](https://gitlab.com/ska-telescope), with GitHub a partial mirror.
- **[radio-astro-tools](https://github.com/radio-astro-tools)** — the spectral-cube ecosystem:
  [spectral-cube](https://github.com/radio-astro-tools/spectral-cube),
  [radio-beam](https://github.com/radio-astro-tools/radio-beam),
  [pvextractor](https://github.com/radio-astro-tools/pvextractor). *In the course:*
  [Ch 11](notebooks/11_hi_rotation_curve.ipynb).
- **[CARTAvis](https://github.com/CARTAvis)** — CARTA, the web-based cube/image viewer for ALMA/VLA/SKA
  ([carta-backend](https://github.com/CARTAvis/carta-backend), [carta-frontend](https://github.com/CARTAvis/carta-frontend)).
  *Paper:* [Wang et al. 2026, PASP 138, 024506](https://doi.org/10.1088/1538-3873/ae3eb4).

### Observatories & facilities

- **[GreenBankObservatory](https://github.com/GreenBankObservatory)** — the GBT toolchain:
  [dysh](https://github.com/GreenBankObservatory/dysh) (the modern GBTIDL successor, Python spectral-line
  reduction), [gbt-pipeline](https://github.com/GreenBankObservatory/gbt-pipeline),
  [gbtgridder](https://github.com/GreenBankObservatory/gbtgridder).
- **[MITHaystack](https://github.com/MITHaystack)** — [srt-py](https://github.com/MITHaystack/srt-py)
  (the Small Radio Telescope), [digital_rf](https://github.com/MITHaystack/digital_rf) (wideband recording
  format), [HOPS](https://github.com/MITHaystack/HOPS) (the EHT VLBI fringe-fitting suite). *In the course:*
  [Ch 6](notebooks/06_hydrogen_line.ipynb), [Projects](projects.md).
- **[jive-vlbi](https://github.com/jive-vlbi)** — JIVE / EVN correlator software:
  [sfxc](https://github.com/jive-vlbi/sfxc) (software correlator), [jive5ab](https://github.com/jive-vlbi/jive5ab)
  (VLBI recording), [PolConvert](https://github.com/jive-vlbi/PolConvert) (used in ALMA-VLBI & the EHT).
  *In the course:* [Ch 19](notebooks/19_eht_and_vlbi.ipynb).
- **[MPIfR-BDG](https://github.com/MPIfR-BDG)** — the Effelsberg/MeerKAT backend group: pulsar/FRB
  acquisition firmware ([mpikat](https://github.com/MPIfR-BDG/mpikat),
  [psrdada_cpp](https://github.com/MPIfR-BDG/psrdada_cpp)).
- **[NCRA-TIFR](https://github.com/NCRA-TIFR)** — the uGMRT's group: the
  [SPAM](https://github.com/NCRA-TIFR/gmrt-spam) ionospheric calibration pipeline. *Paper:*
  [Intema et al. 2017, A&A 598, A78](https://doi.org/10.1051/0004-6361/201628536).
- **[ATNF](https://github.com/ATNF)** — CSIRO-ATNF (ASKAP benchmarks, the deprecated `yandasoft` imager).
  Most ATNF pulsar code (PSRCHIVE, DSPSR) is on SourceForge.

### Collaborations: pulsars, FRBs, SETI, the EHT

- **[nanograv](https://github.com/nanograv)** — the nanohertz-GW pulsar-timing-array collaboration:
  [PINT](https://github.com/nanograv/PINT) (modern Python timing), [enterprise](https://github.com/nanograv/enterprise)
  (Bayesian PTA inference), [tempo](https://github.com/nanograv/tempo) (the Fortran classic). *Paper:*
  [Agazie et al. 2023, ApJ 951, L8](https://ui.adsabs.harvard.edu/abs/2023ApJ...951L...8A/abstract). *In the course:*
  [Ch 13](notebooks/13_pulsars.ipynb), [Ch 20](notebooks/20_pulsar_timing_arrays.ipynb).
- **[CHIMEFRB](https://github.com/CHIMEFRB)** — the largest FRB catalogue's backend:
  [kotekan](https://github.com/CHIMEFRB/kotekan) (real-time GPU pipeline),
  [fitburst](https://github.com/CHIMEFRB/fitburst) (burst modelling). *Paper:*
  [CHIME/FRB 2021, ApJS 257, 59](https://ui.adsabs.harvard.edu/abs/2021ApJS..257...59C/abstract). *In the course:*
  [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **[chime-experiment](https://github.com/chime-experiment)** — the broader CHIME telescope stack
  ([ch_pipeline](https://github.com/chime-experiment/ch_pipeline), [ch_util](https://github.com/chime-experiment/ch_util)).
- **[UCBerkeleySETI](https://github.com/UCBerkeleySETI)** — Breakthrough Listen:
  [blimpy](https://github.com/UCBerkeleySETI/blimpy) (filterbank/GUPPI I/O),
  [turbo_seti](https://github.com/UCBerkeleySETI/turbo_seti) (Doppler-drift search),
  [hyperseti](https://github.com/UCBerkeleySETI/hyperseti) (GPU successor). *Paper:*
  [Enriquez et al. 2017, ApJ 849, 104](https://doi.org/10.3847/1538-4357/aa8d1b). *In the course:*
  [Ch 21](notebooks/21_seti.ipynb).
- **[eventhorizontelescope](https://github.com/eventhorizontelescope)** — the EHT's calibrated data
  releases (M87 2019, Sgr A* 2022) and imaging pipelines. *Paper:*
  [EHT 2019, ApJ 875, L1](https://ui.adsabs.harvard.edu/abs/2019ApJ...875L...1E/abstract). *In the course:*
  [Ch 19](notebooks/19_eht_and_vlbi.ipynb).

### SDR, amateur & education

- **[gnuradio](https://github.com/gnuradio)** — the [GNU Radio](https://github.com/gnuradio/gnuradio)
  software-defined-radio framework behind most amateur and teaching radio astronomy. *In the course:*
  [Ch 28](notebooks/28_gnuradio_flowgraphs.ipynb).
- **[WVURAIL](https://github.com/WVURAIL)** — WVU's DSPIRA education program:
  [gr-radio_astro](https://github.com/WVURAIL/gr-radio_astro) (GNU Radio OOT modules),
  [os_radio_astro_hw](https://github.com/WVURAIL/os_radio_astro_hw) (open LNA hardware),
  [dspira-lessons](https://github.com/WVURAIL/dspira-lessons). *In the course:*
  [Ch 28](notebooks/28_gnuradio_flowgraphs.ipynb), [Projects](projects.md).
- **[krakenrf](https://github.com/krakenrf)** — the KrakenSDR 5-channel coherent receiver:
  [krakensdr_doa](https://github.com/krakenrf/krakensdr_doa) (direction finding / MUSIC),
  [heimdall_daq_fw](https://github.com/krakenrf/heimdall_daq_fw) (coherent acquisition). *In the course:*
  [Ch 17](notebooks/17_coherent_interferometry_kraken.ipynb).
- **[myriadrf](https://github.com/myriadrf)** — home of [RASDR](https://github.com/myriadrf/RASDR), the
  SARA-backed open-hardware Radio Astronomy SDR. *In the course:* [Ch 30](notebooks/30_rasdr_radio_sky.ipynb).
- **[maserlib](https://github.com/maserlib)** — Paris Observatory's
  [maser4py](https://github.com/maserlib/maser4py), readers for low-frequency & planetary radio formats
  (Nançay, Radio JOVE, Voyager/Cassini). *Paper:*
  [Cecconi et al. 2020, Data Science Journal 19, 12](https://doi.org/10.5334/dsj-2020-012). *In the course:*
  [Ch 23](notebooks/23_solar_and_jupiter.ipynb), and the basis for `jansky.formats` SPS/SPD readers.

### Foundational ecosystem

- **[astropy](https://github.com/astropy)** — the bedrock: [astropy](https://github.com/astropy/astropy)
  (coordinates, units, FITS, WCS, time) and [astroquery](https://github.com/astropy/astroquery) (archive
  access — NRAO, ALMA, SIMBAD, VizieR, HEASARC). Plus [reproject](https://github.com/astropy/reproject)
  and [regions](https://github.com/astropy/regions). *Paper:*
  [Astropy Collaboration 2022, ApJ 935, 167](https://doi.org/10.3847/1538-4357/ac7c74). *In the course:*
  used in essentially every chapter.

### 21 cm cosmology, intensity mapping & solar physics

- **[HERA-Team](https://github.com/HERA-Team)** — the Hydrogen Epoch of Reionization Array's
  software: [hera_cal](https://github.com/HERA-Team/hera_cal) (redundant calibration),
  [hera_sim](https://github.com/HERA-Team/hera_sim), [hera_qm](https://github.com/HERA-Team/hera_qm)
  (quality metrics), [hera_pspec](https://github.com/HERA-Team/hera_pspec) (power spectra),
  [matvis](https://github.com/HERA-Team/matvis) (fast visibility simulator). *In the course:*
  [Ch 6](notebooks/06_hydrogen_line.ipynb), [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[radiocosmology](https://github.com/radiocosmology)** — the CHIME 21 cm-intensity-mapping
  m-mode stack: [cora](https://github.com/radiocosmology/cora) (sky simulation),
  [driftscan](https://github.com/radiocosmology/driftscan), [draco](https://github.com/radiocosmology/draco),
  [caput](https://github.com/radiocosmology/caput). *Paper:* [Shaw et al. 2015, PhRvD 91, 083514](https://arxiv.org/abs/1401.2095).
- **[MWATelescope](https://github.com/MWATelescope)** — the Murchison Widefield Array's modern
  Rust pipeline: [mwa_hyperdrive](https://github.com/MWATelescope/mwa_hyperdrive) (calibration),
  [Birli](https://github.com/MWATelescope/Birli) (preprocessing). *In the course:*
  [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[EoRImaging](https://github.com/EoRImaging)** — the MWA EoR power-spectrum pipeline (IDL):
  [FHD](https://github.com/EoRImaging/FHD) (Fast Holographic Deconvolution),
  [eppsilon](https://github.com/EoRImaging/eppsilon) (power-spectrum estimator). *Paper:*
  [Barry et al. 2019, PASA 36, e026](https://doi.org/10.1017/pasa.2019.21).
- **[sunpy](https://github.com/sunpy)** — the core solar-physics Python ecosystem, including the
  radio dynamic-spectrum package [radiospectra](https://github.com/sunpy/radiospectra). *Paper:*
  [SunPy Community 2020, ApJ 890, 68](https://doi.org/10.3847/1538-4357/ab4f7a). *In the course:*
  [Ch 23](notebooks/23_solar_and_jupiter.ipynb).
- **[spedas](https://github.com/spedas)** — [pyspedas](https://github.com/spedas/pyspedas), the
  Python framework for heliophysics/CDAWeb data (Wind/WAVES, STEREO/WAVES, PSP, Solar Orbiter radio).
  *In the course:* [Ch 23](notebooks/23_solar_and_jupiter.ipynb).
- **[i4Ds](https://github.com/i4Ds)** — FHNW's institute for the e-Callisto solar-radio-spectrometer
  network: [ecallisto_ng](https://github.com/i4Ds/ecallisto_ng). *Paper:*
  [Benz et al. 2009, SoPh 260, 375](https://ui.adsabs.harvard.edu/abs/2009SoPh..260..375B/abstract).
  *In the course:* [Ch 23](notebooks/23_solar_and_jupiter.ipynb).

---

## Software repositories

### Pulsar timing & analysis

- **[nanograv/PINT](https://github.com/nanograv/PINT)** — high-precision Python pulsar timing
  (residuals agree with TEMPO/TEMPO2 to ~10 ns). Python, BSD-3. *Paper:*
  [Luo et al. 2021, ApJ 911, 45](https://doi.org/10.3847/1538-4357/abe62f). *In the course:*
  [Ch 13](notebooks/13_pulsars.ipynb), [Ch 20](notebooks/20_pulsar_timing_arrays.ipynb).
- **[scottransom/presto](https://github.com/scottransom/presto)** — the most widely used pulsar search
  suite (FFT/acceleration/single-pulse search, folding). C/Python, GPL-2. *Paper:*
  [Ransom et al. 2002, AJ 124, 1788](https://doi.org/10.1086/342285). *In the course:*
  [Ch 13](notebooks/13_pulsars.ipynb).
- **[mattpitkin/tempo2](https://github.com/mattpitkin/tempo2)** *(GitHub mirror)* — the 1-ns relativistic
  timing package; canonical home on [Bitbucket](https://bitbucket.org/psrsoft/tempo2). C/C++/Fortran, GPL-3.
  *Paper:* [Hobbs, Edwards & Manchester 2006, MNRAS 369, 655](https://doi.org/10.1111/j.1365-2966.2006.10302.x).
- **[vallis/libstempo](https://github.com/vallis/libstempo)** — Python/Cython wrapper around tempo2,
  the bridge into PTA workflows. MIT. *In the course:* [Ch 20](notebooks/20_pulsar_timing_arrays.ipynb).
- **[mattpitkin/psrqpy](https://github.com/mattpitkin/psrqpy)** — scripted queries of the ATNF Pulsar
  Catalogue. *Paper:* [Pitkin 2018, JOSS 3, 538](https://doi.org/10.21105/joss.00538).
- **[NickSwainston/pulsar_spectra](https://github.com/NickSwainston/pulsar_spectra)** — Bayesian
  flux-density spectral fitting with a crowd-maintained catalogue. *Paper:*
  [Swainston et al. 2022, PASA 39, e056](https://ui.adsabs.harvard.edu/abs/2022PASA...39...56S/abstract).
- **[v-morello/clfd](https://github.com/v-morello/clfd)** — outlier-based RFI excision for folded pulsar
  archives. *Paper:* [Morello et al. 2019, MNRAS 483, 3673](https://doi.org/10.1093/mnras/sty3328).
  *In the course:* [Ch 39](notebooks/39_rfi_mitigation.ipynb).
- **[nanograv/enterprise](https://github.com/nanograv/enterprise)** + **[enterprise_extensions](https://github.com/nanograv/enterprise_extensions)**
  — the Bayesian PTA framework behind the 2023 nanohertz-GW-background evidence. MIT. *In the course:*
  [Ch 20](notebooks/20_pulsar_timing_arrays.ipynb).

### Pulsar & FRB search, single-pulse & real-time pipelines

- **[thepetabyteproject/your](https://github.com/thepetabyteproject/your)** — "Your Unified Reader":
  one API over filterbank/PSRFITS/PSRDADA. Python, GPL-3. *Paper:*
  [Aggarwal et al. 2020, JOSS 5, 2750](https://doi.org/10.21105/joss.02750). *In the course:*
  [Ch 13](notebooks/13_pulsars.ipynb), [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **[FRBs/sigpyproc3](https://github.com/FRBs/sigpyproc3)** — numba-accelerated filterbank/PSRFITS I/O and
  search primitives (Python-3 rewrite of [ewanbarr/sigpyproc](https://github.com/ewanbarr/sigpyproc)). MIT.
- **[v-morello/riptide](https://github.com/v-morello/riptide)** — the Fast Folding Algorithm for long-period
  pulsar search. *Paper:* [Morello et al. 2020, MNRAS 497, 4654](https://doi.org/10.1093/mnras/staa2291).
- **[ypmen/PulsarX](https://github.com/ypmen/PulsarX)** — high-performance C++ folding/search for FAST &
  MeerKAT. *Paper:* [Men & Barr 2024, A&A 679, A20](https://ui.adsabs.harvard.edu/abs/2024A%26A...679A..20M/abstract).
- **[ypmen/TransientX](https://github.com/ypmen/TransientX)** — fast single-pulse search pipeline. *Paper:*
  [Men & Barr 2024, A&A 683, A183](https://doi.org/10.1051/0004-6361/202348247). *In the course:*
  [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **[ewanbarr/peasoup](https://github.com/ewanbarr/peasoup)** — GPU FFT-based pulsar search (TRAPUM's engine).
- **[cbassa/cdmt](https://github.com/cbassa/cdmt)** — GPU coherent dedispersion over many DM trials. *Paper:*
  [Bassa et al. 2017](https://arxiv.org/abs/1607.00909). *In the course:* [Ch 13](notebooks/13_pulsars.ipynb).
- **[kiyo-masui/burst_search](https://github.com/kiyo-masui/burst_search)** — real-time FRB search in GUPPI
  data. *In the course:* [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **[realfastvla/rfpipe](https://github.com/realfastvla/rfpipe)** — real-time interferometric FRB search for
  the VLA. *Paper:* [Law et al. 2018, ApJS 236, 8](https://doi.org/10.3847/1538-4365/aab77b). *In the course:*
  [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **[ledatelescope/bifrost](https://github.com/ledatelescope/bifrost)** — GPU stream-processing framework
  for real-time pipelines. *Paper:* [Cranmer et al. 2017, JAI 6, 1750007](https://doi.org/10.1142/S2251171717500076).

### FRBs: classification, redshifts & populations

- **[devanshkv/fetch](https://github.com/devanshkv/fetch)** — CNN classifier separating FRBs from RFI.
  *Paper:* [Agarwal et al. 2020, MNRAS 497, 1661](https://doi.org/10.1093/mnras/staa1856). *In the course:*
  [Ch 18](notebooks/18_fast_radio_bursts.ipynb), [Ch 38](notebooks/38_machine_learning.ipynb).
- **[abatten/fruitbat](https://github.com/abatten/fruitbat)** — FRB redshift estimation from DM. *Paper:*
  [Batten 2019, JOSS 4, 1399](https://doi.org/10.21105/joss.01399). *In the course:*
  [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **[davidgardenier/frbpoppy](https://github.com/davidgardenier/frbpoppy)** — FRB population synthesis.
  *Paper:* [Gardenier et al. 2019, A&A 632, A125](https://doi.org/10.1051/0004-6361/201936404).

### Interferometric calibration & flagging

- **[lofar-astron/DP3](https://github.com/lofar-astron/DP3)** — the LOFAR streaming
  flagging/averaging/calibration pipeline. C++, GPL-3. *In the course:*
  [Ch 39](notebooks/39_rfi_mitigation.ipynb), [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[ratt-ru/QuartiCal](https://github.com/ratt-ru/QuartiCal)** — Dask-based per-antenna Jones-matrix
  calibration (CubiCal's successor). *In the course:* [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[ratt-ru/codex-africanus](https://github.com/ratt-ru/codex-africanus)** — modular RIME / gridding /
  calibration algorithms with GPU support. *Paper:*
  [Perkins et al. 2025, A&C (Africanus I)](https://www.sciencedirect.com/science/article/abs/pii/S2213133725000319).
- **[saopicc/killMS](https://github.com/saopicc/killMS)** — direction-dependent gain solver. *Paper:*
  [Tasse 2014, A&A 566, A127](https://doi.org/10.1051/0004-6361/201423522). *In the course:*
  [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[ska-sa/montblanc](https://github.com/ska-sa/montblanc)** — GPU RIME for Bayesian inference. *Paper:*
  [Perkins et al. 2015, A&C 12, 73](https://doi.org/10.1016/j.ascom.2015.06.003).
- **[lofar-astron/prefactor](https://github.com/lofar-astron/prefactor)** — LOFAR direction-independent
  calibration. *Paper:* [de Gasperin et al. 2019, A&A 622, A5](https://doi.org/10.1051/0004-6361/201833867).
- **[lofar-astron/RMextract](https://github.com/lofar-astron/RMextract)** — ionospheric Faraday-rotation
  correction. *In the course:* [Ch 37](notebooks/37_polarisation_faraday.ipynb).

### Imaging & deconvolution

- **[saopicc/DDFacet](https://github.com/saopicc/DDFacet)** — wide-field, direction-dependent faceted
  imager. *Paper:* [Tasse et al. 2018, A&A 611, A87](https://doi.org/10.1051/0004-6361/201731474).
  *In the course:* [Ch 9](notebooks/09_deconvolution_clean.ipynb).
- **[achael/eht-imaging](https://github.com/achael/eht-imaging)** — the EHT's regularised-maximum-likelihood
  VLBI imaging library (M87 & Sgr A* shadows). Python, GPL-3. *Paper:*
  [Chael et al. 2018, ApJ 857, 23](https://doi.org/10.3847/1538-4357/aab6a8). *In the course:*
  [Ch 19](notebooks/19_eht_and_vlbi.ipynb).
- **[astrosmili/smili](https://github.com/astrosmili/smili)** — sparse-modelling VLBI imaging. *Paper:*
  [Akiyama et al. 2017, AJ 153, 159](https://doi.org/10.3847/1538-3881/aa6302). *In the course:*
  [Ch 19](notebooks/19_eht_and_vlbi.ipynb).
- **[casangi/xradio](https://github.com/casangi/xradio)** — next-gen xarray/Zarr radio data I/O. *In the
  course:* [Ch 16](notebooks/16_data_formats_and_ecosystem.ipynb).

### Visibility data, simulation & sky models

- **[RadioAstronomySoftwareGroup/pyuvdata](https://github.com/RadioAstronomySoftwareGroup/pyuvdata)** —
  read/write/convert UVFITS, Measurement Set, UVH5, MIRIAD. *Paper:*
  [Hazelton et al. 2017, JOSS 2, 140](https://doi.org/10.21105/joss.00140). *In the course:*
  [Ch 12](notebooks/12_vla_imaging.ipynb), [Ch 16](notebooks/16_data_formats_and_ecosystem.ipynb).
- **[RadioAstronomySoftwareGroup/pyuvsim](https://github.com/RadioAstronomySoftwareGroup/pyuvsim)** —
  reference high-precision interferometer simulator. *Paper:*
  [Lanman et al. 2019, JOSS 4, 1234](https://doi.org/10.21105/joss.01234).
- **[ratt-ru/dask-ms](https://github.com/ratt-ru/dask-ms)** — xarray/Dask interface to Measurement Sets.
  *In the course:* [Ch 16](notebooks/16_data_formats_and_ecosystem.ipynb).
- **[ska-sa/katdal](https://github.com/ska-sa/katdal)** + **[katpoint](https://github.com/ska-sa/katpoint)**
  — MeerKAT data access and pointing.

### Spectral cubes, regions & viewers

- **[radio-astro-tools/spectral-cube](https://github.com/radio-astro-tools/spectral-cube)** — lazy,
  WCS-aware analysis of HI/molecular-line cubes. *In the course:* [Ch 11](notebooks/11_hi_rotation_curve.ipynb).
- **[radio-astro-tools/radio-beam](https://github.com/radio-astro-tools/radio-beam)** — synthesised-beam
  handling and common-resolution convolution. *In the course:* [Ch 11](notebooks/11_hi_rotation_curve.ipynb).
- **[radio-astro-tools/pvextractor](https://github.com/radio-astro-tools/pvextractor)** — position-velocity
  diagrams from cubes. *In the course:* [Ch 11](notebooks/11_hi_rotation_curve.ipynb).
- **[astropy/reproject](https://github.com/astropy/reproject)** — WCS reprojection for multi-wavelength
  overlays. *In the course:* [Ch 14](notebooks/14_multiwavelength.ipynb).

### SETI

- **[UCBerkeleySETI/turbo_seti](https://github.com/UCBerkeleySETI/turbo_seti)** — the production Doppler-drift
  technosignature search. *Paper:*
  [Enriquez et al. 2017, ApJ 849, 104](https://doi.org/10.3847/1538-4357/aa8d1b). *In the course:*
  [Ch 21](notebooks/21_seti.ipynb).
- **[UCBerkeleySETI/blimpy](https://github.com/UCBerkeleySETI/blimpy)** — Breakthrough Listen filterbank/GUPPI
  I/O. *Paper:* [Price et al. 2019, JOSS 4, 1554](https://doi.org/10.21105/joss.01554). *In the course:*
  [Ch 21](notebooks/21_seti.ipynb), [Ch 16](notebooks/16_data_formats_and_ecosystem.ipynb).
- **[bbrzycki/setigen](https://github.com/bbrzycki/setigen)** — inject synthetic narrowband signals for
  pipeline validation & ML training. *Paper:* [Brzycki et al. 2022, arXiv:2203.09668](https://arxiv.org/abs/2203.09668).
  *In the course:* [Ch 21](notebooks/21_seti.ipynb).

### SDR toolchains

- **[gnuradio/gnuradio](https://github.com/gnuradio/gnuradio)** — the SDR signal-processing framework.
  C++/Python, GPL-3. *In the course:* [Ch 28](notebooks/28_gnuradio_flowgraphs.ipynb).
- **[osmocom/rtl-sdr](https://github.com/osmocom/rtl-sdr)** + **[librtlsdr/librtlsdr](https://github.com/librtlsdr/librtlsdr)**
  — the RTL2832U userspace driver (`rtl_sdr`, `rtl_power`) and its community fork. C, GPL-2. *In the course:*
  [Ch 5](notebooks/05_sdr_basics.ipynb).
- **[pyrtlsdr/pyrtlsdr](https://github.com/pyrtlsdr/pyrtlsdr)** — Pythonic RTL-SDR access (the `sdr` extra).
  *In the course:* [Ch 5](notebooks/05_sdr_basics.ipynb).
- **[osmocom/gr-osmosdr](https://github.com/osmocom/gr-osmosdr)** — unified GNU Radio source/sink for dozens
  of SDR devices. *In the course:* [Ch 28](notebooks/28_gnuradio_flowgraphs.ipynb).
- **[pothosware/SoapySDR](https://github.com/pothosware/SoapySDR)** — vendor-neutral SDR hardware API. BSL-1.0.
- **[gqrx-sdr/gqrx](https://github.com/gqrx-sdr/gqrx)** — the GUI SDR receiver (spectrum/waterfall) built on
  GNU Radio. *In the course:* [Ch 5](notebooks/05_sdr_basics.ipynb).

### Amateur single-dish, education & planetary

- **[0xCoto/VIRGO](https://github.com/0xCoto/VIRGO)** — open-source spectrometer for amateur radio astronomy
  (HI line, continuum); the `astro-virgo` dependency and the engine behind PICTOR. *Paper:*
  [Spanakis-Misirlis 2021, JOSS 6, 3067](https://doi.org/10.21105/joss.03067). *In the course:*
  [Ch 29](notebooks/29_virgo_pictor.ipynb).
- **[0xCoto/PICTOR](https://github.com/0xCoto/PICTOR)** — the free online 1.5 m radio telescope (web-scheduled
  drift scans). *In the course:* [Ch 29](notebooks/29_virgo_pictor.ipynb).
- **[MITHaystack/srt-py](https://github.com/MITHaystack/srt-py)** — control software for the teaching Small
  Radio Telescope. *In the course:* [Ch 6](notebooks/06_hydrogen_line.ipynb), [Projects](projects.md).
- **[WVURAIL/gr-radio_astro](https://github.com/WVURAIL/gr-radio_astro)** — DSPIRA GNU Radio modules
  (integrating spectrometer for the 21 cm line). *In the course:* [Ch 28](notebooks/28_gnuradio_flowgraphs.ipynb).
- **[myriadrf/RASDR](https://github.com/myriadrf/RASDR)** — the SARA RASDR open-hardware receiver + streamer.
  *In the course:* [Ch 30](notebooks/30_rasdr_radio_sky.ipynb).
- **[maserlib/maser4py](https://github.com/maserlib/maser4py)** — low-frequency & planetary radio format
  readers (Radio JOVE, Voyager/Cassini). *Paper:*
  [Cecconi et al. 2020, DSJ 19, 12](https://doi.org/10.5334/dsj-2020-012). *In the course:*
  [Ch 23](notebooks/23_solar_and_jupiter.ipynb).

### VLF & lightning

- **[ericgibert/supersid](https://github.com/ericgibert/supersid)** — monitor sudden ionospheric
  disturbances from VLF transmitter strength (Stanford/SARA SuperSID). *In the course:*
  [Ch 27](notebooks/27_vlf_ionosphere.ipynb).
- **[daedalus/vlfrx-tools](https://github.com/daedalus/vlfrx-tools)** — GPS-timestamped VLF toolkit
  (sferics, whistlers, meteor scatter). *In the course:* [Ch 40](notebooks/40_lightning_sferics.ipynb),
  [Projects](projects.md).

### 21 cm cosmology, EoR & intensity mapping

The faint cosmological 21 cm signal drives its own software ecosystem — signal simulation,
power-spectrum sensitivity, and the wide-field calibration/imaging that foreground removal demands.

- **[21cmfast/21cmFAST](https://github.com/21cmfast/21cmFAST)** — the canonical semi-numerical
  simulator of the cosmic 21 cm signal through cosmic dawn and reionization. Python/C, MIT. *Paper:*
  [Murray et al. 2020, JOSS 5, 2582](https://doi.org/10.21105/joss.02582). *In the course:*
  [Ch 6](notebooks/06_hydrogen_line.ipynb), [Ch 22](notebooks/22_cosmic_microwave_background.ipynb).
- **[21cmfast/21CMMC](https://github.com/21cmfast/21CMMC)** — MCMC Bayesian inference of EoR
  astrophysics from the 21 cm power spectrum. *Paper:* [Greig & Mesinger 2015](https://arxiv.org/abs/1501.06576).
  *In the course:* [Ch 22](notebooks/22_cosmic_microwave_background.ipynb), [Ch 38](notebooks/38_machine_learning.ipynb).
- **[sambit-giri/tools21cm](https://github.com/sambit-giri/tools21cm)** — analysis of the large-scale
  EoR 21 cm signal (mock LOFAR/MWA/SKA observations, statistics). *Paper:*
  [Giri et al. 2020, JOSS 5, 2363](https://doi.org/10.21105/joss.02363).
- **[steven-murray/powerbox](https://github.com/steven-murray/powerbox)** — Gaussian random fields with
  a specified power spectrum (mock density/21 cm boxes). *Paper:*
  [Murray 2018, JOSS 3, 850](https://doi.org/10.21105/joss.00850).
- **[rasg-affiliates/21cmSense](https://github.com/rasg-affiliates/21cmSense)** — predicted sensitivity
  of a 21 cm array to the EoR power spectrum (thermal noise + foreground avoidance). *Paper:*
  [Pober et al. 2014, ApJ 782, 66](https://ui.adsabs.harvard.edu/abs/2014ApJ...782...66P/abstract).
  *In the course:* [Ch 6](notebooks/06_hydrogen_line.ipynb), [Ch 8](notebooks/08_aperture_synthesis.ipynb).
- **[HERA-Team/hera_pspec](https://github.com/HERA-Team/hera_pspec)** — HERA delay-spectrum / quadratic
  power-spectrum estimation on calibrated visibilities. *In the course:*
  [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[EoRImaging/FHD](https://github.com/EoRImaging/FHD)** — wide-field holographic deconvolution &
  calibration (MWA EoR). IDL, BSD-2. *Paper:*
  [Sullivan et al. 2012, ApJ 759, 17](https://doi.org/10.1088/0004-637X/759/1/17). *In the course:*
  [Ch 9](notebooks/09_deconvolution_clean.ipynb).
- **[MWATelescope/mwa_hyperdrive](https://github.com/MWATelescope/mwa_hyperdrive)** — fast GPU MWA
  calibration. Rust, MPL-2. *In the course:* [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[RadioAstronomySoftwareGroup/healvis](https://github.com/RadioAstronomySoftwareGroup/healvis)** —
  HEALPix-pixel visibility simulator (full-sky, for EoR pipeline tests). *In the course:*
  [Ch 8](notebooks/08_aperture_synthesis.ipynb).
- **[nithyanandan/PRISim](https://github.com/nithyanandan/PRISim)** — precision radio-interferometer
  simulator (transit arrays, foregrounds). *In the course:* [Ch 8](notebooks/08_aperture_synthesis.ipynb).
- **[AaronParsons/aipy](https://github.com/AaronParsons/aipy)** — the PAPER experiment's foundational
  interferometry/calibration/imaging library. *In the course:* [Ch 8](notebooks/08_aperture_synthesis.ipynb),
  [Ch 41](notebooks/41_practical_calibration.ipynb).
- **[radiocosmology/driftscan](https://github.com/radiocosmology/driftscan)** — m-mode transit analysis
  for 21 cm intensity mapping (CHIME). *Paper:* [Shaw et al. 2014, ApJ 781, 57](https://arxiv.org/abs/1302.0327).
  *In the course:* [Ch 22](notebooks/22_cosmic_microwave_background.ipynb).

### Solar & heliophysics radio

Solar radio bursts, dynamic spectra, and the spacecraft radio receivers that track space weather.
(The planetary/solar [maser4py](https://github.com/maserlib/maser4py) above also reads Wind/WAVES &
STEREO/WAVES data.)

- **[sunpy/sunpy](https://github.com/sunpy/sunpy)** — the core solar-physics library (maps, timeseries,
  `Fido` archive access for Wind/STEREO radio). Python, BSD-2. *Paper:*
  [SunPy Community 2020, ApJ 890, 68](https://doi.org/10.3847/1538-4357/ab4f7a). *In the course:*
  [Ch 23](notebooks/23_solar_and_jupiter.ipynb), [Ch 10](notebooks/10_open_archives.ipynb).
- **[sunpy/radiospectra](https://github.com/sunpy/radiospectra)** — solar radio dynamic spectra: reads
  e-Callisto, STEREO/WAVES, Wind/WAVES, RSTN, and Nançay Decameter Array. *In the course:*
  [Ch 23](notebooks/23_solar_and_jupiter.ipynb).
- **[i4Ds/ecallisto_ng](https://github.com/i4Ds/ecallisto_ng)** — fetch & analyse e-Callisto network
  spectrograms (with optional ML flare detection). *Paper:*
  [Benz et al. 2009, SoPh 260, 375](https://ui.adsabs.harvard.edu/abs/2009SoPh..260..375B/abstract).
  *In the course:* [Ch 23](notebooks/23_solar_and_jupiter.ipynb), [Ch 15](notebooks/15_capstone.ipynb).
- **[spedas/pyspedas](https://github.com/spedas/pyspedas)** — download/plot heliophysics CDAWeb data,
  including Wind/WAVES, STEREO/WAVES, PSP/FIELDS, and Solar Orbiter/RPW radio. Python, MIT. *In the
  course:* [Ch 23](notebooks/23_solar_and_jupiter.ipynb).
- **[maserlib/ExPRES](https://github.com/maserlib/ExPRES)** — simulate planetary (and solar-wind-modulated)
  radio emission patterns. *Paper:* [Hess & Zarka 2011, A&A 531, A29](https://doi.org/10.1051/0004-6361/201116510).
  *In the course:* [Ch 23](notebooks/23_solar_and_jupiter.ipynb).
- **[peijin94/LOFAR-Sun-tools](https://github.com/peijin94/LOFAR-Sun-tools)** — LOFAR solar dynamic-spectrum
  & imaging reduction (beam-formed HDF5, RFI, burst onset). *In the course:*
  [Ch 23](notebooks/23_solar_and_jupiter.ipynb).
- **[TCDSolar/SIDpy](https://github.com/TCDSolar/SIDpy)** — process Stanford SuperSID receiver data to
  see solar-flare sudden ionospheric disturbances at VLF. *In the course:*
  [Ch 27](notebooks/27_vlf_ionosphere.ipynb), [Ch 23](notebooks/23_solar_and_jupiter.ipynb).

---

## People — notable maintainers

Authors and maintainers of widely-used radio-astronomy software, with a public GitHub profile and a
representative paper. (Listed for their public, professional open-source work.)

- **Scott Ransom** — [@scottransom](https://github.com/scottransom): [PRESTO](https://github.com/scottransom/presto)
  & co-lead of [PINT](https://github.com/nanograv/PINT). *Paper:*
  [Ransom et al. 2002, AJ 124, 1788](https://doi.org/10.1086/342285). → [Ch 13](notebooks/13_pulsars.ipynb),
  [Ch 20](notebooks/20_pulsar_timing_arrays.ipynb).
- **André Offringa** — [@aroffringa](https://github.com/aroffringa):
  [WSClean](https://gitlab.com/aroffringa/wsclean) & [AOFlagger](https://gitlab.com/aroffringa/aoflagger)
  (primary home on GitLab). *Paper:*
  [Offringa et al. 2014, MNRAS 444, 606](https://doi.org/10.1093/mnras/stu1368). →
  [Ch 9](notebooks/09_deconvolution_clean.ipynb), [Ch 39](notebooks/39_rfi_mitigation.ipynb).
- **Andrew Chael** — [@achael](https://github.com/achael): [eht-imaging](https://github.com/achael/eht-imaging).
  *Paper:* [Chael et al. 2018, ApJ 857, 23](https://doi.org/10.3847/1538-4357/aab6a8). →
  [Ch 19](notebooks/19_eht_and_vlbi.ipynb).
- **Danny C. Price** — [@telegraphic](https://github.com/telegraphic): lead author of
  [blimpy](https://github.com/UCBerkeleySETI/blimpy). *Paper:*
  [Price et al. 2019, JOSS 4, 1554](https://doi.org/10.21105/joss.01554). → [Ch 21](notebooks/21_seti.ipynb).
- **Adam Deller** — [@adamdeller](https://github.com/adamdeller): creator of the
  [DiFX](https://github.com/difx/difx) software correlator (VLBA/LBA/EVN). *Paper:*
  [Deller et al. 2007, PASP 119, 318](https://doi.org/10.1086/513572). → [Ch 19](notebooks/19_eht_and_vlbi.ipynb).
- **Ewan Barr** — [@ewanbarr](https://github.com/ewanbarr): [peasoup](https://github.com/ewanbarr/peasoup)
  (GPU pulsar search) & [sigpyproc](https://github.com/ewanbarr/sigpyproc). →
  [Ch 13](notebooks/13_pulsars.ipynb), [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **Vincent Morello** — [@v-morello](https://github.com/v-morello): [riptide](https://github.com/v-morello/riptide)
  (FFA) & [clfd](https://github.com/v-morello/clfd). *Paper:*
  [Morello et al. 2020, MNRAS 497, 4654](https://doi.org/10.1093/mnras/staa2291). →
  [Ch 13](notebooks/13_pulsars.ipynb), [Ch 39](notebooks/39_rfi_mitigation.ipynb).
- **Devansh Agarwal** — [@devanshkv](https://github.com/devanshkv): [FETCH](https://github.com/devanshkv/fetch)
  (FRB deep-learning classifier). *Paper:*
  [Agarwal et al. 2020, MNRAS 497, 1661](https://doi.org/10.1093/mnras/staa1856). →
  [Ch 18](notebooks/18_fast_radio_bursts.ipynb), [Ch 38](notebooks/38_machine_learning.ipynb).
- **Casey Law** — [@caseyjlaw](https://github.com/caseyjlaw): [realfast / rfpipe](https://github.com/realfastvla/rfpipe)
  (VLA fast-transient search). *Paper:*
  [Law et al. 2018, ApJS 236, 8](https://doi.org/10.3847/1538-4365/aab77b). → [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **Kiyoshi Masui** — [@kiyo-masui](https://github.com/kiyo-masui): [burst_search](https://github.com/kiyo-masui/burst_search)
  & [bitshuffle](https://github.com/kiyo-masui/bitshuffle) (CHIME). *Paper:*
  [Masui et al. 2015, Nature 528, 523](https://doi.org/10.1038/nature15769). → [Ch 18](notebooks/18_fast_radio_bursts.ipynb).
- **Cees Bassa** — [@cbassa](https://github.com/cbassa): [cdmt](https://github.com/cbassa/cdmt) (GPU coherent
  dedispersion). *Paper:* [Bassa et al. 2017](https://arxiv.org/abs/1607.00909). → [Ch 13](notebooks/13_pulsars.ipynb).
- **Apostolos Spanakis-Misirlis** — [@0xCoto](https://github.com/0xCoto):
  [VIRGO](https://github.com/0xCoto/VIRGO) & [PICTOR](https://github.com/0xCoto/PICTOR). *Paper:*
  [Spanakis-Misirlis 2021, JOSS 6, 3067](https://doi.org/10.21105/joss.03067). → [Ch 29](notebooks/29_virgo_pictor.ipynb).

---

## Beyond GitHub (GitLab, SourceForge, Bitbucket)

Several cornerstone tools are *not* primarily on GitHub — listed here so the map is complete.

- **CASA** (Common Astronomy Software Applications) — distributed as pip wheels
  (`pip install casatools casatasks`); there is no public GitHub monorepo. The open layer is
  [casacore](https://github.com/casacore) (above). *Paper:*
  [CASA Team 2022, PASP 134, 114501](https://doi.org/10.1088/1538-3873/ac9642). → [Ch 12](notebooks/12_vla_imaging.ipynb).
- **WSClean** — [gitlab.com/aroffringa/wsclean](https://gitlab.com/aroffringa/wsclean). The dominant
  wide-field imager. *Paper:* [Offringa et al. 2014, MNRAS 444, 606](https://doi.org/10.1093/mnras/stu1368).
- **AOFlagger** — [gitlab.com/aroffringa/aoflagger](https://gitlab.com/aroffringa/aoflagger). The standard
  SumThreshold RFI flagger. *Paper:*
  [Offringa et al. 2010, MNRAS 405, 155](https://doi.org/10.1111/j.1365-2966.2010.16471.x). →
  [Ch 39](notebooks/39_rfi_mitigation.ipynb).
- **RASCIL** — [gitlab.com/ska-telescope/external/rascil-main](https://gitlab.com/ska-telescope/external/rascil-main).
  The SKA's reference imaging library.
- **SatNOGS** — [gitlab.com/librespacefoundation/satnogs](https://gitlab.com/librespacefoundation/satnogs).
  The open global network of satellite ground stations. → [Projects](projects.md).
- **PSRCHIVE** — [psrchive.sourceforge.net](http://psrchive.sourceforge.net). Pulsar archive analysis &
  the PSRFITS standard. *Paper:* [Hotan, van Straten & Manchester 2004, PASA 21, 302](https://doi.org/10.1071/AS04022).
- **DSPSR** — [dspsr.sourceforge.net](http://dspsr.sourceforge.net) (active GitHub mirror:
  [rossjjennings/dspsr](https://github.com/rossjjennings/dspsr)). Coherent dedispersion & folding. *Paper:*
  [van Straten & Bailes 2011, PASA 28, 1](https://doi.org/10.1071/AS10021).
- **heimdall** — [sourceforge.net/projects/heimdall-astro](https://sourceforge.net/projects/heimdall-astro/).
  GPU single-pulse search.
- **GILDAS / CLASS** (IRAM) — [iram.fr/IRAMFR/GILDAS](https://www.iram.fr/IRAMFR/GILDAS/). Single-dish &
  mm-interferometry spectral-line reduction.

---

*This catalogue is curated, not exhaustive — the radio-astronomy software ecosystem is large and moving.
For the organisations and archives behind these tools see [Resources](resources.md); for the hardware and
amateur builds that run them see [Projects, Kits & Hacks](projects.md); for the instruments see
[Radio Telescopes](telescopes.md); for the underlying science see the [Bibliography](references.md).*
