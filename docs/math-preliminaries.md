# Mathematical Preliminaries

Radio astronomy is one of the most welcoming corners of astrophysics for a
programmer: the data are signals, the maths is Fourier transforms, and the tools
are open source. But "the maths is Fourier transforms" only sounds friendly once
the Fourier transform feels friendly — and a lot of us last met it in a hurry,
years ago, in a lecture theatre.

This page is a **get-up-to-speed reference**: the mathematical background the
course assumes, explained for a numerate programmer who may be rusty on the
physics maths. It does not try to be rigorous; it tries to give you working
intuition, the handful of formulas you will actually meet, and a sense of *why
each one shows up* when we point a dish at the sky. Where it's natural, there's a
tiny NumPy snippet so the idea is something you can run, not just read.

Two sibling pages live next to this one and do different jobs — keep them open:

- [Notation](notation.md) — decodes the *symbols* ($\nu$, $S_\nu$, $u$, $v$,
  $T_\mathrm{sys}$, …). When you hit a glyph you don't recognise, look there.
- [Glossary](glossary.md) — defines the *words* (visibility, baseline, brightness
  temperature, …).

Here we **teach the maths**. The other two just decode. If you already know this
material cold, skip to [Chapter 1](notebooks/01_what_is_radio_astronomy.ipynb) and
come back when something bites.

---

## 1. Complex numbers & phasors

A complex number $z = a + b\,i$ (with $i^2 = -1$) is really just a 2-D vector
with a multiplication rule. The reason it pervades radio astronomy is that radio
*is* oscillation, and complex numbers are the natural bookkeeping for oscillations.

### Euler's formula and the phasor

The single most useful identity in the whole course:

$$
e^{i\theta} = \cos\theta + i\sin\theta .
$$

This says: as $\theta$ runs from $0$ to $2\pi$, the point $e^{i\theta}$ walks once
around the unit circle. A sinusoidal signal $\cos(2\pi f t + \phi)$ can therefore
be written as the real part of a rotating arrow — a **phasor**:

$$
A\cos(2\pi f t + \phi) = \operatorname{Re}\!\left[A\,e^{i\phi}\,e^{i 2\pi f t}\right].
$$

The complex amplitude $A\,e^{i\phi}$ packs the two things you care about into one
number:

- the **amplitude** $|z| = A = \sqrt{a^2 + b^2}$ — how strong the wave is, and
- the **phase** $\arg z = \phi = \operatorname{atan2}(b, a)$ — *where in its cycle*
  the wave is.

Adding two waves of the same frequency becomes adding two arrows; their
constructive/destructive interference is just vector addition. That is the entire
physical content of an interferometer in one sentence.

```python
import numpy as np

z = 3 + 4j
amplitude = np.abs(z)            # 5.0
phase = np.angle(z)              # radians, atan2(4, 3)
print(amplitude, np.degrees(phase))
```

### Why visibilities are complex

When two antennas observe the same source, the signal arrives at one slightly
*later* than the other because of the extra path length. A time delay is a phase
shift, and the natural way to record "amplitude *and* phase of the correlated
signal" is a complex number. That complex number is the **visibility** $V$. Its
magnitude tells you how much coherent power the two antennas share; its phase
encodes *where on the sky* the emission sits relative to the baseline. You'll see
visibilities born in [Chapter 7](notebooks/07_why_interferometry.ipynb) and used
throughout Part III; in code they are exactly the complex output of an FFT (see
`grid_visibilities` and `dirty_image` in `jansky.interferometry`).

---

## 2. The Fourier transform

If you remember one thing: **the Fourier transform re-expresses a signal as a sum
of sinusoids**, telling you *how much of each frequency* it contains. A spike in
time is broad in frequency; a pure tone is a spike in frequency. Radio astronomy
lives in this duality.

### Forward and inverse

For a function of time $g(t)$ the (angular-free, "ordinary frequency") convention
the course uses is

