"""Signals, noise, and the radiometer equation.

These helpers let the early chapters *simulate* what a radio telescope's
back-end actually measures: band-limited noise out of which a faint astronomical
signal slowly emerges as you integrate. Everything here is plain NumPy/SciPy so
the maths stays inspectable.

Key results encoded here
------------------------
* The **radiometer equation**, :math:`\\Delta T = T_\\mathrm{sys}/\\sqrt{B\\,\\tau}`
  (Dicke 1946): the temperature sensitivity improves as the square root of
  bandwidth times integration time.
* **Synthetic spectra** with thermal and non-thermal (power-law) components, so
  spectral-index fitting can be practised on data with a known answer.
* Simple **beam shapes** (Gaussian and Airy) used by the antenna chapter.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import special

__all__ = [
    "radiometer_sensitivity",
    "integrate_noise",
    "RadiometerResult",
    "synthetic_spectrum",
    "power_law",
    "gaussian_beam",
    "airy_beam",
    "rng",
]


def rng(seed: int | None = 0) -> np.random.Generator:
    """Return a seeded NumPy random generator.

    Notebooks call this so results are reproducible across runs and machines.
    Pass ``seed=None`` for a fresh, OS-seeded generator.
    """
    return np.random.default_rng(seed)


def radiometer_sensitivity(
    t_sys: float,
    bandwidth: float,
    integration_time: float,
    n_pol: int = 1,
) -> float:
    """Temperature sensitivity from the radiometer equation.

    :math:`\\Delta T = T_\\mathrm{sys} / \\sqrt{n_\\mathrm{pol}\\,B\\,\\tau}`.

    Parameters
    ----------
    t_sys
        System temperature in kelvin (receiver + sky + spillover ...).
    bandwidth
        Bandwidth :math:`B` in hertz.
    integration_time
        Integration time :math:`\\tau` in seconds.
    n_pol
        Number of polarisations averaged (1 or 2). Averaging both hands of
        polarisation improves sensitivity by :math:`\\sqrt{2}`.

    Returns
    -------
    float
        The :math:`1\\sigma` noise level in kelvin.
    """
    if np.any(np.asarray(bandwidth) <= 0) or np.any(np.asarray(integration_time) <= 0):
        raise ValueError("bandwidth and integration_time must be positive")
    return t_sys / np.sqrt(n_pol * bandwidth * integration_time)


@dataclass
class RadiometerResult:
    """Outcome of a simulated integration (see :func:`integrate_noise`)."""

    times: np.ndarray
    """Cumulative integration time at each sample (s)."""
    estimate: np.ndarray
    """Running estimate of the measured temperature (K)."""
    expected_sigma: np.ndarray
    """Radiometer-equation prediction for the 1-sigma error at each time (K)."""


def integrate_noise(
    t_sys: float,
    bandwidth: float,
    total_time: float,
    signal: float = 0.0,
    n_samples: int = 500,
    seed: int | None = 0,
) -> RadiometerResult:
    """Simulate integrating down noise toward a faint signal.

    Models the radiometer output as a running mean of independent samples whose
    per-sample scatter is set so the ensemble obeys the radiometer equation.
    This is the engine behind the "watch the signal emerge" figure in the
    noise chapter.

    Parameters
    ----------
    t_sys
        System temperature (K).
    bandwidth
        Bandwidth (Hz).
    total_time
        Total integration time to simulate (s).
    signal
        True source antenna temperature to recover (K). Default 0.
    n_samples
        Number of time steps to simulate.
    seed
        Seed for reproducibility.

    Returns
    -------
    RadiometerResult
        Running estimate plus the theoretical error envelope.
    """
    generator = rng(seed)
    times = np.linspace(total_time / n_samples, total_time, n_samples)
    dt = times[0]
    # Per-sample noise consistent with the radiometer equation over one step.
    per_sample_sigma = radiometer_sensitivity(t_sys, bandwidth, dt)
    samples = signal + generator.normal(0.0, per_sample_sigma, size=n_samples)
    # Running mean -> the estimate after integrating up to each time.
    estimate = np.cumsum(samples) / np.arange(1, n_samples + 1)
    expected_sigma = radiometer_sensitivity(t_sys, bandwidth, times)
    return RadiometerResult(times=times, estimate=estimate, expected_sigma=expected_sigma)


def power_law(frequency: np.ndarray, amplitude: float, spectral_index: float,
              reference: float = 1.0) -> np.ndarray:
    """Power-law flux density :math:`S(\\nu) = A (\\nu/\\nu_0)^{\\alpha}`.

    Non-thermal synchrotron sources follow such a power law with a negative
    spectral index (typically :math:`\\alpha \\approx -0.7`).

    Parameters
    ----------
    frequency
        Frequencies (any consistent unit; ``reference`` must match).
    amplitude
        Flux density at the reference frequency.
    spectral_index
        The spectral index :math:`\\alpha`.
    reference
        Reference frequency :math:`\\nu_0`.
    """
    frequency = np.asarray(frequency, dtype=float)
    return amplitude * (frequency / reference) ** spectral_index


def synthetic_spectrum(
    frequency: np.ndarray,
    *,
    thermal_amp: float = 1.0,
    nonthermal_amp: float = 5.0,
    spectral_index: float = -0.7,
    reference: float = 1.0,
    noise: float = 0.05,
    seed: int | None = 0,
) -> np.ndarray:
    """Synthesise a two-component radio spectrum with measurement noise.

    Combines a flat thermal (free--free-like) component with a steep
    non-thermal power law and adds Gaussian noise, giving a realistic target
    for spectral-index fitting where the true answer is known.

    Parameters
    ----------
    frequency
        Frequency grid.
    thermal_amp
        Amplitude of the flat thermal component.
    nonthermal_amp
        Amplitude of the power-law component at ``reference``.
    spectral_index
        Spectral index of the non-thermal component.
    reference
        Reference frequency for the power law.
    noise
        Standard deviation of additive Gaussian noise (same units as flux).
    seed
        Seed for reproducibility.
    """
    frequency = np.asarray(frequency, dtype=float)
    model = thermal_amp + power_law(frequency, nonthermal_amp, spectral_index, reference)
    if noise > 0:
        model = model + rng(seed).normal(0.0, noise, size=frequency.shape)
    return model


def gaussian_beam(theta: np.ndarray, fwhm: float) -> np.ndarray:
    """Normalised Gaussian beam power pattern.

    Parameters
    ----------
    theta
        Angular offset from boresight (same unit as ``fwhm``).
    fwhm
        Full width at half maximum.

    Returns
    -------
    numpy.ndarray
        Power response in [0, 1], peaking at 1 on boresight.
    """
    theta = np.asarray(theta, dtype=float)
    sigma = fwhm / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    return np.exp(-0.5 * (theta / sigma) ** 2)


def airy_beam(theta: np.ndarray, diameter: float, wavelength: float) -> np.ndarray:
    """Normalised Airy power pattern of a uniformly illuminated circular dish.

    The diffraction pattern of a filled circular aperture; its first null sets
    the classic :math:`1.22\\,\\lambda/D` resolution limit.

    Parameters
    ----------
    theta
        Angular offset from boresight, in radians.
    diameter
        Dish diameter (same length unit as ``wavelength``).
    wavelength
        Observing wavelength.

    Returns
    -------
    numpy.ndarray
        Power response in [0, 1].
    """
    theta = np.asarray(theta, dtype=float)
    x = np.pi * diameter / wavelength * np.sin(theta)
    # Limit -> 1 at the origin; handle x == 0 without dividing by zero.
    with np.errstate(invalid="ignore", divide="ignore"):
        amp = np.where(x == 0.0, 1.0, 2.0 * special.j1(x) / x)
    return amp**2
