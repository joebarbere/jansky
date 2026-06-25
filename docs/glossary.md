# Glossary

The word you didn't recognise in that paper, defined in a sentence or two. This is an
A–Z of the radio-astronomy terms and jargon the course (and the literature) lean on. For
the **maths symbols** see [notation.md](notation.md); for the **maths itself** —
convolutions, Fourier transforms, coordinates — see
[math-preliminaries.md](math-preliminaries.md).

Where a term has a whole chapter behind it, we point you to it. Definitions are kept
short on purpose; follow the chapter or [References](references.md) for depth.

## A

**Asinh stretch**
: An image display transform, $y = \sinh^{-1}(x/a)$, that is **linear near the noise** and
  **logarithmic for bright pixels** — so a high-dynamic-range radio source shows its faint lobes
  and bright core at once (Lupton et al. 2004). The radio default in `jansky.plotting.radio_norm`
  (Chapter 46).

**Active galactic nucleus (AGN)**
: A compact, luminous core at the centre of a galaxy, powered by accretion onto a
  supermassive black hole. Many are bright radio sources, often with jets and lobes;
  *quasars* are the most luminous AGN.

**AOFlagger / SumThreshold**
: The standard automated RFI-flagging package (AOFlagger) and its core algorithm
  (**SumThreshold**, Offringa et al. 2010): flag windows of increasing length whose mean
  exceeds a threshold that *decreases* with window size, so faint but extended interference
  accumulates above the noise where a single-sample cut would miss it (Chapter 39).

**Antenna temperature ($T_A$)**
: The power a receiver sees from a source, expressed as the temperature of a matched
  resistor that would deliver the same power: $P = k_B T_A \,\Delta\nu$. It is a property
  of the *antenna plus source*, not of the source alone, and is the quantity you actually
  measure (see Chapters 3–4).

**Aperture efficiency ($\eta_A$)**
: The fraction of a dish's geometric area that is effective at collecting signal, after
  losses from surface errors, blockage, illumination taper, and spillover. The effective
  area is $A_e = \eta_A A_{\text{geom}}$, with $\eta_A$ typically 0.5–0.7.

**Aperture synthesis**
: Building up the resolution of a single huge dish by combining many small antennas and
  using Earth's rotation to sample many baseline orientations. The core technique of
  Chapter 8.

## B

**Bandpass**
: The frequency-dependent gain of the instrument across the observing band. *Bandpass
  calibration* divides it out using an observation of a source with a known, flat spectrum
  so that real spectral features aren't confused with instrumental shape.

**Bandwidth ($\Delta\nu$)**
: The width in frequency over which a receiver collects power. Wider bandwidth means more
  collected power and lower noise (see the radiometer equation).

**Baseline**
: The vector between a pair of antennas in an interferometer, usually measured in
  wavelengths. Each baseline samples one spatial frequency of the sky; longer baselines
  give finer angular resolution (Chapters 7–8).

**Beam**
: The angular response pattern of an antenna or array — how sensitive it is as a function
  of direction. In interferometry you meet several: the **primary beam** (the field of view
  of one dish), the **synthesised beam** (the effective resolution of the array, i.e. the
  point-spread function), the **dirty beam** (that PSF including sidelobes from incomplete
  *uv* coverage), and the **clean beam** (an idealised Gaussian fit to it). See Chapters
  8–9.

**Brightness temperature ($T_B$)**
: The temperature a blackbody would need to emit the observed surface brightness at a given
  frequency. In the radio (Rayleigh–Jeans) regime, $T_B \propto I_\nu$, which makes it a
  convenient, frequency-independent way to quote intensity (Chapter 2).

## C

**CASA (Common Astronomy Software Applications)**
: The NRAO software suite for calibrating and imaging interferometer data, used for VLA
  imaging in Chapter 12. It reads and writes Measurement Sets.

**Cosmic dawn**
: The era ($z \sim 15$–30, observed at ~50–90 MHz) when the first stars switched on and their
  Lyman-α photons coupled the 21 cm spin temperature to the cold gas, producing the deep
  absorption trough in the global 21 cm signal that EDGES claimed to detect near 78 MHz
  (Chapter 42).

**CLEAN**
: Högbom's iterative deconvolution algorithm: model the sky as a sum of point sources,
  repeatedly subtracting a scaled dirty beam at the brightest pixel, then restore with a
  clean beam. The workhorse of radio imaging (Chapter 9).

