# Reading the Notation

Open almost any radio-astronomy paper and within a paragraph you will meet a
dense thicket of Greek letters, decorated variables, and units that the authors
assume you already speak. This page is a **decoder ring**. You spot an unfamiliar
symbol or convention in a paper, you look it up here.

This is the *syntax* companion to two sibling references:

- **[Math Preliminaries](math-preliminaries.md)** — *teaches* the underlying
  mathematics (Fourier transforms, complex numbers, statistics). Come here for
  *how to read* a symbol; go there for *how it works*.
- **[Glossary](glossary.md)** — defines the *words* (e.g. "visibility",
  "system temperature", "column density"). Come here for the *symbol*; go there
  for the *concept in prose*.

The aim below is to help you **parse an equation**, not to re-teach the physics.
Where a symbol first appears in the course, the relevant chapter is noted.

!!! tip "The golden rule of notation"
    Notation is **local**. A symbol means whatever the author defined it to mean,
    usually near its first appearance or in a table of symbols. The conventions
    below are *strong priors*, not laws. Always check the paper's own definitions
    first — especially for $\alpha$, $*$, and the sign of an exponent.

---

## 1. Greek letters in common use

Radio astronomy leans heavily on the Greek alphabet, and several letters carry
more than one meaning. The right reading is almost always fixed by context (an
angle on the sky vs. a statistical quantity, for instance).

| Symbol | Name | Usual meaning in radio astronomy | Watch out |
|--------|------|----------------------------------|-----------|
| $\nu$ | nu | **frequency** (Hz) — the radio astronomer's default x-axis | looks like Latin *v*; $\nu$ has the little tail |
| $\lambda$ | lambda | **wavelength** (m); $\lambda = c/\nu$ | also eigenvalue in linear algebra |
| $\alpha$ | alpha | **spectral index** ($S_\nu \propto \nu^\alpha$) **or right ascension** | the big clash — see §5 |
| $\delta$ | delta (lower) | **declination** (sky latitude); also a small increment | distinct from $\Delta$ |
| $\theta$ | theta | an **angle** — beamwidth, zenith angle, scattering angle | often the angular size $\theta_\mathrm{FWHM}$ |
| $\phi$, $\varphi$ | phi | **azimuth / phase angle**; also Galactic-rotation azimuth | $\Phi$ (capital) often a flux or potential |
| $\Omega$ | omega (cap) | **solid angle** (steradians); beam solid angle $\Omega_A$, $\Omega_\mathrm{MB}$ | $\omega$ (lower) = angular frequency $2\pi\nu$ |
| $\sigma$ | sigma (lower) | **standard deviation / RMS noise**; also a **cross-section** $\sigma$ (cm$^2$) | rms vs. cross-section is pure context |
| $\Sigma$ | sigma (cap) | **summation** $\sum$; also a surface density $\Sigma$ | the operator vs. the quantity |
| $\tau$ | tau | **optical depth** (dimensionless) **or integration time** (s) | depth in radiative transfer; time in the radiometer eqn |
| $\rho$ | rho | **correlation coefficient**; also a mass density $\rho$ | |
| $\Delta$ | delta (cap) | a **difference or interval**: $\Delta\nu$ (bandwidth), $\Delta T$ (noise) | "change in", not a value itself |
| $\mu$ | mu | the prefix **micro-** ($10^{-6}$, e.g. $\mu$Jy); also a **mean** $\mu$ | $\mu$Jy is microjansky |
| $\eta$ | eta | an **efficiency** (aperture $\eta_A$, beam $\eta_B$, main-beam) $\in [0,1]$ | |
| $\kappa$ | kappa | **opacity / absorption coefficient** ($\kappa_\nu$, cm$^2$ g$^{-1}$ or cm$^{-1}$) | |
| $\epsilon$, $\varepsilon$ | epsilon | **emissivity / emission coefficient** $\epsilon_\nu$; also a small quantity | |
| $\Phi$ | phi (cap) | a **flux** (e.g. photon flux) **or a phase / potential** | |
| $\chi$ | chi | **$\chi^2$** the goodness-of-fit statistic; also an angle | almost always seen as $\chi^2$ |
| $\beta$ | beta | a **velocity in units of $c$**, $\beta = v/c$; also a power-law slope | |
| $\gamma$ | gamma | **Lorentz factor** $\gamma = (1-\beta^2)^{-1/2}$; also a power-law index | |
| $\pi$ | pi | the constant $3.14159\ldots$ (and $2\pi$ everywhere in Fourier work) | |
| $\psi$ | psi | a **position angle** or phase | |
| $\zeta$, $\xi$ | zeta, xi | generic dummy variables of integration | |

