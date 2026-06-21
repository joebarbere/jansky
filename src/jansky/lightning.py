"""Lightning as a radio source: sferics, tweeks, whistlers, and geolocation.

Every lightning return stroke radiates a broadband electromagnetic impulse. In the
very-low-frequency band (VLF, ~3--30 kHz) that impulse -- a **sferic** -- propagates
for thousands of kilometres in the Earth--ionosphere waveguide, and is the signal that
global lightning-location networks (Blitzortung, WWLLN) trilaterate. Two dispersed
descendants of the sferic are especially instructive:

* a **tweek** is a sferic that has bounced far enough in the waveguide that its
  low-frequency tail piles up near the waveguide cutoff (~1.6--1.8 kHz at night),
  stretching into a brief descending tone;
* a **whistler** is lightning energy that leaked up a geomagnetic field line, dispersed
  in the magnetospheric plasma, and returned with a group delay :math:`t \\propto
  f^{-1/2}` -- the close cousin of the interstellar :math:`t \\propto \\nu^{-2}` sweep
  of a pulsar or fast radio burst (see :mod:`jansky.transients`).

This module provides small, teachable helpers: a synthetic return-stroke field, the
tweek and whistler group-delay laws, a whistler dynamic-spectrum synthesiser and its
de-disperser (the magnetospheric analogue of pulsar de-dispersion), and a
time-of-arrival (TOA) geolocator -- the same multilateration that locates real strokes
and that underlies VLBI geometry (Chapter 19).

References
----------
* Storey, L. R. O. (1953), "An investigation of whistling atmospherics",
  Phil. Trans. R. Soc. Lond. A 246, 113. DOI:10.1098/rsta.1953.0011 -- the founding
  paper of magnetospheric whistler physics.
* Rodger et al. (2006), "Detection efficiency of the VLF World-Wide Lightning Location
  Network (WWLLN)", Ann. Geophys. 24, 3197 -- the academic TOA network.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from astropy import constants as const

__all__ = [
    "C_KM_S",
    "TWEEK_CUTOFF_HZ",
    "return_stroke_field",
    "whistler_group_delay",
    "tweek_group_delay",
    "synthesize_whistler",
    "dedisperse_whistler",
    "simulate_arrival_times",
    "geolocate_toa",
    "GeoFix",
]

#: Speed of light in km/s (from CODATA, via astropy). Sferics travel at very close to
#: this in the waveguide; we use it for the geolocation light-travel times.
C_KM_S: float = float(const.c.to("km/s").value)

#: First-mode (QTM1) cutoff of the night-time Earth--ionosphere waveguide, in Hz. Set
#: by the reflection height via :math:`f_c \\approx c/2h_D`, so 1700 Hz corresponds to
#: :math:`h_D \\approx 88` km (and :math:`h_D \\approx 83` km → ~1.8 kHz); the literature
#: quotes ~1.6--1.8 kHz. Below it, the waveguide does not propagate and a tweek's group
#: delay diverges.
TWEEK_CUTOFF_HZ: float = 1700.0


def return_stroke_field(
    n: int = 2048,
    dt: float = 1.0e-6,
    tau_rise: float = 2.0e-6,
    tau_fall: float = 40.0e-6,
) -> tuple[np.ndarray, np.ndarray]:
    """Synthesise a lightning return-stroke radiated electric field.

    The channel-base current is modelled as a difference of exponentials,
    :math:`I(t) = I_0\\,(e^{-t/\\tau_\\mathrm{fall}} - e^{-t/\\tau_\\mathrm{rise}})`,
    and the far-field radiation is proportional to :math:`\\mathrm{d}I/\\mathrm{d}t`.
    The result is a fast bipolar pulse whose magnitude spectrum is broadband -- flat at
    low frequency and rolling off above ~1/(2πτ_rise) -- the qualitative shape
    measured for real strokes (Serhan et al. 1980).

    Parameters
    ----------
    n
        Number of samples.
    dt
        Sample spacing in seconds (1 µs by default → 1 MHz, ample for a VLF/LF pulse).
    tau_rise, tau_fall
        Current rise and fall time constants in seconds (``tau_rise < tau_fall``).

    Returns
    -------
    (t, field)
        Time axis (s) and the normalised radiated field (peak |field| = 1).
    """
    if tau_rise <= 0 or tau_fall <= tau_rise:
        raise ValueError("require 0 < tau_rise < tau_fall")
    t = np.arange(n) * dt
    # dI/dt of the double-exponential current.
    field = np.exp(-t / tau_rise) / tau_rise - np.exp(-t / tau_fall) / tau_fall
    peak = np.max(np.abs(field))
    if peak > 0:
        field = field / peak
    return t, field


def whistler_group_delay(dispersion: float, freq_hz: np.ndarray | float) -> np.ndarray:
    """Whistler group delay :math:`t(f) = D / \\sqrt{f}`.

    In a cold magnetised plasma below the electron gyro- and plasma frequencies, a
    whistler's group delay scales as :math:`f^{-1/2}`. The single parameter ``D`` (the
    *whistler dispersion*, in :math:`\\mathrm{s\\,Hz^{1/2}}`) is an integral of
    :math:`\\sqrt{n_e}/B` along the field line. Compare
    :func:`jansky.transients.dispersion_delay`, where the interstellar law is
    :math:`t \\propto \\nu^{-2}`.

    Parameters
    ----------
    dispersion
        The whistler dispersion :math:`D` in :math:`\\mathrm{s\\,Hz^{1/2}}` (terrestrial
        one-hop whistlers have ``D`` of order tens).
    freq_hz
        Frequency or array of frequencies in Hz.

    Returns
    -------
    numpy.ndarray
        Group delay in seconds.
    """
    f = np.asarray(freq_hz, dtype=float)
    return dispersion / np.sqrt(f)


def tweek_group_delay(
    freq_hz: np.ndarray | float,
    distance_km: float,
    cutoff_hz: float = TWEEK_CUTOFF_HZ,
) -> np.ndarray:
    """Group delay of a tweek in the Earth--ionosphere waveguide.

    The first waveguide mode has group velocity
    :math:`v_g(f) = c\\,\\sqrt{1 - (f_c/f)^2}`, so the propagation delay over a path of
    length ``distance_km`` is :math:`t(f) = (L/c)\\,/\\sqrt{1 - (f_c/f)^2}`. The delay
    diverges as :math:`f \\to f_c^+`, producing the tweek's descending "hook"; below the
    cutoff the mode does not propagate and the delay is returned as ``nan``.

    Parameters
    ----------
    freq_hz
        Frequency or array of frequencies in Hz.
    distance_km
        Great-circle propagation distance in km.
    cutoff_hz
        Waveguide cutoff frequency in Hz (default :data:`TWEEK_CUTOFF_HZ`).

    Returns
    -------
    numpy.ndarray
        Group delay in seconds; ``nan`` where ``freq_hz <= cutoff_hz``.
    """
    f = np.asarray(freq_hz, dtype=float)
    base = distance_km / C_KM_S
    with np.errstate(invalid="ignore", divide="ignore"):
        factor = np.sqrt(1.0 - (cutoff_hz / f) ** 2)
        delay = np.where(f > cutoff_hz, base / factor, np.nan)
    return delay


def synthesize_whistler(
    freqs_hz: np.ndarray,
    n_time: int,
    dt: float,
    dispersion: float,
    t0: float = 0.05,
    width: float = 6.0e-3,
    amplitude: float = 1.0,
    noise: float = 0.2,
    seed: int | None = 0,
) -> np.ndarray:
    """Build a whistler dynamic spectrum (frequency × time).

    Each frequency channel receives a Gaussian pulse delayed by ``t0`` plus the whistler
    group delay :func:`whistler_group_delay` at that frequency, then white noise is
    added. The resulting ``(n_freq, n_time)`` array shows the characteristic descending
    glide -- the direct analogue of the dispersed pulse built by
    :func:`jansky.transients.disperse_pulse`.

    Parameters
    ----------
    freqs_hz
        Channel frequencies in Hz (e.g. ``np.linspace(300, 10000, 200)``).
    n_time
        Number of time samples.
    dt
        Time-sample spacing in seconds.
    dispersion
        Whistler dispersion :math:`D` in :math:`\\mathrm{s\\,Hz^{1/2}}`.
    t0
        Arrival time of the (infinite-frequency) impulse, in seconds.
    width
        Gaussian pulse width (standard deviation) in seconds.
    amplitude
        Peak pulse amplitude before noise.
    noise
        Standard deviation of additive white noise.
    seed
        Seed for reproducible noise.

    Returns
    -------
    numpy.ndarray
        A ``(n_freq, n_time)`` dynamic spectrum.
    """
    freqs_hz = np.asarray(freqs_hz, dtype=float)
    rng = np.random.default_rng(seed)
    times = np.arange(n_time) * dt
    delays = t0 + whistler_group_delay(dispersion, freqs_hz)
    # (n_freq, n_time) Gaussian centred on each channel's delayed arrival.
    arg = (times[None, :] - delays[:, None]) / width
    dynspec = amplitude * np.exp(-0.5 * arg**2)
    dynspec += rng.normal(0.0, noise, size=dynspec.shape)
    return dynspec


def dedisperse_whistler(
    dynspec: np.ndarray,
    freqs_hz: np.ndarray,
    dt: float,
    dispersion: float,
) -> np.ndarray:
    """De-disperse a whistler dynamic spectrum by removing the :math:`f^{-1/2}` delay.

    Each frequency channel is rolled *earlier* by its whistler group delay so that an
    aligned, broadband impulse stacks vertically. This is the magnetospheric twin of
    pulsar/FRB de-dispersion (:func:`jansky.transients.dedisperse`); summing the returned
    array over frequency recovers the original sferic impulse.

    Parameters
    ----------
    dynspec
        A ``(n_freq, n_time)`` dynamic spectrum.
    freqs_hz
        Channel frequencies in Hz (matching ``dynspec`` rows).
    dt
        Time-sample spacing in seconds.
    dispersion
        The whistler dispersion :math:`D` to remove, in :math:`\\mathrm{s\\,Hz^{1/2}}`.

    Returns
    -------
    numpy.ndarray
        The de-dispersed ``(n_freq, n_time)`` dynamic spectrum.
    """
    dynspec = np.asarray(dynspec, dtype=float)
    freqs_hz = np.asarray(freqs_hz, dtype=float)
    delays = whistler_group_delay(dispersion, freqs_hz)
    shifts = np.round(delays / dt).astype(int)
    out = np.empty_like(dynspec)
    for i in range(dynspec.shape[0]):
        out[i] = np.roll(dynspec[i], -shifts[i])
    return out


def simulate_arrival_times(
    source_xy: tuple[float, float],
    stations_xy: np.ndarray,
    t0: float = 0.0,
    noise_us: float = 1.0,
    seed: int | None = 0,
) -> np.ndarray:
    """Simulate sferic arrival times at a set of stations (for the TOA demo).

    The arrival time at station :math:`i` is the emission time ``t0`` plus the
    light-travel time over the plane distance from the source, with Gaussian timing
    jitter of ``noise_us`` microseconds.

    Parameters
    ----------
    source_xy
        True stroke location ``(x, y)`` in km.
    stations_xy
        ``(n_station, 2)`` array of station positions in km.
    t0
        Emission time in seconds.
    noise_us
        Timing-noise standard deviation in microseconds.
    seed
        Seed for reproducibility.

    Returns
    -------
    numpy.ndarray
        Arrival times (s), one per station.
    """
    stations_xy = np.asarray(stations_xy, dtype=float)
    rng = np.random.default_rng(seed)
    src = np.asarray(source_xy, dtype=float)
    dist = np.linalg.norm(stations_xy - src, axis=1)
    times = t0 + dist / C_KM_S
    times += rng.normal(0.0, noise_us * 1e-6, size=times.shape)
    return times


@dataclass
class GeoFix:
    """Result of a time-of-arrival geolocation (see :func:`geolocate_toa`)."""

    x: float  #: recovered source x (km)
    y: float  #: recovered source y (km)
    t0: float  #: recovered emission time (s)
    residual_rms_us: float  #: RMS of the timing residuals (microseconds)


def geolocate_toa(
    stations_xy: np.ndarray,
    arrival_times: np.ndarray,
    guess: tuple[float, float] | None = None,
) -> GeoFix:
    """Locate a stroke from station arrival times by least-squares multilateration.

    Solves for the source position :math:`(x, y)` and emission time :math:`t_0` that
    best reproduce the measured arrival times, minimising
    :math:`\\sum_i \\big[(|\\mathbf{s}-\\mathbf{r}_i|/c + t_0) - t_i\\big]^2`. At least
    three stations are required (three unknowns); more over-determine the fit and average
    down the timing noise. This is the same hyperbolic geometry used by VLBI
    (Chapter 19) and by real lightning networks.

    Parameters
    ----------
    stations_xy
        ``(n_station, 2)`` array of station positions in km.
    arrival_times
        Measured arrival times (s), one per station.
    guess
        Optional ``(x, y)`` starting point in km; defaults to the station centroid.

    Returns
    -------
    GeoFix
        The recovered position, emission time, and residual RMS.
    """
    from scipy.optimize import least_squares

    stations_xy = np.asarray(stations_xy, dtype=float)
    arrival_times = np.asarray(arrival_times, dtype=float)
    if stations_xy.shape[0] < 3:
        raise ValueError("need at least 3 stations to solve for (x, y, t0)")

    if guess is None:
        cx, cy = stations_xy.mean(axis=0)
    else:
        cx, cy = guess
    t0_guess = float(arrival_times.min())

    def residuals(p: np.ndarray) -> np.ndarray:
        x, y, t0 = p
        dist = np.hypot(stations_xy[:, 0] - x, stations_xy[:, 1] - y)
        return (dist / C_KM_S + t0) - arrival_times

    sol = least_squares(residuals, x0=np.array([cx, cy, t0_guess]))
    res = residuals(sol.x)
    rms_us = float(np.sqrt(np.mean(res**2)) * 1e6)
    return GeoFix(x=float(sol.x[0]), y=float(sol.x[1]), t0=float(sol.x[2]), residual_rms_us=rms_us)