$$
G(f) = \int_{-\infty}^{\infty} g(t)\, e^{-i 2\pi f t}\, \mathrm{d}t,
\qquad
g(t) = \int_{-\infty}^{\infty} G(f)\, e^{+i 2\pi f t}\, \mathrm{d}f .
$$

Note the two conventions worth pinning down, because they bite people:

- **Sign:** the forward transform carries $e^{-i 2\pi f t}$ (minus), the inverse
  carries $e^{+i 2\pi f t}$ (plus). Other texts swap them — always check.
- **The $2\pi$:** putting $2\pi$ inside the exponent (so the variable is ordinary
  frequency $f$ in Hz, not angular frequency $\omega = 2\pi f$) keeps the forward
  and inverse transforms symmetric, with no stray $1/2\pi$ out front. This is the
  convention NumPy implements.

### Time/frequency and *spatial* frequency

The same maths applies to space. If $g(x)$ is a pattern across an aperture, its
transform $G(s)$ is a function of **spatial frequency** $s$ — cycles per metre
(or per radian on the sky). High spatial frequency means fine detail; low spatial
frequency means broad, smooth structure. An interferometer's $(u, v)$ coordinates
*are* spatial frequencies, measured in wavelengths. Long baselines sample high
$(u,v)$ and so resolve fine structure; short baselines sample low $(u,v)$ and see
the smooth, extended emission. That trade is the heart of
[Chapter 8](notebooks/08_aperture_synthesis.ipynb).

### Van Cittert–Zernike: visibilities are the FT of the sky

The cornerstone theorem of interferometry says, to a good approximation for a
small patch of sky, that the **visibility measured on a baseline $(u, v)$ is the
Fourier transform of the sky brightness $I(l, m)$**:

$$
V(u, v) = \iint I(l, m)\, e^{-i 2\pi (u l + v m)}\, \mathrm{d}l\, \mathrm{d}m .
$$

Here $(l, m)$ are direction cosines — coordinates on the patch of sky. Read it as:
*each baseline measures one Fourier component of the sky.* Collect enough of them
and you can inverse-transform back to an image. This is literally what
`dirty_image` in `jansky.interferometry` does. See
[Chapter 8](notebooks/08_aperture_synthesis.ipynb).

### How NumPy's FFT maps to the integrals

The **Discrete Fourier Transform** is the sampled version of the integrals above.
NumPy's `np.fft.fft` computes

$$
G_k = \sum_{n=0}^{N-1} g_n\, e^{-i 2\pi k n / N},
$$

which matches the **minus sign** in our forward transform — good. Two practical
gotchas:

- **Normalisation.** `fft` puts no factor out front; `ifft` divides by $N$. So
  `ifft(fft(x)) == x`, but if you want physically scaled amplitudes you may need to
  multiply/divide by $N$ or the sample spacing yourself.
- **Frequency ordering.** `fft` returns frequencies as
  $[0, +, +, \dots, -, \dots]$: the zero frequency first, then positives, then the
  negatives wrapped around to the end. `np.fft.fftfreq` gives you the matching
  frequency axis.

### `fftshift` — put DC in the middle

Because of that wrap-around ordering, the natural place for "zero frequency" (the
image centre, in 2-D) is the *corner* of the array, not the middle. `fftshift`
rotates the array so DC sits in the centre, which is how you actually want to
*look* at a spectrum or an image; `ifftshift` undoes it. You'll see the
shift/transform/inverse-shift sandwich all over `jansky.interferometry`:

```python
import numpy as np

# A clean tone at 50 Hz, sampled at 1 kHz.
fs, n = 1000, 1024
t = np.arange(n) / fs
x = np.sin(2 * np.pi * 50 * t)

X = np.fft.fftshift(np.fft.fft(x))          # DC moved to centre
freq = np.fft.fftshift(np.fft.fftfreq(n, d=1/fs))
peak = freq[np.argmax(np.abs(X))]           # ~ +/- 50 Hz
```

---

## 3. Convolution & the convolution theorem

**Convolution** blurs one function with another. Formally,

