"""Cosmic dawn & the Epoch of Reionization: the redshifted 21 cm signal.

The same hydrogen 21 cm line taught in :mod:`jansky` Chapter 6, observed from neutral
gas at high redshift, is the most promising probe of the first stars and reionization.
Redshift maps it down to low frequencies (:func:`redshift_to_freq`): the cosmic-dawn
absorption trough sits near 78 MHz (z ~ 17) and reionization finishes near 200 MHz
(z ~ 6).

This module provides small, teachable helpers: the frequency/redshift mapping, the CMB
temperature, the differential brightness temperature :math:`\\delta T_b` (whose sign is
set by the spin temperature relative to the CMB), a phenomenological flattened-Gaussian
global-signal trough (the form fit by EDGES and others), and a smooth-foreground
polynomial subtraction -- the core data-analysis idea, since Galactic synchrotron
foregrounds are ~10^4--10^5 brighter than the signal but spectrally smooth.

References
----------
* Furlanetto, Oh & Briggs (2006), "Cosmology at low frequencies", Phys. Rep. 433, 181 --
  the standard review; the :math:`\\delta T_b` prefactor used here is their eq. 1.
* Pritchard & Loeb (2012), Rep. Prog. Phys. 75, 086901 -- the modern review.
* Bowman et al. (2018), Nature 555, 67 -- the claimed (and contested) EDGES absorption
  profile fit with a flattened Gaussian.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "NU_21_MHZ",
    "T_CMB0_K",
    "redshift_to_freq",
    "freq_to_redshift",
    "cmb_temperature",
    "differential_brightness",
    "global_signal",
    "remove_smooth_foreground",
]

#: Rest frequency of the HI 21 cm hyperfine line, in MHz (the same line as Chapter 6).
NU_21_MHZ: float = 1420.405751768

#: CMB temperature today, in K (FIRAS; the same value used in Chapter 22).
T_CMB0_K: float = 2.725


def redshift_to_freq(z: np.ndarray | float) -> np.ndarray:
    """Observed frequency (MHz) of the 21 cm line emitted at redshift ``z``."""
    return NU_21_MHZ / (1.0 + np.asarray(z, dtype=float))


def freq_to_redshift(nu_mhz: np.ndarray | float) -> np.ndarray:
    """Redshift of 21 cm emission observed at frequency ``nu_mhz`` (MHz)."""
    return NU_21_MHZ / np.asarray(nu_mhz, dtype=float) - 1.0


def cmb_temperature(z: np.ndarray | float, t0: float = T_CMB0_K) -> np.ndarray:
    """CMB temperature (K) at redshift ``z``: :math:`T_\\mathrm{CMB}(z) = T_0 (1+z)`."""
    return t0 * (1.0 + np.asarray(z, dtype=float))


def differential_brightness(
    z: np.ndarray | float,
    spin_temp_k: np.ndarray | float,
    x_hi: np.ndarray | float = 1.0,
    delta_b: np.ndarray | float = 0.0,
    omega_b_h2: float = 0.0223,
    omega_m_h2: float = 0.143,
    t0: float = T_CMB0_K,
) -> np.ndarray:
    """Differential 21 cm brightness temperature :math:`\\delta T_b` (mK).

    The sky signal is the contrast of neutral hydrogen against the CMB
    (Furlanetto, Oh & Briggs 2006, eq. 1):

    .. math::

        \\delta T_b \\approx 27\\, x_\\mathrm{HI}\\,(1+\\delta_b)
        \\left(1 - \\frac{T_\\mathrm{CMB}}{T_S}\\right)
        \\sqrt{\\frac{1+z}{10}}\\,
        \\frac{\\Omega_b h^2}{0.023}\\,
        \\sqrt{\\frac{0.15}{\\Omega_m h^2}}\\ \\mathrm{mK}.

    The sign is set by the spin temperature :math:`T_S`: ``T_S < T_CMB`` gives
    **absorption** (negative), ``T_S > T_CMB`` **emission** (positive), and
    ``T_S = T_CMB`` no signal. (Density fluctuations and redshift-space distortions are
    dropped -- this is the global / first-order form.)

    Parameters
    ----------
    z
        Redshift.
    spin_temp_k
        Spin temperature :math:`T_S` in K.
    x_hi
        Neutral hydrogen fraction (1 = fully neutral, 0 = fully ionized).
    delta_b
        Baryon overdensity (0 on average).
    omega_b_h2, omega_m_h2
        Baryon and matter physical density parameters.
    t0
        CMB temperature today, in K.

    Returns
    -------
    numpy.ndarray
        :math:`\\delta T_b` in mK.
    """
    z = np.asarray(z, dtype=float)
    t_cmb = cmb_temperature(z, t0)
    prefactor = 27.0 * (omega_b_h2 / 0.023) * np.sqrt(0.15 / omega_m_h2)
    return (
        prefactor
        * np.asarray(x_hi, dtype=float)
        * (1.0 + np.asarray(delta_b, dtype=float))
        * (1.0 - t_cmb / np.asarray(spin_temp_k, dtype=float))
        * np.sqrt((1.0 + z) / 10.0)
    )


def global_signal(
    nu_mhz: np.ndarray,
    center_mhz: float = 78.0,
    depth_mk: float = -200.0,
    width_mhz: float = 19.0,
    flatness: float = 1.0,
) -> np.ndarray:
    """A phenomenological flattened-Gaussian global 21 cm absorption trough (mK).

    A generalised ("super") Gaussian,
    :math:`\\delta T_b(\\nu) = A\\,\\exp\\!\\big[-\\tfrac12 |(\\nu-\\nu_0)/\\sigma|^{2p}\\big]`,
    where ``flatness`` :math:`p \\ge 1` flattens the bottom of the trough (``p = 1`` is a
    plain Gaussian; larger ``p`` approaches the flat-bottomed profile EDGES reported).
    A teaching stand-in for a physical global-signal model such as 21cmFAST.

    Parameters
    ----------
    nu_mhz
        Frequency axis in MHz.
    center_mhz
        Trough centre frequency (78 MHz ~ z 17 for the cosmic-dawn trough).
    depth_mk
        Trough amplitude in mK (negative for absorption; ~ -200 in standard ΛCDM,
        ~ -500 for the contested EDGES fit).
    width_mhz
        Characteristic half-width :math:`\\sigma` in MHz.
    flatness
        Super-Gaussian exponent :math:`p \\ge 1`.

    Returns
    -------
    numpy.ndarray
        The global signal in mK on the ``nu_mhz`` grid.
    """
    nu = np.asarray(nu_mhz, dtype=float)
    arg = np.abs((nu - center_mhz) / width_mhz) ** (2.0 * flatness)
    return depth_mk * np.exp(-0.5 * arg)


def remove_smooth_foreground(
    nu_mhz: np.ndarray,
    temps_k: np.ndarray,
    degree: int = 5,
) -> tuple[np.ndarray, np.ndarray]:
    """Subtract a spectrally smooth foreground by a log--log polynomial fit.

    Galactic synchrotron foregrounds are ~10^4--10^5 brighter than the 21 cm signal but
    follow a smooth power law, so a low-order polynomial in :math:`\\log_{10}\\nu` versus
    :math:`\\log_{10}T` absorbs almost all of the foreground while leaving spectrally
    *structured* signal (and noise) in the residual. This is the core of every
    global-signal experiment (EDGES uses a degree-5 polynomial); the same low-order
    smooth-baseline removal idea appears in :mod:`jansky.rfi` and :mod:`jansky.vlf`.

    Parameters
    ----------
    nu_mhz
        Frequency axis in MHz (all positive).
    temps_k
        Measured antenna/brightness temperature spectrum in K (all positive).
    degree
        Polynomial degree of the log--log foreground model.

    Returns
    -------
    (residual_k, foreground_k)
        The residual (data minus smooth model) and the fitted smooth foreground, both in K.
    """
    nu = np.asarray(nu_mhz, dtype=float)
    temps = np.asarray(temps_k, dtype=float)
    if np.any(nu <= 0) or np.any(temps <= 0):
        raise ValueError("remove_smooth_foreground needs positive frequencies and temperatures")
    log_nu = np.log10(nu)
    coeffs = np.polyfit(log_nu, np.log10(temps), deg=degree)
    foreground = 10.0 ** np.polyval(coeffs, log_nu)
    return temps - foreground, foreground