!!! note "Disambiguating multi-use letters"
    - $\alpha$: if it sits in an exponent on $\nu$ or appears with $\delta$ as a
      coordinate pair $(\alpha,\delta)$, it is **right ascension**; otherwise
      it is the **spectral index**.
    - $\tau$: inside $e^{-\tau}$ it is **optical depth**; under a square root with
      a bandwidth it is **integration time**.
    - $\sigma$: next to a measurement ("$3\sigma$ detection") it is **noise**;
      next to a number density it is a **cross-section**.

---

## 2. Core radio-astronomy symbols

These are the workhorses. The subscript $\nu$ (or $_\lambda$) almost always reads
"per unit frequency" — i.e. a *spectral* density (Ch. 1–2).

| Symbol | Reads as | Typical units | First seen |
|--------|----------|---------------|------------|
| $S_\nu$ | **flux density** at frequency $\nu$ | Jy ($=10^{-26}$ W m$^{-2}$ Hz$^{-1}$) | Ch. 1 |
| $I_\nu$, $B_\nu$ | **specific intensity** / **brightness** ($B_\nu$ = Planck) | W m$^{-2}$ Hz$^{-1}$ sr$^{-1}$ | Ch. 1–2 |
| $T_b$ | **brightness temperature** (temp. of a blackbody giving that $I_\nu$) | K | Ch. 1 |
| $T_\mathrm{sys}$ | **system temperature** (total noise power as a temperature) | K | Ch. 3 |
| $T_A$ | **antenna temperature** (signal power as a temperature) | K | Ch. 3–4 |
| $T_\mathrm{rx}$ | **receiver temperature** (noise added by the electronics) | K | Ch. 4 |
| $A_\mathrm{eff}$, $A_e$ | **effective collecting area** of the antenna | m$^2$ | Ch. 4 |
| $\Omega_A$ | **(antenna) beam solid angle** | sr | Ch. 4 |
| $G$ | **gain** (telescope K/Jy, or amplifier gain) | K Jy$^{-1}$ or dimensionless | Ch. 4 |
| $\mathrm{SEFD}$ | **system-equivalent flux density** ($= 2kT_\mathrm{sys}/A_e$) | Jy | Ch. 3–4 |
| $V(u,v)$, $\mathcal{V}$ | **visibility** — the complex correlator output | Jy (complex) | Ch. 7–8 |
| $u,v,w$ | **baseline coordinates** in wavelengths ($uv$-plane = sky FT plane) | $\lambda$ (wavelengths) | Ch. 8 |
| $\mathbf{b}$, $B$ | **baseline** vector / length between two antennas | m (or $\lambda$) | Ch. 7 |
| $l,m$ | **direction cosines** on the sky (image-plane coordinates) | dimensionless | Ch. 8 |
| $b$, $\ell$ | **Galactic latitude / longitude** (note: $\ell$ also = longitude) | deg | Ch. 11 |
| $z$ | **redshift** ($1+z = \nu_\mathrm{emit}/\nu_\mathrm{obs}$) | dimensionless | Ch. 14 |
| $\mathrm{DM}$ | **dispersion measure** (integrated electron column to a pulsar) | pc cm$^{-3}$ | Ch. 13 |
| $N_\mathrm{H}$, $N_\mathrm{HI}$ | **column density** of (neutral) hydrogen | cm$^{-2}$ | Ch. 11 |
| $\mathrm{EM}$ | **emission measure** ($\int n_e^2\,dl$) | pc cm$^{-6}$ | Ch. 2 |
| $v_\mathrm{LSR}$ | **velocity w.r.t. the Local Standard of Rest** | km s$^{-1}$ | Ch. 11 |
| $k$, $k_B$ | **Boltzmann constant** ($1.38\times10^{-23}$ J K$^{-1}$) | — | Ch. 1 |
| $h$ | **Planck constant** (or, lowercase in cosmology, $H_0/100$) | — | Ch. 2 |

