"""Radio transients: dispersion, de-dispersion, and single-pulse searching.

The tools behind the fast-radio-burst (FRB) chapter, and shared with the pulsar
material (Chapter 13). A broadband pulse travelling through the ionised
interstellar/intergalactic medium is delayed more at lower frequencies -- the
**cold-plasma dispersion law** -- by an amount set by the *dispersion measure*
(DM), the integrated column of free electrons. Finding a pulse means trying many
trial DMs, de-dispersing, and looking for a matched-filter spike: the classic
single-pulse search.

Everything here is plain NumPy so the maths stays inspectable; ``turboSETI`` /
PRESTO do the same at survey scale (see Chapter 16 and :mod:`jansky.formats`).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "DM_CONST",
    "dispersion_delay",
    "disperse_pulse",
    "dedisperse",
    "dm_search",
    "DMSearchResult",
    "boxcar_snr",
    "macquart_redshift",
]

#: Dispersion constant in MHz^2 cm^3 pc^-1 s (the conventional value, k_DM).
DM_CONST = 4.148808e3


def dispersion_delay(dm: float, f_lo_mhz: float, f_hi_mhz: float) -> float:
    """Cold-plasma dispersion delay (seconds) between two frequencies.

    :math:`\\Delta t = k_\\mathrm{DM}\\,\\mathrm{DM}\\,(f_\\mathrm{lo}^{-2} - f_\\mathrm{hi}^{-2})`,
    with frequencies in MHz and DM in pc cm^-3. The lower frequency arrives later.
    """
    return DM_CONST * dm * (f_lo_mhz**-2 - f_hi_mhz**-2)


def disperse_pulse(
    n_time: int,
    freqs_mhz: np.ndarray,
    dm: float,
    dt: float,
    *,
    t0_index: int = 0,
    width_samples: float = 2.0,
    amplitude: float = 10.0,
    noise: float = 1.0,
    seed: int | None = 0,
) -> np.ndarray:
    """Build a synthetic dynamic spectrum containing one dispersed pulse.

    Parameters
    ----------
    n_time
        Number of time samples.
    freqs_mhz
        Channel centre frequencies (MHz), shape ``(n_chan,)``.
    dm
        Dispersion measure (pc cm^-3).
    dt
        Time sample spacing (s).
    t0_index
        Arrival time (sample index) at the highest frequency.
    width_samples
        Gaussian pulse width (samples).
    amplitude
        Peak pulse amplitude (in units of the noise sigma when ``noise=1``).
    noise
        Std of additive Gaussian noise per sample.
    seed
        Seed for reproducibility.

    Returns
    -------
    numpy.ndarray
        Dynamic spectrum, shape ``(n_time, n_chan)``.
    """
    freqs_mhz = np.asarray(freqs_mhz, dtype=float)
    f_ref = freqs_mhz.max()
    rng = np.random.default_rng(seed)
    dynspec = rng.normal(0.0, noise, size=(n_time, freqs_mhz.size))
    times = np.arange(n_time)
    for j, f in enumerate(freqs_mhz):
        delay = dispersion_delay(dm, f, f_ref) / dt  # samples, >= 0
        centre = t0_index + delay
        dynspec[:, j] += amplitude * np.exp(-0.5 * ((times - centre) / width_samples) ** 2)
    return dynspec


def dedisperse(dynspec: np.ndarray, freqs_mhz: np.ndarray, dm: float, dt: float) -> np.ndarray:
    """De-disperse a dynamic spectrum at a trial DM and sum to a time series.

    Each channel is shifted earlier by its dispersion delay (rounded to whole
    samples) relative to the highest frequency, then all channels are summed. At
    the true DM the pulse aligns across channels and the summed series spikes.
    """
    dynspec = np.asarray(dynspec)
    freqs_mhz = np.asarray(freqs_mhz, dtype=float)
    f_ref = freqs_mhz.max()
    out = np.zeros(dynspec.shape[0])
    for j, f in enumerate(freqs_mhz):
        shift = int(round(dispersion_delay(dm, f, f_ref) / dt))
        out += np.roll(dynspec[:, j], -shift)
    return out


def _snr(series: np.ndarray) -> float:
    """Robust peak signal-to-noise: (peak - median) / MAD-based sigma."""
    med = np.median(series)
    mad = np.median(np.abs(series - med))
    sigma = 1.4826 * mad if mad > 0 else series.std()
    return float((series.max() - med) / sigma) if sigma > 0 else 0.0


@dataclass
class DMSearchResult:
    """Outcome of :func:`dm_search`."""

    dms: np.ndarray  #: trial DMs
    snr: np.ndarray  #: peak S/N at each trial DM
    best_dm: float  #: DM with the highest S/N
    best_snr: float  #: that highest S/N


def dm_search(
    dynspec: np.ndarray,
    freqs_mhz: np.ndarray,
    dt: float,
    dm_trials: np.ndarray,
) -> DMSearchResult:
    """Brute-force single-pulse DM search ("the butterfly").

    De-disperses at each trial DM and records the peak S/N of the summed time
    series. The S/N-vs-DM curve peaks sharply at the pulse's true DM.
    """
    dm_trials = np.asarray(dm_trials, dtype=float)
    snr = np.array([_snr(dedisperse(dynspec, freqs_mhz, dm, dt)) for dm in dm_trials])
    best = int(np.argmax(snr))
    return DMSearchResult(
        dms=dm_trials, snr=snr, best_dm=float(dm_trials[best]), best_snr=float(snr[best])
    )


def boxcar_snr(series: np.ndarray, widths: np.ndarray) -> tuple[float, int, int]:
    """Matched-filter the time series with boxcars of several widths.

    Returns ``(best_snr, best_width, peak_index)``. A boxcar matched to the pulse
    width maximises S/N -- the optimal detector for a top-hat pulse in white noise.
    """
    series = np.asarray(series, dtype=float)
    med = np.median(series)
    mad = np.median(np.abs(series - med))
    sigma = 1.4826 * mad if mad > 0 else series.std()
    best = (-np.inf, 1, 0)
    for w in np.atleast_1d(widths).astype(int):
        kernel = np.ones(w) / np.sqrt(w)  # preserves white-noise sigma
        conv = np.convolve(series - med, kernel, mode="same")
        idx = int(np.argmax(conv))
        snr = conv[idx] / sigma if sigma > 0 else 0.0
        if snr > best[0]:
            best = (float(snr), int(w), idx)
    return best


def macquart_redshift(dm_excess: float, slope: float = 900.0) -> float:
    """Rough redshift from an FRB's extragalactic DM via the Macquart relation.

    The mean cosmic dispersion grows roughly linearly with redshift,
    :math:`\\langle \\mathrm{DM_{cosmic}} \\rangle \\approx 900\\,z` pc cm^-3
    (Macquart et al. 2020), so :math:`z \\approx \\mathrm{DM_{excess}}/900`. This
    is an *order-of-magnitude* estimate -- after subtracting the Milky Way and
    host contributions, and with large sightline scatter.
    """
    return float(dm_excess / slope)
