"""Pulsar timing arrays and the nanohertz gravitational-wave background.

A pulsar is a clock; an *array* of millisecond pulsars spread across the sky is a
galaxy-sized gravitational-wave detector. A passing low-frequency gravitational
wave perturbs the pulse arrival times, leaving correlated wiggles in the timing
*residuals* of pulsar pairs. The signature that the correlation is gravitational
(and not, say, a clock error) is its specific dependence on the angle between two
pulsars: the **Hellings--Downs curve**. This module simulates that and lets the
chapter recover the curve -- exactly what NANOGrav/EPTA/PPTA reported in 2023.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "hellings_downs",
    "angular_separations",
    "simulate_pta_residuals",
    "pairwise_correlations",
    "PTACorrelations",
]


def hellings_downs(separation: np.ndarray) -> np.ndarray:
    """The Hellings--Downs correlation as a function of pulsar-pair separation.

    :math:`\\Gamma(\\theta) = \\tfrac{3}{2}x\\ln x - \\tfrac{1}{4}x + \\tfrac{1}{2}`
    with :math:`x = (1-\\cos\\theta)/2`, normalised so the autocorrelation
    :math:`\\Gamma(0)=1` (the "pulsar term"); just above zero separation the
    cross-correlation jumps to 1/2. This quadrupolar shape is the fingerprint of
    a gravitational-wave background.

    Parameters
    ----------
    separation
        Angular separation(s) between pulsar pairs, in radians.

    Returns
    -------
    numpy.ndarray
        The HD correlation at each separation.
    """
    sep = np.asarray(separation, dtype=float)
    x = (1.0 - np.cos(sep)) / 2.0
    with np.errstate(divide="ignore", invalid="ignore"):
        gamma = 1.5 * x * np.log(x) - 0.25 * x + 0.5
    return np.where(x == 0.0, 1.0, gamma)


def angular_separations(positions: np.ndarray) -> np.ndarray:
    """Pairwise great-circle separations (radians) for unit sky vectors.

    Parameters
    ----------
    positions
        ``(n_pulsars, 3)`` array of unit vectors on the sky.

    Returns
    -------
    numpy.ndarray
        ``(n_pulsars, n_pulsars)`` matrix of angular separations.
    """
    positions = np.asarray(positions, dtype=float)
    dots = np.clip(positions @ positions.T, -1.0, 1.0)
    return np.arccos(dots)


def simulate_pta_residuals(
    positions: np.ndarray,
    n_epochs: int = 200,
    gwb_amplitude: float = 1.0,
    white_noise: float = 0.3,
    seed: int | None = 0,
) -> np.ndarray:
    """Simulate timing residuals for a pulsar array with an HD-correlated signal.

    Injects a common signal whose inter-pulsar correlation follows the
    Hellings--Downs curve (built as a covariance matrix and drawn via Cholesky),
    plus independent per-pulsar white noise.

    Parameters
    ----------
    positions
        ``(n_pulsars, 3)`` unit sky vectors.
    n_epochs
        Number of observing epochs.
    gwb_amplitude
        Amplitude of the common (gravitational-wave-background) signal.
    white_noise
        Std of independent per-pulsar measurement noise.
    seed
        Seed for reproducibility.

    Returns
    -------
    numpy.ndarray
        ``(n_pulsars, n_epochs)`` residuals.
    """
    positions = np.asarray(positions, dtype=float)
    n = positions.shape[0]
    sep = angular_separations(positions)
    cov = hellings_downs(sep)
    np.fill_diagonal(cov, 1.0)
    # Regularise to a valid (positive-definite) covariance before Cholesky.
    eigmin = np.linalg.eigvalsh(cov).min()
    if eigmin < 1e-8:
        cov = cov + (1e-8 - eigmin) * np.eye(n)
    chol = np.linalg.cholesky(cov)

    rng = np.random.default_rng(seed)
    common = gwb_amplitude * (chol @ rng.standard_normal((n, n_epochs)))
    noise = rng.normal(0.0, white_noise, size=(n, n_epochs))
    return common + noise


@dataclass
class PTACorrelations:
    """Pairwise correlations vs separation (see :func:`pairwise_correlations`)."""

    separations: np.ndarray  #: pair angular separations (radians)
    correlations: np.ndarray  #: measured Pearson correlation per pair


def pairwise_correlations(residuals: np.ndarray, positions: np.ndarray) -> PTACorrelations:
    """Measure each pulsar pair's residual correlation vs their sky separation.

    Returns the empirical (Pearson) correlation for every distinct pair, ready to
    be binned and compared against :func:`hellings_downs`.
    """
    residuals = np.asarray(residuals)
    n = residuals.shape[0]
    sep = angular_separations(positions)
    corr = np.corrcoef(residuals)
    seps, corrs = [], []
    for i in range(n):
        for j in range(i + 1, n):
            seps.append(sep[i, j])
            corrs.append(corr[i, j])
    return PTACorrelations(separations=np.array(seps), correlations=np.array(corrs))