---

## 3. Operators & decorations

What the marks *on* and *around* a variable do to it.

| Notation | Reads as | Notes |
|----------|----------|-------|
| $f * g$ | **convolution** | the beam smears the sky: (true sky) $*$ (beam) |
| $z^*$ | **complex conjugate** | same star, different job — see §5; conjugate flips the sign of the imaginary part |
| $\langle x \rangle$ | **ensemble / time average** | the expectation of $x$; in noise theory $\langle x\rangle$ often $=0$ |
| $\hat{x}$ | **unit vector**, **estimate**, *or* **Fourier transform** | $\hat{\mathbf{n}}$ = direction; $\hat{\theta}$ = an estimator; $\hat{f}(\nu)$ = the FT of $f$ |
| $\bar{x}$ | **mean** of $x$ (sometimes complex conjugate) | overbar = average; in some texts $\bar{z}$ = conjugate |
| $\tilde{x}$ | a **transformed / modified** quantity | often "$x$ in the Fourier domain" or a smoothed version |
| $x_\mathrm{rms}$, $\sigma_x$ | the **root-mean-square / scatter** of $x$ | |
| $\propto$ | **is proportional to** | drops all constants: $S_\nu \propto \nu^\alpha$ |
| $\sim$ | **"of order" / "scales as"** | an order-of-magnitude statement, looser than $\approx$ |
| $\approx$ | **approximately equal** | a genuine numerical near-equality |
| $\equiv$ | **is defined to be** | introduces a definition, not a derived result |
| $\nabla$ | **gradient / vector derivative** ("del") | $\nabla\cdot$ divergence, $\nabla\times$ curl |
| $\partial$ | **partial derivative** | $\partial I_\nu/\partial s$ along a ray |
| $\int$, $\iint$ | **integral**, **double integral** | $\iint \cdots\, dl\, dm$ integrates over the sky |
| $\sum$, $\prod$ | **sum**, **product** over an index | |
| $\lvert z\rvert$ | **magnitude / modulus** | amplitude of a complex visibility |
| $\arg z$ | **argument / phase** | the phase angle of a complex number |
| $\mathcal{F}\{\cdot\}$ | the **Fourier-transform operator** | $\mathcal{F}^{-1}$ is the inverse; sky $\leftrightarrow$ visibilities |
| $\mathbf{b}$, $\vec{b}$ | a **vector** | **bold** and $\vec{\ }$ arrow are interchangeable conventions |

**Subscripts & superscripts.** A subscript usually *specifies* (which quantity:
$T_\mathrm{sys}$, $S_\nu$, $\Omega_A$); a superscript usually *modifies* (a power
$\nu^\alpha$, or a label like $T^\mathrm{atm}$). Numerical subscripts often pin a
reference value: $\nu_0$, $T_0$, $H_0$ all mean "at the fiducial / present epoch".

!!! warning "The two stars"
    `*` is overloaded. As an operator *between* two functions, $f*g$, it is
    **convolution**. As a superscript *on* a single symbol, $z^*$, it is the
    **complex conjugate**. A correlator computes $V \propto \langle E_1 E_2^*\rangle$
    — both stars in one expression. See §5.

---

## 4. Units & their conventions

| Unit | Reads as | Notes |
|------|----------|-------|
| Jy | **jansky** | $1\,\mathrm{Jy} = 10^{-26}\,\mathrm{W\,m^{-2}\,Hz^{-1}}$; mJy, $\mu$Jy common |
| Jy/beam | **jansky per beam** | the unit of a *map* pixel before deconvolution — see below |
| K | **kelvin** | as a *brightness temperature*, not a physical temperature, in maps |
| K km s$^{-1}$ | brightness $\times$ velocity | the integrated-line unit (Ch. 11), $\propto N_\mathrm{H}$ |
| pc cm$^{-3}$ | parsec per cm$^{3}$ | the DM unit — a column of electrons (Ch. 13) |
| cm$^{-2}$ | per square cm | column density $N_\mathrm{H}$ (Ch. 11) |
| dB | **decibel** | $10\log_{10}$ of a power ratio (gain, dynamic range) |
| mag | **magnitude** | logarithmic, *backwards*: brighter = smaller (Ch. 14) |
| dex | **"decimal exponent"** | one dex = one factor of 10 (a unit of log-spacing) |