**Closure amplitude**
: A ratio of four visibility amplitudes ($|V_{ij}||V_{kl}| / |V_{ik}||V_{jl}|$) that cancels
  antenna-based *gain* errors. With closure phase, the robust observable that lets sparse VLBI
  arrays like the EHT image black holes (Chapter 19).

**Closure phase**
: The sum of visibility phases around a triangle of baselines, which cancels all
  antenna-based phase errors. It is therefore a robust observable, central to VLBI and to
  self-calibration (Chapter 19).

**CMB (cosmic microwave background)**
: The relic radiation of the hot early universe — a near-perfect 2.725 K blackbody peaking in
  the microwave. Discovered as excess antenna temperature by Penzias & Wilson (1965); see
  Chapter 22.

**CNN (convolutional neural network)**
: A neural network whose layers slide learned filters across the input, giving it
  translation invariance — well matched to image-like data such as the dynamic spectra used to
  classify FRBs vs RFI (Chapter 38).

**Confusion matrix**
: A table of a classifier's predictions vs the true labels (true/false positives and
  negatives), from which accuracy, precision, and recall are read. The basic scorecard for a
  classification model (Chapter 38).

**CME (coronal mass ejection)**
: An eruption of plasma from the Sun whose shock drives a type II radio burst; its speed can be
  read off the burst's frequency drift (Chapter 23).

**CO line**
: The rotational transitions of carbon monoxide (J=1→0 at 115 GHz and its harmonics), the
  standard millimetre tracer of cold molecular gas (Chapter 24).

**Continuum**
: Broadband emission that varies smoothly with frequency, as opposed to narrow spectral
  lines. Synchrotron and thermal (free–free) radiation are continuum sources; continuum
  imaging is the subject of Chapter 12.

**Correlator**
: The hardware (or software) that multiplies and time-averages the signals from every pair
  of antennas to produce visibilities. The beating heart of an interferometer.

**Cross-correlation**
: Multiplying the (time-aligned) signals from two antennas and averaging. The result, as a
  function of baseline, is the visibility — the quantity an interferometer measures.

## D

**Declination (Dec, $\delta$)**
: The celestial-sphere analogue of latitude: angular distance north (+) or south (−) of the
  celestial equator, from $-90°$ to $+90°$. See [math-preliminaries.md](math-preliminaries.md)
  for the coordinate machinery.

**Deconvolution**
: Recovering the true sky from a dirty image by removing the effect of the dirty beam.
  Because *uv* coverage is incomplete, this is an ill-posed problem that needs an algorithm
  like CLEAN to constrain (Chapter 9).

**De-dispersion**
: Removing the frequency-dependent dispersion delay by shifting each channel back in time so a
  broadband pulse re-aligns; the core of pulsar and FRB searches (Chapters 13, 18).