$$
(f \ast h)(x) = \int_{-\infty}^{\infty} f(\tau)\, h(x - \tau)\, \mathrm{d}\tau .
$$

Intuitively: slide a copy of $h$ across $f$, and at each position record the
overlap. If $h$ is a little blob, $f \ast h$ is $f$ smeared by that blob.

### The convolution theorem

Convolution in one domain is plain multiplication in the other:

$$
\mathcal{F}\{f \ast h\} = \mathcal{F}\{f\}\cdot \mathcal{F}\{h\}.
$$

This is *the* reason the Fourier transform is so powerful operationally: an
expensive smearing operation becomes a cheap elementwise product after an FFT.

### "Dirty image = sky ⊛ dirty beam"

An interferometer never samples *all* spatial frequencies — only the $(u,v)$ points
its baselines reach. Multiplying the true sky's visibilities by that sampling mask
(a product in the Fourier plane) is, by the convolution theorem, the same as
**convolving the true sky with the transform of the sampling pattern** in the image
plane. That transform is the **dirty beam**, also called the **point spread
function (PSF)** — the smear that a single point source picks up:

$$
I_\text{dirty} = I_\text{true} \ast B_\text{dirty}.
$$

This is exactly the relationship `dirty_image` and `dirty_beam` encode. Because the
sampling has holes, the dirty beam has ugly sidelobes, and undoing that convolution
is **deconvolution** — the job of CLEAN in
[Chapter 9](notebooks/09_deconvolution_clean.ipynb).

```python
import numpy as np

sky = np.zeros(64); sky[20] = 1.0; sky[40] = 0.6   # two point sources
beam = np.exp(-0.5 * ((np.arange(64) - 32) / 2.0) ** 2)
dirty = np.convolve(sky, beam, mode="same")        # each spike smeared by the beam
```

---

## 4. Sampling & the Nyquist–Shannon theorem

To put a continuous signal in a computer you **sample** it: read its value every
$\Delta t$ seconds, i.e. at sample rate $f_s = 1/\Delta t$. The question is whether
those samples capture the signal faithfully.

The **Nyquist–Shannon sampling theorem** answers it: a signal that contains no
frequencies above $f_\text{max}$ (it is **band-limited**) is *fully* determined by
samples taken at

$$
f_s > 2\, f_\text{max}.
$$

The threshold $2 f_\text{max}$ is the **Nyquist rate**; $f_s/2$ is the **Nyquist
frequency**.

### Aliasing

Sample too slowly and frequencies above $f_s/2$ don't just disappear — they **fold
back** and masquerade as lower frequencies. That's **aliasing** (the wagon-wheel
effect in film). A 700 Hz tone sampled at 1000 Hz is indistinguishable from a
300 Hz tone. In practice you put an **anti-aliasing filter** before the sampler to
kill anything above Nyquist, and an SDR's choice of sample rate sets the bandwidth
you can see at once. This is the practical backdrop to
[Chapter 5](notebooks/05_sdr_basics.ipynb) and the band-limited-noise simulations
behind [Chapter 3](notebooks/03_signals_noise_radiometer.ipynb).

```python
import numpy as np

fs = 1000
t = np.arange(0, 1, 1/fs)
real = np.sin(2 * np.pi * 700 * t)     # 700 Hz, above Nyquist (500 Hz)
alias = np.sin(2 * np.pi * 300 * t)    # its alias
print(np.allclose(real, -alias))       # True: 700 Hz folds onto -300 Hz
```

---

## 5. Probability & statistics for noise

A radio telescope mostly measures **noise**. The signal you want is often far below
it, and the whole art of detection is *statistical*. A little probability goes a
long way here.

### Gaussian noise and its three numbers

Thermal noise is, to excellent approximation, **Gaussian** (normally distributed).
A Gaussian is described by just two numbers:

$$
p(x) = \frac{1}{\sigma\sqrt{2\pi}}\,
\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right],
$$

- the **mean** $\mu$ — where it's centred (the true signal level), and
- the **variance** $\sigma^2$, or its square root the **standard deviation**
  $\sigma$ — how wide the scatter is.