**Frequency, wavelength, velocity are interchangeable.** Spectral axes get
labelled in any of three ways, related by $\lambda=c/\nu$ and a Doppler shift.
The radio community uses the **radio velocity convention**:

$$
v_\mathrm{radio} = c\,\frac{\nu_0 - \nu}{\nu_0},
$$

which differs from the *optical* convention $v_\mathrm{opt} = c(\lambda-\lambda_0)/\lambda_0$.
The two disagree at high $z$ — always check which a paper uses (Ch. 11, 14).

!!! warning "cgs vs SI"
    Much of the classic literature (and `Essential Radio Astronomy`) works in
    **cgs-Gaussian** units: ergs, cm, gauss, and intensities in
    erg s$^{-1}$ cm$^{-2}$ Hz$^{-1}$ sr$^{-1}$. Modern code and this course
    lean **SI** (W, m, tesla). Factors of $10^{7}$, $10^{4}$, and $4\pi$ between
    the systems are a classic source of silent errors. Check the units on $k$,
    $\sigma_T$, and $\kappa_\nu$ before plugging numbers in.

**Common prefixes:** k ($10^3$), M ($10^6$), G ($10^9$, as in GHz), T ($10^{12}$);
and down: m ($10^{-3}$), $\mu$ ($10^{-6}$), n ($10^{-9}$), p ($10^{-12}$).

!!! note "Why \"per beam\"?"
    A radio interferometer map is the true sky **convolved** with the instrument's
    point-spread function (the "dirty/clean beam"). A point source therefore spreads
    its flux over a beam-sized blob, so each pixel carries *flux density per beam
    area*, i.e. **Jy/beam**. To recover a source's total flux in Jy you integrate
    over the source and divide by the beam area (in pixels). This is why **beam $\ne$
    pixel** matters — see §5.

---

## 5. Conventions & gotchas

A short field guide to the traps that cost real time.

**Spectral-index sign.** The spectral index $\alpha$ is defined by a power law,
but *the sign convention is not universal*:

$$
S_\nu \propto \nu^{+\alpha} \qquad\text{vs.}\qquad S_\nu \propto \nu^{-\alpha}.
$$

With the $+\alpha$ convention, synchrotron sources have $\alpha \approx -0.7$
(negative); with the $-\alpha$ convention the same source has $\alpha \approx +0.7$.
A paper will state which it uses; if a "steep-spectrum" source is quoted with a
*positive* index, you are in the $-\alpha$ camp (Ch. 2).

**The $\alpha$ collision.** $\alpha$ is *both* the spectral index *and* right
ascension. They essentially never appear in the same equation, and context
separates them instantly: paired with $\delta$ it is a coordinate; sitting on
$\nu$ it is a slope. (§1)

**The $*$ collision.** Convolution ($f*g$) vs. complex conjugate ($z^*$). Position
disambiguates: between functions it convolves; as a superscript it conjugates. (§3)

**Fourier sign and $2\pi$.** Fourier transforms come in several conventions that
differ by the sign in the exponent and where the $2\pi$ lives:

$$
\hat f(s)=\int f(x)\,e^{\mp 2\pi i s x}\,dx
\quad\text{or}\quad
\hat f(k)=\frac{1}{\sqrt{2\pi}}\int f(x)\,e^{\mp i k x}\,dx .
$$

Radio interferometry conventionally uses $e^{-2\pi i(ul+vm)}$ for the
sky $\to$ visibility direction (Ch. 8). A flipped sign mirror-images your map;
a misplaced $2\pi$ rescales it. See [Math Preliminaries](math-preliminaries.md).