**Doppler drift**
: The slow change in a narrowband signal's frequency from the relative acceleration of
  transmitter and receiver (e.g. a planet's spin and orbit). SETI searches integrate along
  trial drift rates to recover such signals (Chapter 21).

**Dirty beam / dirty image**
: The point-spread function produced by the array's actual (incomplete) *uv* sampling, and
  the raw image you get by Fourier-transforming the visibilities before deconvolution. The
  dirty image is the true sky convolved with the dirty beam (Chapters 8–9).

**Dispersion measure (DM)**
: The integrated free-electron column along the line of sight to a pulsar,
  $\mathrm{DM} = \int n_e\,dl$. Because lower frequencies are delayed more, DM tells you how
  far the signal has travelled through the interstellar medium and must be removed
  ("dedispersed") to recover the pulse (Chapter 13).

**Dynamic range (imaging)**
: The ratio of the brightest pixel to the background noise (RMS) in an image — often $10^4$–$10^6$
  for a radio map of an AGN. It is why a *linear* display shows a single white dot on black, and
  why the asinh/log stretches exist (`jansky.plotting.dynamic_range`, Chapter 46).

**Dynamic spectrum**
: A two-dimensional plot of intensity against time and frequency. Pulses, RFI, and FRBs
  show up as characteristic shapes (a dispersed pulse sweeps from high to low frequency).

## E

**Death line (pulsars)**
: A line on the period–period-derivative ($P$–$\dot P$) diagram below which a rotation-powered
  pulsar can no longer sustain the pair cascades that power coherent radio emission. Long-period
  transients sit far below it (as neutron stars they "shouldn't" emit), which is the central
  puzzle of Chapter 47 (`jansky.transients.death_line_pdot`).

**Epoch folding**
: Finding an unknown period by folding a time series at many trial periods and scoring each folded
  profile (the Leahy $\chi^2$ statistic); the score peaks sharply at the true period. How the
  minutes-to-hours periods of long-period transients are recovered
  (`jansky.transients.epoch_folding_search`, Chapter 47).

**Effective area ($A_e$)**
: The equivalent collecting area of an antenna for a matched source, $A_e = \eta_A
  A_{\text{geom}}$. It sets the gain and, with $T_{\text{sys}}$, the sensitivity via the
  SEFD.

**Emission measure (EM)**
: The line-of-sight integral of the squared electron density, $\mathrm{EM} = \int n_e^2\,
  \mathrm{d}l$ (in pc cm⁻⁶). It sets the free-free optical depth and hence the whole thermal
  spectrum of an HII region — fitting it (with $T_e$) to a radio spectrum measures the density
  and depth of the ionized gas (Chapter 44).

**Equipartition (minimum-energy) field**
: The magnetic field that minimises the total energy in relativistic particles plus field for an
  observed synchrotron source; near the minimum the particle and field energies are comparable.
  It is the standard way to estimate $B$ (a few µG to tens of µG in radio lobes) from the radio
  luminosity and source size (Chapter 43).

**Epoch of Reionization (EoR)**
: The era ($z \sim 6$–10, observed at ~130–200 MHz) when ultraviolet light from the first
  galaxies reionized the neutral intergalactic hydrogen left over from recombination,
  extinguishing the redshifted 21 cm signal. Probed by the 21 cm power spectrum (LOFAR, MWA,
  HERA, SKA-Low) (Chapter 42).

**Ephemeris**
: A table or model giving the predicted position (and for pulsars, the spin phase) of a
  source as a function of time. Pulsar timing uses an ephemeris to predict pulse arrival
  times (Chapter 13).

## F

**Fanaroff–Riley class (FR I / FR II)**
: The morphological split of powerful radio galaxies: **FR I** sources are *edge-darkened*
  (brightest near the core, jets fading outward) and lower-luminosity; **FR II** sources are
  *edge-brightened*, with collimated jets feeding bright lobes and terminal hotspots, and higher
  luminosity. The transition sits near $L_{178\,\mathrm{MHz}} \sim 10^{25}$ W Hz⁻¹ (Fanaroff &
  Riley 1974) (Chapter 45).

**Faraday rotation**
: The rotation of a linearly polarised wave's plane of polarisation as it passes through a
  magnetised plasma, by an angle $\Delta\chi = \mathrm{RM}\,\lambda^2$. The $\lambda^2$
  dependence is the signature that lets the **rotation measure** be recovered (Chapter 37).

**Fast radio burst (FRB)**
: A millisecond-duration, highly dispersed radio flash, mostly extragalactic in origin.
  Their large DMs make them probes of the otherwise-invisible diffuse cosmic baryons.

**Flagging**
: Marking corrupted samples (RFI, dead antennas, edge channels) so they are excluded from
  averaging and imaging. Lossy but essential — too little leaves interference in the data, too
  much throws away signal and biases statistics (Chapter 39; Maths Lab C).

**Flux density ($S_\nu$)**
: Power received per unit area per unit frequency, integrated over the source — measured in
  **janskys**. The fundamental quantity describing how bright a radio source appears.

**Free-free (thermal bremsstrahlung)**
: The thermal continuum radiated by free electrons scattering off ions in ionized gas (HII
  regions, planetary nebulae, the thermal Galactic background). It is **unpolarised** and
  **flat**: optically thick at low frequency ($T_B \to T_e$, $S_\nu \propto \nu^2$) and
  optically thin above the turnover, where the spectral index flattens to $\alpha \approx -0.1$.
  The flat-vs-steep contrast with synchrotron is the standard thermal/non-thermal diagnostic
  (Chapter 44).

**Fringe**
: The sinusoidal interference pattern an interferometer produces as a source moves through
  the beam. Its amplitude and phase are exactly the visibility; "fringe-fitting" solves for
  residual delays and rates (Chapter 7).

**FWHM (full width at half maximum)**
: The width of a peak (a beam, a spectral line, a pulse) measured between the points where
  it drops to half its maximum. A standard, robust measure of "how wide".

## G

**Gain**
: How efficiently an antenna converts incoming flux into measured signal — for a dish,
  $G = A_e/(2k_B)$ in K/Jy. In calibration, "gains" also means the per-antenna complex
  amplitude and phase corrections solved for during reduction.

**Gain calibration**
: Solving for each antenna's complex gain $g_i$ (amplitude and phase, varying with time and
  frequency) — usually from a bright calibrator of known structure — and dividing it out of the
  data. Bandpass calibration is the frequency-dependent case; self-calibration uses the target's
  own model (Chapter 41, Maths Lab E).