For data, $\mu \approx \frac1N\sum x_i$ and $\sigma^2 \approx \frac1N\sum (x_i-\mu)^2$.
The standard deviation is the natural unit of "how big is the noise", so a
detection is often quoted as a number of $\sigma$ ("a $5\sigma$ source").

### The central limit theorem and why averaging wins

The **central limit theorem** says that the mean of $N$ independent samples tends
toward a Gaussian — *regardless* of the samples' own distribution — and, crucially,
its standard deviation shrinks:

$$
\sigma_{\text{mean of }N} = \frac{\sigma}{\sqrt{N}}.
$$

That $1/\sqrt{N}$ is the single most important fact about radio sensitivity. Average
four times as long and you halve the noise; to improve by $10\times$ you must
integrate $100\times$ longer. This is precisely why `integrate_noise` in
`jansky.signals` lets a faint signal "emerge" from the noise as the running mean
tightens.

### The radiometer equation

Apply $1/\sqrt{N}$ to a receiver. The number of independent samples in an
integration of time $\tau$ over bandwidth $B$ is $\sim B\tau$, so the temperature
uncertainty is

$$
\Delta T = \frac{T_\mathrm{sys}}{\sqrt{B\,\tau}}.
$$

This is the **radiometer equation** (Dicke 1946). It says sensitivity improves as
the square root of *bandwidth times time* — wider band and longer stares both help.
It is implemented as `radiometer_sensitivity` and is the spine of
[Chapter 3](notebooks/03_signals_noise_radiometer.ipynb).

### Signal-to-noise ratio

The **signal-to-noise ratio** is just

$$
\mathrm{SNR} = \frac{\text{signal}}{\sigma_\text{noise}}.
$$

Everything above is a campaign to push this number up: more bandwidth, longer
integration, averaging polarisations, combining antennas.

### Least-squares fitting

When you fit a model to noisy data — say a power law to a measured spectrum — the
standard recipe is **least squares**: choose parameters that minimise the sum of
squared residuals,

$$
\chi^2 = \sum_i \frac{\big(y_i - \text{model}(x_i)\big)^2}{\sigma_i^2}.
$$

Under Gaussian noise this is the maximum-likelihood estimate, which is why it's
ubiquitous. You'll fit a spectral index this way in
[Chapter 2](notebooks/02_physics_of_radio_emission.ipynb), against synthetic data
from `synthetic_spectrum` whose true answer you know.

```python
import numpy as np

rng = np.random.default_rng(0)
x = np.linspace(0, 10, 200)
y = 2.0 * x + 1.0 + rng.normal(0, 1.0, x.size)   # noisy line
slope, intercept = np.polyfit(x, y, 1)           # least-squares fit
```

---

## 6. Logarithms & decibels

Radio quantities span enormous ranges — the faintest source and a satellite
downlink can differ by twelve orders of magnitude. **Logarithms** compress that
range into something you can plot and reason about. Recall $\log(ab)=\log a+\log b$:
multiplication becomes addition, and a power law $y = x^{\alpha}$ becomes a
*straight line* of slope $\alpha$ in $\log$–$\log$ axes.

### Decibels

Engineers express *ratios* of power in **decibels**:

$$
\text{dB} = 10\,\log_{10}\!\frac{P}{P_\text{ref}}.
$$

So $\times 10$ in power is $+10$ dB, $\times 2$ is $\approx +3$ dB, and gains/losses
along a signal chain simply *add* in dB. (For amplitude rather than power the factor
is $20\log_{10}$, because power goes as amplitude squared.) Receiver gains, noise
figures and dynamic ranges in [Chapter 4](notebooks/04_antennas_and_receivers.ipynb)
are all quoted in dB.

### Magnitudes (the astronomer's log)

Optical astronomy's **magnitude** scale is also logarithmic — and backwards
(brighter = smaller number, a leftover from antiquity): $m = -2.5\log_{10} F +
\text{const}$. You'll meet it when you cross-match radio sources against optical
catalogues in [Chapter 14](notebooks/14_multiwavelength.ipynb).

