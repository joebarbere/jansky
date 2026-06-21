# Projects, Kits & Hacks

Radio astronomy is one of the few sciences where an amateur can still gather *real,
publishable-quality data* from the backyard. This page is a curated, link-verified field
guide to the projects, kits, full systems, hacks, and parts suppliers that get you
observing — from a salvaged satellite dish you wire up in an afternoon to a turnkey
hydrogen-line observatory.

It pairs with the hands-on hardware chapters of the course —
[Chapter 5: Hands-on SDR](notebooks/05_sdr_basics.ipynb) and
[Chapter 6: Detecting the Hydrogen Line](notebooks/06_hydrogen_line.ipynb) — and with the
institutions and communities listed in [Resources](resources.md). For the underlying
science, see the [References](references.md).

!!! tip "New here? Start with one of these"
    - **[NASA Radio JOVE](https://radiojove.gsfc.nasa.gov/)** — build a simple antenna and
      SDR receiver and hear Jupiter and the Sun at ~20 MHz. The classic on-ramp.
    - **[Itty Bitty Telescope](http://www.opensourceradiotelescopes.org/itty-bitty-radio-telescope/)**
      — a salvaged satellite dish + signal meter that "sees" the warm Sun against the cold sky.
    - **Cheap hydrogen line** — a WiFi grid dish + a 1420 MHz LNA + an RTL-SDR detects the
      21 cm line of galactic hydrogen for ~$200.

*Prices and availability change constantly and are approximate (mid-2026). For RF parts —
LNAs, filters, cables, connectors — prefer reputable vendors over unbranded marketplace
clones, where noise figure and quality vary wildly.*

---

## Kits (you build it)

Buy a box of parts and a guide, assemble, observe.

- **NASA Radio JOVE (2.1)** — The flagship education kit: an SDRplay RSP1B receiver, a
  build-it-yourself dual-dipole antenna, cabling, and Radio-Sky Spectrograph software. It
  listens over ~8 MHz around 20 MHz to capture Jupiter's decametric storms, solar radio
  bursts, and the Milky Way's galactic background. Beginner-to-intermediate.
  [Radio JOVE kits](https://radiojove.gsfc.nasa.gov/kits) · [project home](https://radiojove.gsfc.nasa.gov)
- **Nooelec SAWbird+ H1** — A pocket-sized SAW filter + dual-LNA module centred on
  1420 MHz: the essential front end for detecting the neutral-hydrogen (21 cm) line. Pair
  it with an RTL-SDR and an antenna and you can map galactic hydrogen; ~$45, beginner-friendly.
  [nooelec.com](https://www.nooelec.com/store/sawbird-h1.html)
- **SARA "Scope in a Box"** — A ready-made hydrogen-line starter kit refined by the Society
  of Amateur Radio Astronomers from an RTL-SDR design; parts drop-ship and you get
  instructions plus software. Observes the 21 cm HI line; ~$350 (US shipping).
  [radio-astronomy.org](https://www.radio-astronomy.org/store/projects/scope-in-a-box)
- **MIT Haystack Very Small Radio Telescope (VSRT)** — A classroom *interferometer* from
  off-the-shelf parts; a compact-fluorescent-lamp "radio source" lets students explore
  propagation, polarisation, and interference. Under $500, build-from-plans, grades 8–12.
  [Haystack VSRT](https://www.haystack.mit.edu/edu/pcr/vsrt-ret/index.html)

## Full & turnkey systems

Mostly assembled, higher cost — for schools, universities, and serious hobbyists.

- **MIT Haystack Small Radio Telescope (SRT)** — The classic undergraduate radio telescope:
  a ~2–3 m dish with a 1.4 GHz receiver for the Sun, the hydrogen line, and basic
  spectroscopy. The original commercial kit is retired; Haystack now publishes plans and
  open `srt-py` (Python + GNU Radio) software so institutions self-build.
  [SRT for education](https://www.haystack.mit.edu/haystack-public-outreach/srt-the-small-radio-telescope-for-education/)
  · [srt-py on GitHub](https://github.com/MITHaystack/srt-py)
- **Radio2Space SPIDER 230C** — Entry point to PrimaLuceLab's commercial line: a compact
  1420 MHz hydrogen-line radio telescope with the H142-PRO receiver and RadioUniversePRO
  software. Turnkey but a serious instrument; ~$19,000.
  [Radio2Space SPIDER](https://www.primalucelab.us/radio2space/radio-telescopes-for-radio-astronomy/)
- **Radio2Space SPIDER 300A / 500A** — 3 m and 5 m dishes with automatic tracking for
  universities, museums, and science institutes — enough to map galactic hydrogen and
  measure the Milky Way's rotation. Fully turnkey; ~$49,000 / ~$110,000.
  [Radio2Space SPIDER](https://www.primalucelab.us/radio2space/radio-telescopes-for-radio-astronomy/)

---

## Homebrew & open-source builds

Telescopes you build largely from scratch, from published plans and open designs.

### Online & open-source

- **PICTOR** — A free-to-use online hydrogen-line observatory by Apostolos
  Spanakis-Misirlis: a 1.5 m dish in Athens (feedhorn + two-stage LNA + RTL-SDR + GNU Radio)
  that anyone can point and drift-scan through a web browser — no hardware required. The
  full open hardware/software design is on GitHub if you want to replicate it.
  [pictortelescope.com](https://pictortelescope.com/) · [GitHub](https://github.com/0xCoto/PICTOR)

### Hydrogen-line (21 cm) horn antennas

- **DSPIRA "Sky's the Limit" horn telescope** — The NSF-funded WVU project's flagship
  build: a pyramidal horn from lumber, foil-faced insulation board, and aluminium tape,
  paired with a ~$30 LNA, an RTL-SDR, and a GNU Radio spectrometer. Full lesson plans make
  it the go-to teaching design for the 1420 MHz line.
  [DSPIRA lessons](https://wvurail.org/dspira-lessons/) ·
  [build overview](https://wvurail.org/dspira-lessons/BuildingHornTelescope_Overview) ·
  [open hardware (LNAs)](https://github.com/WVURAIL/os_radio_astro_hw)
- **"Shoestring" DIY hydrogen-line telescope** — A remarkably well-documented build by a
  high-school teacher and a former student: a foil-and-insulation pyramidal horn feeding a
  paint-can waveguide, an H-line LNA + filter, and an Airspy running GNU Radio. A great "how
  it's really done" reference.
  [Hackaday writeup](https://hackaday.com/2019/09/29/probe-the-galaxy-on-a-shoestring-with-this-diy-hydrogen-line-telescope/)
- **Project H Line 3D** — A beginner's guide using an easily fabricated 13-element Yagi
  (~15 dBi) plus LNA and RTL-SDR, with a full software workflow for drift-scanning and
  even 3D-graphing galactic hydrogen. An antenna-focused alternative to a horn.
  [RTL-SDR overview](https://www.rtl-sdr.com/project-h-line-3d-beginners-guide-to-hydrogen-line-antenna-fabrication-reception-software-and-graphic-display/)
- **BHARAT (Bose Horn Antenna Radio Telescope)** — A peer-reviewed (*American Journal of
  Physics*) teaching design from IUCAA, India: an efficient, low-cost dual-mode conical horn
  for 21 cm experiments, used in university lab curricula. More rigorous than the hobbyist
  horns, and openly published. [arXiv:2208.06070](https://arxiv.org/abs/2208.06070)

### Advanced: pulsars & interferometry

- **Amateur pulsar detection of B0329+54** — A milestone homebrew result by Job Geheniau:
  detection of the bright pulsar PSR B0329+54 with a 1.9 m dish + RTL-SDR (software help
  from Michiel Klaassen), reportedly a first at that dish size. A concrete target for dish +
  SDR owners. [RTL-SDR coverage](https://www.rtl-sdr.com/pulsar-b032954-detected-with-a-1-9m-dish-and-rtl-sdr/)
- **Home-built radio interferometer** — NRAO's "Ask an Astronomer" confirms a rudimentary
  two-antenna interferometer is buildable at home and points to worked amateur examples and
  interferometry theory — the most advanced rung of the homebrew ladder.
  [NRAO: home-built interferometer](https://public.nrao.edu/ask/home-built-radio-interferometer/)

---

## Hacks & afternoon experiments

Clever, cheap, repurposing-based observations — many doable in an afternoon. Cost levels
assume you already own a computer.

### Sun & sky with a satellite dish

- **Itty Bitty Radio Telescope (IBT)** — Bolt a satellite-finder signal meter onto a
  discarded TV dish + LNB and sweep the sky: warm objects (trees, buildings, your hand) glow
  against the cold sky, and you'll pick up the Sun at ~12 GHz. The classic near-zero-cost
  beginner build. [NRAO IBT](https://public.nrao.edu/gallery/itty-bitty-teaching-telescope/)
  · [build guide](http://www.opensourceradiotelescopes.org/itty-bitty-radio-telescope/)
- **11.2 GHz dish radio telescope** — A step up: a 1.2 m prime-focus TV dish with a Ku-band
  LNB feeds an SDR (the LNB down-converts ~11 GHz to ~1.4 GHz). Good enough for solar and
  lunar transits and Galactic-plane drift scans.
  [RTL-SDR.com build](https://www.rtl-sdr.com/building-an-11-2-ghz-radio-telescope-with-an-airspy-and-1-2m-tv-satellite-dish/)

### Hydrogen line & passive radar with an RTL-SDR

- **Hydrogen line in an afternoon (~$200)** — A 2.4 GHz WiFi parabolic *grid* dish + a
  1420 MHz LNA + an RTL-SDR Blog dongle, with SDR# and the IF-Average plugin, detects the
  21 cm line and even the Doppler shift of the spinning Galactic plane. The canonical cheap
  radio telescope.
  [RTL-SDR.com tutorial](https://www.rtl-sdr.com/cheap-and-easy-hydrogen-line-radio-astronomy-with-a-rtl-sdr-wifi-parabolic-grid-dish-lna-and-sdrsharp/)
- **Passive radar / aircraft scatter** — Two RTL-SDR dongles on a shared clock turn a local
  FM tower into a passive radar that detects aircraft from reflected signals; a single-dongle
  version watches a VOR beacon for Doppler-shifted echoes.
  [FM passive radar](https://www.rtl-sdr.com/a-fm-radio-passive-radar-system-from-two-rtl-sdr-dongles/)
  · [VOR aircraft scatter](https://www.rtl-sdr.com/passive-doppler-aircraft-scatter-with-a-vor-beacon-and-an-rtl-sdr/)

### Meteors

- **GRAVES meteor scatter (Europe)** — Tune an RTL-SDR just below the 143.050 MHz GRAVES
  radar in France, aim a small VHF antenna skyward, and watch brief "pings" as the radar
  reflects off ionised meteor trails. Cheap and beginner-friendly across much of Europe.
  [RTL-SDR.com: GRAVES meteors](https://www.rtl-sdr.com/using-the-graves-radar-to-listen-to-reflections-from-meteors-planes-and-spacecraft/)
- **FM/VHF meteor pings (worldwide)** — No GRAVES nearby? Tune a VHF receiver to a vacant
  ~88 MHz frequency and point a directional antenna up; distant transmitters reflected off
  meteor trails appear as short bursts.
  [BAA: Meteor Reflections](https://britastro.org/section_information_/radio-astronomy-section-overview/radio-astronomy-basics/meteor-reflections)

### VLF & the ionosphere

- **INSPIRE / natural-radio listening** — A simple VLF receiver lets you *hear* the
  magnetosphere: sferics (lightning pops), tweeks, and whistlers (descending tones guided
  along Earth's field lines). A great no-licence entry hack, best away from mains hum.
  [The INSPIRE Project](https://theinspireproject.org/default.asp?contentID=4)
- **SuperSID / SID monitor** — A small pre-amp and a ~1 m loop antenna feed a sound card to
  watch distant VLF transmitters; when a solar flare hits, the sudden ionospheric disturbance
  shifts the signal and you've detected the flare. Inexpensive, runs indoors 24/7.
  [Stanford SOLAR Center](https://solar-center.stanford.edu/SID/sidmonitor/) ·
  [SARA SuperSID kit](https://www.radio-astronomy.org/store/projects/supersid)

### Lightning & sferics

Lightning is the loudest natural radio source you can hear from the backyard: every return
stroke radiates a broadband impulse that peaks in the VLF band (~5–10 kHz) and reaches up into
VHF. Those impulses — **sferics** — bounce around the Earth–ionosphere waveguide as **tweeks**
and, when they leak up a geomagnetic field line and disperse, return as whistling **whistlers**.
The physics is the same plasma dispersion you meet with pulsars and FRBs (a whistler's group
delay goes as $t \propto f^{-1/2}$, the close cousin of the interstellar $t \propto \nu^{-2}$),
and lightning is also a textbook *broadband RFI* source that radio observatories must flag — so
these builds tie straight back to [Chapter 13 (Pulsars)](notebooks/13_pulsars.ipynb),
[Chapter 18 (FRBs)](notebooks/18_fast_radio_bursts.ipynb),
[Chapter 27 (VLF & the Ionosphere)](notebooks/27_vlf_ionosphere.ipynb), and
[Chapter 39 (RFI Mitigation)](notebooks/39_rfi_mitigation.ipynb). The same techniques even
detect lightning on *other planets* — Saturn's electrostatic discharges and Jupiter's whistlers
were found by Voyager, Cassini, and Juno.

- **Join Blitzortung / LightningMaps (citizen-science geolocation)** — The most rewarding build:
  a small VLF loop/ferrite antenna and a GPS-timestamped controller board upload sferic arrival
  times to a global server, which trilaterates each strike by **time-of-arrival** (the same
  hyperbolic geometry as VLBI in [Chapter 19](notebooks/19_eht_and_vlbi.ipynb)). Hundreds of
  stations feed the live map; kits are ~$50–200 and the data are free to use.
  [How to cover your area](https://www.blitzortung.org/en/cover_your_area.php) ·
  [live map](https://www.lightningmaps.org/) ·
  [WWLLN (the academic network)](https://wwlln.net/)
- **AS3935 "Franklin" lightning sensor** — A single I²C/SPI chip with a 500 kHz resonant front
  end and an on-board classifier that flags strikes vs man-made "disturbers" and estimates
  distance (1–40 km). Cheap (~$25) and Raspberry-Pi/Arduino-friendly — great for a "storm is
  approaching" alarm, though it's single-station (no direction or geolocation) and its 500 kHz
  band misses the VLF energy peak.
  [SparkFun hookup guide](https://learn.sparkfun.com/tutorials/sparkfun-as3935-lightning-detector-hookup-guide-v20) ·
  [ScioSense AS3935](https://www.sciosense.com/as3935-franklin-lightning-sensor-ic/)
- **Soundcard / RTL-SDR sferic & whistler receiver** — Because VLF lightning emission lands in
  the audio band, a loop antenna + high-gain pre-amp + a 96 kHz sound card records raw sferics,
  tweeks, and whistlers with no down-conversion — point a spectrogram at it and the descending
  whistler tones appear directly. (An RTL-SDR with an upconverter, or HF direct-sampling, catches
  the "crashes" higher up the band.) The open-source [vlfrx-tools](https://github.com/daedalus/vlfrx-tools)
  toolkit adds GPS-locked timing and sferic analysis; the
  [INSPIRE Project](https://theinspireproject.org/default.asp?contentID=4) (already above) is the
  classic listen-first on-ramp.

---

## Sources for radio-astronomy parts

Where to buy the components for the projects above.

### Software-defined radios (SDRs)

- **RTL-SDR Blog** — The reference budget dongle (Blog V4); also sells the radio-astronomy
  Discovery Dish. Best starting point for hydrogen-line work.
  [rtl-sdr.com store](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/)
- **Nooelec** — NESDR family of RTL-SDR dongles, including bias-tee "SMArTee" models that
  power an LNA over coax. [nooelec.com](https://www.nooelec.com/store/)
- **Airspy** — Higher-dynamic-range receivers (R2, HF+ Discovery) when 8-bit isn't enough.
  [airspy.com](https://airspy.com/)
- **SDRplay** — RSP series (RSP1B, RSPdx, RSPduo) with 14-bit ADCs and free software.
  [sdrplay.com](https://www.sdrplay.com/)
- **HackRF (Great Scott Gadgets)** — Open-source 1 MHz–6 GHz transmit/receive SDR.
  [greatscottgadgets.com](https://greatscottgadgets.com/hackrf/one/)
- **Ettus Research / USRP** — High-end, calibrated USRP platforms for instrumentation budgets.
  [ettus.com](https://www.ettus.com/)
- **KrakenSDR** — Five RTL-SDR receivers on one board sharing a single clock, phase-coherent
  by design — the affordable on-ramp to amateur *interferometry* and direction finding (a
  stock RTL-SDR has no external clock input, which is what makes coherent multi-receiver work
  hard; see [Field Notes](field-notes.md#interferometry-is-genuinely-hard)). ~$450.
  [krakenrf.com](https://www.krakenrf.com/)

### Low-noise amplifiers (LNAs) & filters

- **Nooelec** — SAWbird+ H1 (1420 MHz SAW filter + cascaded LNA, purpose-built for the
  hydrogen line) and the wideband LaNA.
  [SAWbird+ H1](https://www.nooelec.com/store/sawbird-h1.html) ·
  [LaNA](https://www.nooelec.com/store/lana.html)
- **RTL-SDR Blog** — Wideband bias-tee LNA (50 MHz–4 GHz, <1 dB NF) plus band-stop/high-pass
  filters. [rtl-sdr.com store](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/)
- **Mini-Circuits** — Lab-grade connectorised LNAs (ZX60 series), bias tees, attenuators,
  and filters; the professional choice. [minicircuits.com](https://www.minicircuits.com/)
- **LNA4ALL** — Popular DIY-favourite wideband LNA (PSA4-5043+, ~0.75 dB NF).
  [lna4all.blogspot.com](http://lna4all.blogspot.com/)
- **Mini-Kits (AU)** — Low-noise amplifier and preamp kits/modules for HF–microwave.
  [minikits.com.au](https://www.minikits.com.au/rf-low-noise)

### Antennas, feeds, horns & dishes

- **RTL-SDR Blog Discovery Dish** — Near off-the-shelf lightweight dish + 1420 MHz feed
  (integrated LNA/filter) for hydrogen-line and L-band reception.
  [rtl-sdr.com store](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/)
- **WiFi grid antennas (2.4 GHz parabolic grids)** — Cheap ~1 m grid dishes repurposed with
  a 1.4 GHz feed are a classic budget hydrogen-line telescope; sold by networking retailers
  and surplus channels.
- **Surplus satellite dishes** — Offset Ku-band TV dishes and old C-band dishes make good
  reflectors; source from classifieds, ham swaps, and university surplus (see below).
- **DIY horns & cantennas** — Pyramidal horn / waveguide-can feeds from sheet metal, paint
  cans, or foil board. Build references:
  [Lichfield RAO horn guide](https://www.astronomy.me.uk/how-to-build-a-horn-antenna-at-1420-mhz)
  · [PhysicsOpenLab](https://physicsopenlab.org/2020/07/20/horn-antenna-for-the-21cm-neutral-hydrogen-line/).
- **Pasternack** — Commercial waveguide-to-coax adapters and feed hardware.
  [pasternack.com](https://www.pasternack.com/)

### Connectors, cable & RF bits

- **Digi-Key** · **Mouser** · **Newark/element14** — The three major distributors: SMA/N/F
  connectors, adapters, attenuators, bias tees, and coax, in stock with fast shipping.
  [digikey.com](https://www.digikey.com/) · [mouser.com](https://www.mouser.com/) ·
  [newark.com](https://www.newark.com/)
- **Pasternack** — RF specialist: connectors, adapters, attenuators, jumper cables, off the
  shelf. [pasternack.com](https://www.pasternack.com/)
- **L-com** — Pre-made LMR-400 and low-loss coax jumper assemblies plus bulk cable.
  [l-com.com](https://www.l-com.com/)
- **Amphenol RF** — Connector manufacturer (SMA, N, F, MCX…); buy through the distributors
  above. [amphenolrf.com](https://www.amphenolrf.com/)

### Surplus, generic & maker sources

- **Adafruit** · **SparkFun** — Maker-friendly sources for the HackRF, RTL-SDR kits, and
  general electronics. [adafruit.com](https://www.adafruit.com/) ·
  [sparkfun.com](https://www.sparkfun.com/)
- **eBay** · **AliExpress** · **Amazon** — Surplus dishes, LNAs, connectors, and dongles,
  often cheap. *Caution:* many unbranded RF parts are clones with poor or unspecified noise
  figure — verify the seller and specs, and prefer genuine branded gear for the front end.
  [ebay.com](https://www.ebay.com/) · [aliexpress.com](https://www.aliexpress.com/) ·
  [amazon.com](https://www.amazon.com/)
- **University surplus & ham-radio swap meets** — Excellent for free/cheap dishes, coax,
  connectors, and test gear. Check local hamfests and your nearest university's surplus sales.

---

## Communities & going further

You don't have to go it alone — amateur radio astronomy is small, friendly, and open.

- **Society of Amateur Radio Astronomers (SARA)** — The hub: projects, the *Radio Astronomy*
  journal, conferences, and a [Getting Started](https://www.radio-astronomy.org/getting-started)
  guide that ties together Radio JOVE, SuperSID, INSPIRE, the IBT, and meteor work.
  [radio-astronomy.org](https://www.radio-astronomy.org/)
- **British Astronomical Association — Radio Astronomy Group** — Active UK community with
  beginner guides and projects.
  [britastro.org](https://britastro.org/section_information_/radio-astronomy-section-overview)
- **Open Source Radio Telescopes** — A community catalogue of open, reproducible builds.
  [opensourceradiotelescopes.org](http://www.opensourceradiotelescopes.org/)
- **Cloudy Nights — scientific/amateur astronomy forum** — A large, friendly community whose
  scientific subforum is an active place to ask radio-astronomy questions.
  [cloudynights.com](https://www.cloudynights.com/forum/88-scientific-amateur-astronomy/)
- **SatNOGS** — A global network of open-source satellite ground stations; a great way to put
  an SDR + antenna to collaborative use. [satnogs.org](https://satnogs.org/)
- **saveitforparts (YouTube)** — Entertaining, instructive builds of radio telescopes and
  satellite receivers from salvaged parts. [youtube.com/@saveitforparts](https://www.youtube.com/@saveitforparts)

!!! tip "You can always just listen"
    Radio astronomy is **receive-only** — no licence required. (A licence is only for
    *transmitting*.) Before buying anything, you can even tune real receivers over the web with
    [WebSDR](http://websdr.org/) or [KiwiSDR](http://kiwisdr.com/).

For more hard-won practical advice from the amateur community — what's actually discoverable,
the hardware gotchas, why interferometry is hard, and the RFI traps — see
[Field Notes from the Community](field-notes.md).

For observatories, archives, university groups, and journals, see [Resources](resources.md);
for the foundational papers behind these experiments, see the [References](references.md).