**GNU Radio**
: An open-source toolkit for building signal-processing "flowgraphs" from blocks
  (source → filter → FFT → sink); the basis of many amateur radio-astronomy receivers (Chapter 28).

**GUPPI raw**
: A voltage-data file format (FITS-like ASCII header + 8-bit complex samples) from Green Bank /
  Breakthrough Listen backends; the input to the SETI search pipeline (Chapter 16).

## H

**Hanbury Brown–Twiss (HBT) / intensity interferometry**
: Correlating the *intensity* fluctuations of two detectors rather than their amplitudes;
  recovers a source's angular size while needing only modest timing — sidestepping the
  phase-coherence burden of ordinary interferometry (Chapter 25).

**Hellings–Downs curve**
: The characteristic quadrupolar correlation between pulsar pairs as a function of their angular
  separation — the fingerprint of a gravitational-wave background in a pulsar timing array
  (Chapter 20).

**HI / 21 cm line**
: The spectral line of neutral atomic hydrogen at 1420.4 MHz (wavelength 21 cm), from the
  hyperfine spin-flip transition. It traces cold gas across the Galaxy and, via its
  Doppler shift, the rotation of the Milky Way (Chapters 6 and 11).

**Hour angle (HA)**
: How far west of the local meridian a source has moved, measured in time or angle:
  $\mathrm{HA} = \text{LST} - \alpha$. It encodes where a source is in its daily arc across
  the sky.

## I

**Interferometer**
: An array of antennas whose signals are combined to act as one large telescope, achieving
  resolution set by the *longest* baseline rather than by dish size. The subject of Part III.

**Inverse-Compton catastrophe**
: The runaway cooling that caps an incoherent synchrotron source's brightness temperature at
  ~$10^{12}$ K: above it, the relativistic electrons inverse-Compton scatter their own synchrotron
  photons away. Apparent temperatures far higher signal relativistic (Doppler) beaming
  (Chapter 43).

**IQ data**
: Complex baseband samples — *In-phase* (real) and *Quadrature* (imaginary) — that capture
  both amplitude and phase of a signal. The native output of an SDR and of digital
  receivers generally (Chapter 5).

## J

**Jansky (Jy)**
: The unit of flux density, $1\,\mathrm{Jy} = 10^{-26}\,\mathrm{W\,m^{-2}\,Hz^{-1}}$. Named
  for Karl Jansky, who in 1932 first detected radio waves from the Milky Way — and the
  namesake of this course.

## K

**KrakenSDR**
: A five-channel, phase-coherent RTL-SDR (all sharing one clock) that makes amateur
  interferometry and radio direction-finding practical (Chapter 17).

## L

**Long-period radio transient (LPT)**
: A radio source that pulses every few **minutes to hours** — orders of magnitude slower than any
  ordinary pulsar. Since 2022 (GLEAM-X J1627) about a dozen are known; several have now been
  identified as **white-dwarf + M-dwarf binaries** where the period is *orbital*, not a spin, with
  the rest debated between ultra-long-period magnetars and white-dwarf pulsars (Chapter 47).

**log N–log S (source counts)**
: The number of radio sources brighter than flux density $S$ as a function of $S$. In a static,
  uniformly-filled Euclidean universe the integral counts follow $N(>S) \propto S^{-3/2}$
  (differential $\mathrm{d}N/\mathrm{d}S \propto S^{-5/2}$), independent of luminosity. The
  observed departure from this slope — steeper at bright flux, flatter at faint flux — measures
  the cosmic evolution of the source population and helped end steady-state cosmology (Chapter 45).

**LSR (Local Standard of Rest)**
: A reference frame moving with the mean motion of stars in the Sun's neighbourhood around
  the Galaxy. Radial velocities of HI are usually quoted relative to the LSR to remove the
  Sun's peculiar motion (Chapter 11).

