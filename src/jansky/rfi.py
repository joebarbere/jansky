"""Radio-frequency interference (RFI): robust statistics and flagging.

Real radio data is riddled with terrestrial interference -- phones, Wi-Fi, radar,
satellites, switching supplies. Before you can trust an average you have to
*flag* the corrupted samples. Two workhorse tools: **robust statistics** (the
median and the median-absolute-deviation, which interference can't drag around
like the mean and standard deviation can) and the **spectral kurtosis** estimator
(which spots signals that are too steady -- or too spiky -- to be natural noise).
This module provides both, behind the RFI Maths Lab.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "mad_sigma",
    "flag_outliers",
    "spectral_kurtosis",
    "flag_by_kurtosis",
]


def mad_sigma(x: np.ndarray, axis: int | None = None) -> float | np.ndarray:
    """Robust standard-deviation estimate from the median absolute deviation.

    :math:`\\sigma \\approx 1.4826 \\times \\mathrm{median}(|x - \\mathrm{median}(x)|)`,
    the constant making it consistent with the std for Gaussian data. Unlike the
    plain std, a few strong RFI samples barely move it.
    """
    x = np.asarray(x, dtype=float)
    med = np.median(x, axis=axis, keepdims=True)
    mad = np.median(np.abs(x - med), axis=axis, keepdims=True)
    sigma = 1.4826 * mad
    if axis is None:
        return float(np.asarray(sigma).reshape(-1)[0])
    return np.squeeze(sigma, axis=axis)


def flag_outliers(data: np.ndarray, threshold: float = 5.0, axis: int | None = None) -> np.ndarray:
    """Boolean RFI mask: ``True`` where a sample exceeds ``threshold`` robust sigma.

    Uses the median and :func:`mad_sigma` so the flagging is not itself biased by
    the interference it is trying to find.
    """
    data = np.asarray(data, dtype=float)
    med = np.median(data, axis=axis, keepdims=True)
    sigma = mad_sigma(data, axis=axis)
    if axis is not None:
        sigma = np.expand_dims(sigma, axis=axis)
    return np.abs(data - med) > threshold * sigma


def spectral_kurtosis(power: np.ndarray, axis: int = 0) -> np.ndarray:
    """Generalised spectral-kurtosis (SK) estimator over ``M`` power samples.

    :math:`\\mathrm{SK} = \\dfrac{M+1}{M-1}\\left(\\dfrac{M\\,S_2}{S_1^2} - 1\\right)`
    with :math:`S_1=\\sum P`, :math:`S_2=\\sum P^2` over the ``M`` samples along
    ``axis``. For RFI-free Gaussian noise SK ≈ 1; a steady (CW) interferer pushes
    SK below 1, a spiky/bursty one above 1. (Nita & Gary 2010.)

    Parameters
    ----------
    power
        Power (magnitude-squared) samples; SK is computed across ``axis``.
    axis
        The accumulation axis (its length is ``M``).
    """
    power = np.asarray(power, dtype=float)
    m = power.shape[axis]
    s1 = power.sum(axis=axis)
    s2 = (power**2).sum(axis=axis)
    with np.errstate(divide="ignore", invalid="ignore"):
        sk = (m + 1) / (m - 1) * (m * s2 / s1**2 - 1)
    return sk


def flag_by_kurtosis(
    power: np.ndarray, axis: int = 0, low: float = 0.7, high: float = 1.3
) -> np.ndarray:
    """Flag channels whose spectral kurtosis falls outside ``[low, high]``.

    Returns a boolean mask over the non-``axis`` dimensions: ``True`` where the SK
    indicates interference (too steady below ``low``, too spiky above ``high``).
    """
    sk = spectral_kurtosis(power, axis=axis)
    return (sk < low) | (sk > high)