**RA in hms vs degrees.** Right ascension is written either in **time units**
($\mathrm{h\,m\,s}$, e.g. `05h34m31s`) or in **degrees**, with
$1^\mathrm{h} = 15^\circ$. Declination is always degrees (`+22d00m52s`).
A common bug: feeding an hms RA to code expecting degrees, off by a factor of 15.

**Epoch / equinox.** Coordinates depend on the date of the reference frame.
**J2000** (equinox 2000.0, ICRS for practical purposes) is today's default;
older catalogues use **B1950**. Mixing them shifts positions by tenths of a degree
(Ch. 10, 12).

**Beam vs. pixel.** A *pixel* is a sampling grid cell; a *beam* is the instrument's
resolution element, typically several pixels across. Photometry, noise statistics,
and "Jy/beam $\to$ Jy" conversions all depend on the beam, not the pixel (§4, Ch. 9, 12).

**FWHM vs. $\sigma$.** A Gaussian beam is quoted either by its **full width at half
maximum** or by its **standard deviation** $\sigma$. They are not the same number:

$$
\theta_\mathrm{FWHM} = 2\sqrt{2\ln 2}\;\sigma \approx 2.355\,\sigma .
$$

Telescope beams are almost always given as FWHM; smoothing kernels in code often
take $\sigma$. Mixing them mis-sizes the beam by a factor of $\sim$2.4 (Ch. 4, 9).

---

## 6. Worked examples — parsing every symbol

The method: read left to right, name each symbol, note its units, then read the
whole thing as a sentence.

### The radiometer equation

$$
\Delta T = \frac{T_\mathrm{sys}}{\sqrt{n_\mathrm{pol}\,B\,\tau}}
$$

| Symbol | What it is | Units |
|--------|-----------|-------|
| $\Delta T$ | the **noise**: smallest temperature change detectable (the $1\sigma$ sensitivity) | K |
| $T_\mathrm{sys}$ | **system temperature** — total noise power expressed as a temperature | K |
| $n_\mathrm{pol}$ | number of **polarisations** summed (1 or 2) | dimensionless |
| $B$ | **bandwidth** ($\Delta\nu$) over which you integrate | Hz |
| $\tau$ | **integration time** (here $\tau$ is *time*, not optical depth) | s |
| $\sqrt{\;\;}$ | square root — sensitivity improves as the *root* of $B\tau$, not linearly | — |

**Read as:** *"the noise floor equals the system temperature divided by the square
root of (number of polarisations $\times$ bandwidth $\times$ integration time)."*
Doubling your integration time only improves sensitivity by $\sqrt{2}$ — the heart
of "integrating down" (Ch. 3).

### The visibility integral

$$
V(u,v) = \iint I(l,m)\,e^{-2\pi i (ul + vm)}\,dl\,dm
$$

| Symbol | What it is | Notes |
|--------|-----------|-------|
| $V(u,v)$ | the **visibility** — what the interferometer measures | *complex*: amplitude + phase |
| $(u,v)$ | a **baseline** in the Fourier plane, measured in wavelengths | one antenna pair = one $(u,v)$ point |
| $\iint \cdots\, dl\, dm$ | **integrate over the whole sky** | $(l,m)$ = direction cosines |
| $I(l,m)$ | the **sky brightness** in that direction | the thing we want to recover |
| $e^{-2\pi i(\ldots)}$ | the **Fourier kernel** | the $-$ sign and $2\pi$ are the conventions of §5 |
| $i$ | $\sqrt{-1}$ | makes $V$ complex; its phase encodes source *position* |

**Read as:** *"the visibility at baseline $(u,v)$ is the two-dimensional Fourier
transform of the sky brightness."* Each baseline samples one Fourier component;
filling the $uv$-plane (by using many antennas and Earth rotation) and inverting
the transform reconstructs $I(l,m)$ — the whole programme of aperture synthesis
(Ch. 7–9). Note $V^*(-u,-v) = V(u,v)$ because the sky is real, so each baseline
secretly gives you two $uv$ points (the conjugate $*$ of §3 at work).

---

!!! tip "When in doubt"
    Find the paper's **symbol table** or the sentence "where $x$ is…" near the
    first use. Notation is a dialect; this page is a phrasebook, but the author
    always has the final say.