## M

**Magnetar**
: A neutron star with an extreme magnetic field ($B \sim 10^{14}$–$10^{15}$ G) whose decaying
  field powers X-ray/gamma-ray bursts and, in a few cases, radio emission. Magnetars sit at the
  top-right of the $P$–$\dot P$ diagram; an *ultra-long-period* magnetar is one candidate
  explanation for long-period radio transients, and a Galactic magnetar (SGR 1935+2154) produced
  an FRB-like burst (Chapters 18, 47).

**Machine learning (ML)**
: Algorithms that learn a task from labelled (or unlabelled) examples rather than from
  hand-coded rules. In radio astronomy, used for FRB/RFI classification, source-finding, and
  parameter estimation — powerful but data-hungry, and only as good as its training set
  (Chapter 38).

**Macquart relation**
: The roughly linear relation between a fast radio burst's dispersion measure and its redshift,
  which turns FRBs into probes of the universe's diffuse "missing" baryons (Chapter 18).

**Maser**
: A microwave laser — naturally occurring, compact, very bright spectral-line emission (e.g.
  H₂O at 22 GHz). Masers orbiting in a Keplerian disk weighed the NGC 4258 black hole (Chapter 24).

**Matched filter**
: The optimal linear detector for a *known* signal shape in white noise: correlate the data with
  a copy of the template. De-dispersion and the SETI drift search are matched filters
  (Chapters 18, 21; Maths Lab B).

**Measurement equation**
: The model relating what an interferometer *records* to the true sky, antenna by antenna:
  $V^\mathrm{obs}_{ij} = g_i\,V^\mathrm{true}_{ij}\,g_j^{*} + n_{ij}$ (and its full polarised,
  matrix form, Hamaker et al. 1996). Calibration inverts it for the gains $g_i$ (Chapter 41).

**Measurement Set (MS)**
: CASA's on-disk data format for visibility data: a set of tables holding the correlated
  data plus all the metadata (antennas, frequencies, pointing). The standard input for
  Chapter 12.

**Meteor scatter**
: Radio reflection off the ionised trail of a meteor; forward-scattering a distant transmitter
  lets amateurs count meteors as brief "pings" (Chapter 26).

## N

**Nanohertz gravitational waves**
: Gravitational waves with ~year periods, from supermassive-black-hole binaries — detectable only
  by pulsar timing arrays via the Hellings–Downs correlation (Chapter 20).

**Noise temperature ($T_N$)**
: The temperature of a fictitious resistor that would generate the same noise power as a
  given component (e.g. the receiver). Adding the noise contributions of every stage gives
  the system temperature.

**Nyquist sampling**
: Sampling a band-limited signal at twice its bandwidth, the minimum rate that preserves all
  its information without aliasing. The reason an SDR's sample rate sets its usable bandwidth
  (Chapter 5).

## P

**Perceptually-uniform colormap**
: A colormap (viridis, inferno, cividis, magma) whose perceived lightness increases monotonically
  with the data, so equal data steps look like equal colour steps. The rainbow/"jet" map is *not*
  uniform — its non-monotonic luminance invents banding that isn't in the data — which is why it
  is avoided here (`jansky.plotting.recommend_cmap`, Chapter 46).

**Parallactic angle**
: The angle between celestial north and the local vertical at a source, which changes as the
  source transits. It matters for alt-az telescopes and for tracking polarisation across an
  observation.

**Phase centre**
: The point on the sky to which the interferometer's phases are referenced (the assumed
  centre of the field). Visibility phase measures position *relative to* the phase centre.

**PICTOR**
: A free online hydrogen-line radio telescope you can point from a web browser; powered by the
  VIRGO package (Chapter 29).

**Plasma frequency ($f_p$)**
: The natural oscillation frequency of an ionised gas, $f_p \propto \sqrt{n_e}$. Radio waves
  below it cannot propagate; in the solar corona it sets the frequency of solar bursts (Chapter 23).

**Polarisation / Stokes parameters**
: The orientation state of the electromagnetic wave. The four **Stokes parameters** $(I, Q,
  U, V)$ fully describe it: $I$ is total intensity, $Q$ and $U$ linear polarisation, $V$
  circular. Synchrotron emission is often linearly polarised, which probes magnetic fields
  (Chapter 37).