### Why spectra are log-log

Because synchrotron and free–free emission follow power laws in frequency, plotting
flux density against frequency on **log–log axes** turns those curves into straight
lines whose *slopes* are the spectral indices you're after. Reading a slope off a
log–log plot is reading off physics.

```python
import numpy as np

nu = np.logspace(8, 10, 50)           # 0.1 to 10 GHz
flux = 5.0 * (nu / 1e9) ** -0.7       # power law, alpha = -0.7
slope = np.polyfit(np.log10(nu), np.log10(flux), 1)[0]   # ~ -0.7
```

---

## 7. Coordinates & spherical trigonometry

The sky is a sphere, so positions are **angles**, and angular maths is where a lot
of bookkeeping lives.

### Angles and the small-angle approximation

Use **radians** for maths ($2\pi$ rad = 360°). Astronomers also use fine units:
1° = 60 **arcminutes** (′), 1′ = 60 **arcseconds** (″). For the tiny angles typical
in astronomy, the **small-angle approximation** is your friend: for $\theta$ in
radians and $\theta \ll 1$,

$$
\sin\theta \approx \theta, \qquad \tan\theta \approx \theta, \qquad
\cos\theta \approx 1 - \tfrac12\theta^2 .
$$

This is why a source's physical size and its angular size relate by the simple
$\text{size} \approx \theta \times \text{distance}$, and why the diffraction limit
$\theta \approx 1.22\,\lambda/D$ (next section) can be written as a clean
proportion.

### Celestial coordinates

Two coordinate systems matter:

- **Equatorial — Right Ascension (RA, $\alpha$) and Declination (Dec, $\delta$).**
  Fixed to the stars. Dec is "celestial latitude" ($-90°$ to $+90°$); RA is
  "celestial longitude", usually measured in *hours* (24 h = 360°). A source's RA/Dec
  don't change as the Earth turns.
- **Horizontal — Altitude (alt) and Azimuth (az).** Where the dish actually points:
  height above the horizon and compass bearing. These *do* change minute to minute.

The bridge between them is the **hour angle** $H$ — how far west of the meridian a
source has rotated, essentially local sidereal time minus RA. Hour angle is what
drives **Earth-rotation synthesis**: as $H$ sweeps, a fixed pair of antennas traces
an arc through the $(u,v)$ plane, which is exactly the `hour_angles` loop in
`uv_coverage`. See [Chapter 8](notebooks/08_aperture_synthesis.ipynb).

Converting between these frames is **spherical trigonometry** — the law of cosines
on a sphere. In practice you let `astropy.coordinates` do it (see
[Chapter 10](notebooks/10_open_archives.ipynb)); the point is to know *which* frame
a number lives in.

### Solid angle and the steradian

A patch of sky subtends a **solid angle** — area on the unit sphere, measured in
**steradians (sr)**. The whole sky is $4\pi$ sr. For a small beam of angular radius
$\theta$, the solid angle is approximately $\Omega \approx \pi\theta^2$ (the
small-angle area of a disc). Solid angle is how a telescope beam's "size" enters
brightness: flux density is brightness integrated over solid angle, $S =
\int I\,\mathrm{d}\Omega$. This relationship underpins brightness temperature in
[Chapter 1](notebooks/01_what_is_radio_astronomy.ipynb) and the beam patterns in
[Chapter 4](notebooks/04_antennas_and_receivers.ipynb).

---

## 8. A few special functions

A handful of named functions recur so often it's worth recognising them on sight.

### The sinc function

$$
\operatorname{sinc}(x) = \frac{\sin(\pi x)}{\pi x},
\qquad \operatorname{sinc}(0) = 1 .
$$

It's the Fourier transform of a rectangular ("box") function — so it appears
whenever something is sharply truncated: a finite observation in time gives a sinc
in frequency, a finite (1-D) aperture gives a sinc beam on the sky. Its oscillating
sidelobes are the mathematical ancestor of the sidelobes that make deconvolution
necessary. NumPy's `np.sinc` uses exactly this $\pi$-normalised definition.

