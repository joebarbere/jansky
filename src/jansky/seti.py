"""The radio search for technosignatures (SETI).

A narrowband transmitter on another world drifts in frequency as that world
spins and orbits -- the **Doppler drift**. In a high-resolution waterfall (time
vs fine frequency) the signal traces a sloped line. Finding it is the SETI
analogue of the single-pulse DM search in :mod:`jansky.transients`: try many
trial drift rates, de-drift, integrate, and look for a spike. Real interference
is rejected by an **ON/OFF cadence** -- a true signal from the target appears
only when the telescope points at it. ``turboSETI`` (the ``seti`` extra; see
Chapter 16) does exactly this over Breakthrough Listen data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "drifting_tone",
    "dedrift",
    "drift_search",
    "DriftSearchResult",
    "cadence_detection",
]


def drifting_tone(
    n_time: int,
    n_freq: int,
    drift_rate: float,
    *,
    f0: float | None = None,
    snr: float = 10.0,
    width: float = 1.5,
    noise: float = 1.0,
    present: bool = True,
    seed: int | None = 0,
) -> np.ndarray:
    """Synthesise a waterfall with a drifting narrowband tone.

    Parameters
    ----------
    n_time, n_freq
        Waterfall shape (time samples, frequency channels).
    drift_rate
        Drift in **channels per time sample** (the signal's slope).
    f0
        Starting channel of the tone (default: centre).
    snr
        Peak amplitude of the tone (in units of the noise sigma when ``noise=1``).
    width
        Gaussian line width (channels).
    noise
        Std of additive Gaussian noise.
    present
        If ``False``, only noise is generated (an OFF-source / blank pointing).
    seed
        Seed for reproducibility.

    Returns
    -------
    numpy.ndarray
        Waterfall, shape ``(n_time, n_freq)``.
    """
    rng = np.random.default_rng(seed)
    waterfall = rng.normal(0.0, noise, size=(n_time, n_freq))
    if present:
        if f0 is None:
            f0 = n_freq / 2
        channels = np.arange(n_freq)
        for t in range(n_time):
            centre = f0 + drift_rate * t
            waterfall[t] += snr * np.exp(-0.5 * ((channels - centre) / width) ** 2)
    return waterfall


def dedrift(waterfall: np.ndarray, drift_rate: float) -> np.ndarray:
    """Integrate a waterfall along a trial drift line into a 1-D spectrum.

    Each time row is shifted in frequency by ``-round(drift_rate * t)`` channels
    (undoing the assumed drift) and the rows are summed. At the true drift rate
    the signal aligns and the integrated spectrum spikes.
    """
    waterfall = np.asarray(waterfall)
    n_time = waterfall.shape[0]
    out = np.zeros(waterfall.shape[1])
    for t in range(n_time):
        shift = int(round(drift_rate * t))
        out += np.roll(waterfall[t], -shift)
    return out


def _snr(spectrum: np.ndarray) -> float:
    med = np.median(spectrum)
    mad = np.median(np.abs(spectrum - med))
    sigma = 1.4826 * mad if mad > 0 else spectrum.std()
    return float((spectrum.max() - med) / sigma) if sigma > 0 else 0.0


@dataclass
class DriftSearchResult:
    """Outcome of :func:`drift_search`."""

    drift_rates: np.ndarray  #: trial drift rates (channels/sample)
    snr: np.ndarray  #: peak S/N at each trial drift
    best_drift: float  #: drift rate with the highest S/N
    best_snr: float  #: that highest S/N


def drift_search(waterfall: np.ndarray, drift_rates: np.ndarray) -> DriftSearchResult:
    """Brute-force Doppler-drift search: peak S/N over a grid of drift rates."""
    drift_rates = np.asarray(drift_rates, dtype=float)
    snr = np.array([_snr(dedrift(waterfall, d)) for d in drift_rates])
    best = int(np.argmax(snr))
    return DriftSearchResult(
        drift_rates=drift_rates,
        snr=snr,
        best_drift=float(drift_rates[best]),
        best_snr=float(snr[best]),
    )


def cadence_detection(
    on_results: list[DriftSearchResult],
    off_results: list[DriftSearchResult],
    threshold: float = 8.0,
) -> bool:
    """Apply an ON/OFF cadence test to reject interference.

    A genuine technosignature from the target appears in every ON-source scan and
    in none of the OFF-source scans. Returns ``True`` only if all ON scans exceed
    ``threshold`` and all OFF scans fall below it.
    """
    on_ok = all(r.best_snr >= threshold for r in on_results)
    off_ok = all(r.best_snr < threshold for r in off_results)
    return on_ok and off_ok