**Polarisation fraction & angle**
: The **linear polarisation fraction** $p = \sqrt{Q^2+U^2}/I$ (how polarised the emission is)
  and the **polarisation (E-vector) angle** $\chi = \tfrac12\arctan(U/Q)$ (its orientation). The
  factor of two reflects that polarisation is a "headless vector" — a $\pi$ rotation is the same
  state (Chapter 37).

**Primary beam**
: The single-dish response pattern that sets an interferometer's field of view; sources far
  from the pointing centre are attenuated by it. Correcting for it ("primary-beam
  correction") restores true flux across the image (Chapter 12).

**Pulsar**
: A rapidly rotating, highly magnetised neutron star whose beamed radio emission sweeps past
  us as regular pulses — a cosmic clock. Discovered by Bell and Hewish in 1967; the subject
  of Chapter 13.

**Pulsar timing array (PTA)**
: A set of millisecond pulsars timed for years as a galaxy-scale gravitational-wave detector.
  NANOGrav/EPTA/PPTA reported evidence for a nanohertz GW background in 2023 (Chapter 20).

## Q

**Quasar**
: An extremely luminous AGN, so distant it appears starlike ("quasi-stellar"). Compact radio
  quasars make ideal calibrators and VLBI targets.

## R

**Radio window**
: The range of frequencies (roughly 10 MHz to ~1 THz) at which Earth's atmosphere is
  transparent enough for ground-based radio astronomy, bounded below by the ionosphere and
  above by molecular (mainly water) absorption (Chapter 1).

**Radio luminosity function**
: The space density of radio sources per unit (logarithmic) luminosity. It is steeply
  declining: many faint star-forming galaxies, a break, and a rapidly thinning population of
  rare, powerful radio-loud AGN. Its convolution with cosmic evolution shapes the observed
  source counts (Chapter 45).

**Radio-loud AGN**
: An active galactic nucleus whose accreting supermassive black hole launches powerful
  synchrotron-emitting jets, producing the radio galaxies and radio quasars that dominate the
  bright extragalactic radio sky. Orientation of the jet axis underlies the unified model
  (Chapters 45, 19).

**Radio-quiet zone**
: A legally protected region where radio transmissions are restricted to shield a sensitive
  telescope — e.g. the US National Radio Quiet Zone around Green Bank, or the Murchison
  Radio-astronomy Observatory. A regulatory complement to on-line RFI flagging (Chapter 39).

**Radio recombination line (RRL)**
: A spectral line emitted when an electron recombines into a high-$n$ level of an ion and
  cascades down (e.g. H109α at 5 GHz). Arising from the same ionized gas as free-free emission,
  RRLs give the gas velocity and — combined with the continuum — an independent electron
  temperature (Chapter 44).

**ROC curve & AUC**
: The Receiver Operating Characteristic plots a classifier's true-positive rate against its
  false-positive rate as the decision threshold varies; the Area Under the Curve (AUC, 0.5 =
  chance, 1.0 = perfect) summarises it in one number. The standard way to compare detectors —
  e.g. a learned classifier vs a matched filter (Chapter 38).

**RASDR (Radio Astronomy SDR)**
: A LimeSDR-based amateur radio-astronomy receiver (myriadrf) that streams spectra to Radio-Sky
  Spectrograph over a TCP protocol (Chapter 30).

**Radiometer equation**
: The relation giving the noise on a measurement,
  $\Delta T \approx T_{\text{sys}} / \sqrt{\Delta\nu\,\tau}$ — sensitivity improves with more
  bandwidth and longer integration. The central tool of Chapter 3.

**RFI (radio frequency interference)**
: Human-made signals — phones, radar, satellites, microwave ovens — that contaminate radio
  data. Identifying and excising RFI ("flagging") is a routine and unglamorous part of every
  reduction.

**RM synthesis (Faraday tomography)**
: A Fourier-like transform of the complex polarisation $P(\lambda^2) = Q + iU$ into **Faraday
  depth** $\phi$, reconstructing emission as a function of $\phi$ (Burn 1966; Brentjens & de
  Bruyn 2005). For a single Faraday-thin screen the result peaks at $\phi = \mathrm{RM}$; its
  resolution is set by the $\lambda^2$ coverage via the **RMSF** (Chapter 37).

**Rotation measure (RM)**
: The constant of proportionality in **Faraday rotation**, $\Delta\chi = \mathrm{RM}\,\lambda^2$,
  equal to $0.81\int n_e B_\parallel\,\mathrm{d}l$ (rad m$^{-2}$, with $n_e$ in cm$^{-3}$,
  $B_\parallel$ in µG, $l$ in pc). It measures the line-of-sight magnetic field weighted by
  electron density — the workhorse probe of cosmic magnetism (Chapter 37).

**Right ascension (RA, $\alpha$)**
: The celestial analogue of longitude, measured eastward along the celestial equator,
  usually in hours (0–24h). With declination it fixes a source's position on the sky.

## S

**SED (Saturn Electrostatic Discharge)**
: An impulsive HF radio burst (1–40 MHz) from lightning in Saturn's storms, first seen by
  Voyager and studied in detail by Cassini — planetary lightning detected by exactly the
  dynamic-spectrum and polarimetry methods this course teaches (Chapter 40).

**SEFD (system-equivalent flux density)**
: The flux density of a source that would double the system noise, $\mathrm{SEFD} =
  2k_B T_{\text{sys}} / A_e$, in janskys. A single number summarising an antenna's
  sensitivity — lower is better.

**Sferic**
: The broadband radio impulse ("radio atmospheric") from a lightning return stroke; its energy
  peaks in the VLF band (~5–10 kHz) and propagates globally in the Earth–ionosphere waveguide.
  Sferics are the signal lightning-location networks trilaterate, and a textbook broadband-RFI
  contaminant for radio telescopes (Chapters 40, 39).

**SETI (search for extraterrestrial intelligence)**
: The radio search for artificial narrowband signals (technosignatures), told apart from nature
  by being narrowband and Doppler-drifting (Chapter 21).

**Self-calibration**
: Using a strong source in the field itself to solve for time-varying antenna gains and
  phases, then re-imaging — iterating image and calibration together. It dramatically
  improves dynamic range when closure relations constrain the solution.

**Sidereal time**
: Time kept by the stars rather than the Sun; the **Local Sidereal Time (LST)** equals the RA
  currently on your meridian. A sidereal day is ~4 minutes shorter than a solar day — the
  same 4 minutes by which Jansky's hiss rose earlier each day.

**SigMF**
: An open "Signal Metadata Format" for SDR recordings — a JSON metadata sidecar
  (`.sigmf-meta`) plus a raw binary data file (`.sigmf-data`) (Chapter 16).

**Spectral index ($\alpha$)**
: The power-law slope of a source's spectrum, $S_\nu \propto \nu^{\alpha}$. A steep negative
  index signals synchrotron emission; a flatter or positive one suggests thermal or
  self-absorbed sources — the basis of separating emission mechanisms (Chapter 2).

**Spectral kurtosis**
: A statistic that flags RFI by spotting signals too steady (continuous-wave) or too spiky to be
  natural Gaussian noise; it is ≈ 1 for clean noise (Maths Lab C).

**Spin temperature ($T_S$)**
: The excitation temperature of the 21 cm hyperfine levels, set by a weighted mean of the CMB,
  the gas kinetic temperature (collisions), and the Lyman-α colour temperature (the
  Wouthuysen–Field effect). Whether the cosmological 21 cm line is seen in absorption or emission
  against the CMB depends on $T_S$ vs $T_\mathrm{CMB}$ (Chapter 42).

**Spectral line**
: Emission or absorption confined to a narrow range of frequencies, from a specific atomic
  or molecular transition (e.g. HI at 1420 MHz). Its Doppler shift gives velocity; its width
  gives temperature and turbulence.

**Stokes parameters ($I, Q, U, V$)**
: See **Polarisation / Stokes parameters** (under P) — the four numbers that fully describe a
  wave's polarisation state (Chapter 37).

**Strömgren sphere**
: The roughly spherical zone of fully ionized hydrogen around a hot star, with a sharp edge at
  the **Strömgren radius** where the stellar ionizing-photon rate is balanced by recombinations,
  $Q = \tfrac{4}{3}\pi R_s^3 n_e^2 \alpha_B$. It sets the size of an ionization-bounded HII region
  (Chapter 44).

**Sudden ionospheric disturbance (SID)**
: A jump in a VLF transmitter's received amplitude when a solar flare's X-rays ionise the
  ionospheric D-layer — the basis of SuperSID flare monitoring (Chapter 27).

**Synchrotron radiation**
: Radiation from relativistic electrons spiralling in magnetic fields. It dominates the radio
  continuum of AGN, supernova remnants, and galaxies, with a characteristic power-law,
  often-polarised spectrum; a power-law electron distribution $N(E)\propto E^{-p}$ radiates
  $S_\nu\propto\nu^{\alpha}$ with $\alpha = -(p-1)/2$ (Chapters 2, 43).

**Synchrotron self-absorption (SSA)**
: At low frequency a compact synchrotron source becomes optically thick to its own emission,
  turning the spectrum over to the universal $S_\nu\propto\nu^{5/2}$ slope below the turnover —
  independent of the electron index. The turnover frequency probes the source's size and field
  (Chapter 43).

**Spectral aging**
: The steepening of a synchrotron spectrum above a *break frequency* as radiative (synchrotron +
  inverse-Compton) losses deplete the highest-energy electrons first; the break frequency dates
  the source (Chapter 43).

**Synthesised beam**
: The effective point-spread function of an interferometer, set by its *uv* coverage — the
  array's "resolution element". See **Beam** and Chapter 8.

**System temperature ($T_{\text{sys}}$)**
: The total noise of the whole observing system expressed as a temperature — receiver,
  atmosphere, ground spillover, and sky combined. It is the $T_{\text{sys}}$ in the
  radiometer equation and the single most important sensitivity number (Chapters 3–4).

## T

**Training / validation / test split**
: Partitioning labelled data so a model *learns* on one subset, is *tuned* on a second, and is
  *evaluated* on a held-out third it never saw. Reporting performance on the test set guards
  against over-fitting and over-optimistic accuracy (Chapter 38).

**Tapering / weighting**
: How visibilities are weighted before imaging, trading resolution against sensitivity.
  **Natural** weighting maximises sensitivity (favours short baselines); **uniform** maximises
  resolution; **Briggs/robust** weighting tunes smoothly between the two. *Tapering* further
  down-weights long baselines to emphasise extended structure (Chapters 8–9).

**Technosignature**
: An observable sign of technology — for radio, an artificial narrowband transmission — sought by
  SETI (Chapter 21).

**TOGA (Time of Group Arrival)**
: The refined arrival-time measure used by the Blitzortung lightning network — derived from the
  dispersed sferic's group delay rather than a single onset sample — fed into multilateration to
  geolocate strokes (Chapter 40).

**Tweek**
: A sferic that has propagated far in the night-time Earth–ionosphere waveguide; near the ~1.6–1.8
  kHz waveguide cutoff its group velocity falls to zero, stretching the low-frequency tail into a
  brief descending tone whose cutoff measures the D-layer height (Chapter 40).

**Type II burst**
: A slow-drifting solar radio burst produced by a shock (often a CME) climbing outward through
  the corona; its frequency drift gives the shock speed (Chapter 23).

## U

**u-v plane / visibility**
: The plane of spatial frequencies sampled by an interferometer; each baseline lands at a
  point $(u, v)$. The **visibility** measured there is the Fourier transform of the sky
  brightness (the van Cittert–Zernike theorem), so imaging is an inverse Fourier transform
  (Chapter 8).

## V

**VIRGO**
: An open-source Python package for single-dish spectral-line and continuum radio astronomy; the
  engine behind the PICTOR online telescope (Chapters 16, 29).

**VLBI (very long baseline interferometry)**
: Interferometry with antennas thousands of kilometres apart — even on different continents —
  recording independently and correlating later. It yields the highest angular resolution in
  astronomy (micro-arcseconds), as in the Event Horizon Telescope.

## W

**Whistler**
: Lightning energy that leaked up a geomagnetic field line and dispersed in the magnetospheric
  plasma, returning as a descending tone with group delay $t \propto f^{-1/2}$ — the close cousin
  of the interstellar $t \propto \nu^{-2}$ pulsar/FRB sweep, and de-dispersed by the same machinery
  (Chapters 40, 13, 18).

**Wouthuysen–Field effect**
: The coupling of the 21 cm spin temperature to the gas kinetic temperature by Lyman-α photons
  scattering off neutral hydrogen. Once the first stars provide those photons, it drives the
  cosmic-dawn absorption trough (Chapter 42).

## Z

**Zenith angle**
: The angle of a source from straight overhead (the zenith); $0°$ at the zenith, $90°$ at the
  horizon. Larger zenith angles mean more atmosphere along the line of sight, hence more
  absorption and noise.