### The Gaussian

$$
g(x) = \exp\!\left[-\frac{x^2}{2\sigma^2}\right].
$$

Special for two reasons: the Fourier transform of a Gaussian is again a Gaussian
(no sidelobes), and the central limit theorem makes it the universal shape of noise.
Telescope beams are routinely *modelled* as Gaussians, with width quoted as the
**full width at half maximum (FWHM)**, related to $\sigma$ by
$\text{FWHM} = 2\sqrt{2\ln 2}\,\sigma \approx 2.355\,\sigma$. That exact conversion
is the line in `gaussian_beam` in `jansky.signals`.

### The Airy pattern and Bessel $J_1$ (diffraction)

A uniformly illuminated *circular* dish doesn't produce a sinc beam — it produces
the **Airy pattern**, built from the first-order **Bessel function** $J_1$:

$$
P(\theta) = \left[\frac{2 J_1(x)}{x}\right]^2,
\qquad x = \frac{\pi D}{\lambda}\sin\theta .
$$

Its first null sets the famous diffraction-limited resolution

$$
\theta_\text{res} \approx 1.22\,\frac{\lambda}{D},
$$

bigger wavelength or smaller dish ⇒ blurrier view — the reason radio dishes are
huge. This is `airy_beam` in `jansky.signals`, used in
[Chapter 4](notebooks/04_antennas_and_receivers.ipynb).

### The power law

$$
S(\nu) = A\left(\frac{\nu}{\nu_0}\right)^{\alpha}.
$$

The workhorse spectral shape. The exponent $\alpha$ is the **spectral index**;
synchrotron sources have steep negative indices ($\alpha \approx -0.7$), thermal
sources are flatter. On log–log axes (§6) it's a straight line of slope $\alpha$.
This is `power_law` in `jansky.signals`, fitted in
[Chapter 2](notebooks/02_physics_of_radio_emission.ipynb).

```python
import numpy as np
from scipy import special

x = np.linspace(-10, 10, 400)
sinc = np.sinc(x)                              # sin(pi x)/(pi x)
airy = np.where(x == 0, 1.0, 2 * special.j1(x) / x) ** 2
```

---

## 9. Vectors & linear algebra essentials

You need only a little linear algebra, but you need it often.

### Dot products

For vectors $\mathbf{a}$ and $\mathbf{b}$,

$$
\mathbf{a}\cdot\mathbf{b} = \sum_i a_i b_i = |\mathbf{a}|\,|\mathbf{b}|\cos\theta .
$$

It measures alignment, and it's how a path-length delay is computed: the extra
distance a wavefront travels to one antenna is the **baseline vector dotted with the
direction to the source**. That dot product becomes the visibility phase of §1.

### Matrices for rotation

A matrix is a linear map; the ones you'll meet most are **rotations**. In 2-D,

$$
R(\theta) =
\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix},
$$

and $R(\theta)\,\mathbf{x}$ turns the vector $\mathbf{x}$ by $\theta$. Coordinate
transforms — baseline to $(u,v)$, equatorial to horizontal — are products of such
rotation matrices. The $(u,v)$ projection in `uv_coverage` is exactly a rotation by
the hour angle followed by a $\sin(\text{Dec})$ squash of the $v$ axis. Stacking
many points and rotating them all at once is just one matrix multiply — which is why
NumPy makes this fast.

```python
import numpy as np

def rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])

pts = np.array([[1, 0], [0, 1], [1, 1]]).T     # column vectors
turned = rot(np.pi / 2) @ pts                   # rotate 90 degrees
```

That's the toolkit. None of it is deep on its own; the magic is how a few of these
ideas — a complex phasor, a Fourier transform, the $1/\sqrt{N}$ of averaging — stack
up into a telescope. Onward to [Chapter 1](notebooks/01_what_is_radio_astronomy.ipynb).
