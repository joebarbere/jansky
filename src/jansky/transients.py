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

from .constants import DM_CONST, MACQUART_SLOPE

__all__ = [
    "DM_CONST",
    "dispersion_delay",
    "disperse_pulse",
    "dedisperse",
    "dm_search",
    "DMSearchResult",
    "boxcar_snr",
    "macquart_redshift",
    "fold_profile",
    "epoch_folding_search",
    "PeriodSearchResult",
    "surface_bfield",
    "characteristic_age",
    "death_line_pdot",
]

# DM_CONST (k_DM, MHz^2 cm^3 pc^-1 s) now lives in jansky.constants and is
# re-exported here so existing imports (`from jansky.transients import DM_CONST`)
# keep working.


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


def macquart_redshift(dm_excess: float, slope: float = MACQUART_SLOPE) -> float:
    """Rough redshift from an FRB's extragalactic DM via the Macquart relation.

    The mean cosmic dispersion grows roughly linearly with redshift,
    :math:`\\langle \\mathrm{DM_{cosmic}} \\rangle \\approx 900\\,z` pc cm^-3
    (Macquart et al. 2020), so :math:`z \\approx \\mathrm{DM_{excess}}/900`. This
    is an *order-of-magnitude* estimate -- after subtracting the Milky Way and
    host contributions, and with large sightline scatter.

    The slope itself is **model-dependent**: it follows from the cosmic baryon
    density and the assumed fraction of baryons in the diffuse ionised IGM, so it
    is not a universal constant (see :data:`jansky.constants.MACQUART_SLOPE`).
    """
    return float(dm_excess / slope)


# --- Period finding & the P-Pdot diagram (Chapter 47: long-period transients) ----------


def fold_profile(
    times: np.ndarray,
    values: np.ndarray,
    period: float,
    n_bins: int = 20,
    t0: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fold a time series at a trial ``period`` into a pulse profile.

    Each sample's **phase** is ``((t - t0) / period) mod 1``; samples are binned by
    phase and averaged. At the true period a pulse stacks up in one bin; at a wrong
    period it smears out. The engine behind :func:`epoch_folding_search`.

    Returns ``(phase_centres, profile, counts)`` -- the profile is NaN in empty bins.
    """
    times = np.asarray(times, dtype=float)
    values = np.asarray(values, dtype=float)
    phase = ((times - t0) / period) % 1.0
    idx = np.minimum((phase * n_bins).astype(int), n_bins - 1)
    counts = np.bincount(idx, minlength=n_bins).astype(float)
    sums = np.bincount(idx, weights=values, minlength=n_bins)
    with np.errstate(invalid="ignore", divide="ignore"):
        profile = np.where(counts > 0, sums / counts, np.nan)
    centres = (np.arange(n_bins) + 0.5) / n_bins
    return centres, profile, counts


@dataclass
class PeriodSearchResult:
    """Outcome of :func:`epoch_folding_search`."""

    periods: np.ndarray  #: trial periods (s)
    stat: np.ndarray  #: epoch-folding statistic at each trial period
    best_period: float  #: period with the highest statistic
    best_stat: float  #: that highest statistic


def epoch_folding_search(
    times: np.ndarray,
    values: np.ndarray,
    periods: np.ndarray,
    n_bins: int = 20,
) -> PeriodSearchResult:
    """Blind period search by epoch folding -- find a period without knowing it.

    For each trial period the series is folded (:func:`fold_profile`) and scored with
    the Leahy (1983) chi-square statistic
    :math:`S = \\sum_i n_i (m_i - \\bar m)^2 / \\sigma^2`, where :math:`m_i` is the
    mean in phase bin *i*, :math:`n_i` its count, and :math:`\\sigma^2` the data
    variance. ``S`` peaks sharply at the true period (and its harmonics). This is how
    the minutes-to-hours periods of long-period transients are recovered.
    """
    times = np.asarray(times, dtype=float)
    values = np.asarray(values, dtype=float)
    var = values.var()
    periods = np.asarray(periods, dtype=float)
    stats = np.empty(periods.size)
    for k, period in enumerate(periods):
        _, profile, counts = fold_profile(times, values, period, n_bins)
        good = counts > 0
        if not good.any() or var == 0:
            stats[k] = 0.0
            continue
        mean = np.average(profile[good], weights=counts[good])
        stats[k] = float(np.sum(counts[good] * (profile[good] - mean) ** 2) / var)
    best = int(np.argmax(stats))
    return PeriodSearchResult(
        periods=periods, stat=stats, best_period=float(periods[best]), best_stat=float(stats[best])
    )


def surface_bfield(period: np.ndarray | float, pdot: np.ndarray | float) -> np.ndarray:
    """Canonical dipole surface magnetic field (Gauss) from ``period`` and ``pdot``.

    :math:`B_\\mathrm{surf} \\approx 3.2\\times10^{19}\\sqrt{P\\,\\dot P}` G, with ``P``
    in seconds and ``pdot`` dimensionless -- the standard magnetic-dipole spin-down
    estimate. A 1 s pulsar with :math:`\\dot P = 10^{-15}` has :math:`B \\sim 10^{12}` G;
    magnetars reach :math:`10^{14}`-:math:`10^{15}` G.
    """
    return 3.2e19 * np.sqrt(np.asarray(period, dtype=float) * np.asarray(pdot, dtype=float))


def characteristic_age(period: np.ndarray | float, pdot: np.ndarray | float) -> np.ndarray:
    """Characteristic (spin-down) age :math:`\\tau_c = P / (2\\dot P)`, in seconds.

    An upper-limit age assuming magnetic-dipole braking from a much faster birth spin.
    """
    return np.asarray(period, dtype=float) / (2.0 * np.asarray(pdot, dtype=float))


def death_line_pdot(period: np.ndarray | float, b_over_p2_threshold: float = 3.2e11) -> np.ndarray:
    """The pulsar **death line**, as the minimum ``pdot`` for radio emission at ``P``.

    Below the death line a rotation-powered pulsar can no longer sustain the pair
    cascades that power coherent radio emission. Using the common constant-:math:`B/P^2`
    criterion (:math:`B/P^2 >` threshold) with :math:`B = 3.2\\times10^{19}\\sqrt{P\\dot P}`
    gives :math:`\\dot P_\\mathrm{death} = (\\text{thr}/3.2\\times10^{19})^2\\,P^3` -- a slope-3
    line in the :math:`P`-:math:`\\dot P` plane. The default threshold places it near
    :math:`(P,\\dot P) = (1\\,\\mathrm{s}, 10^{-16})`. This is one representative model;
    published death lines differ by their assumed gap physics. It is what makes the
    minutes-to-hours periods of long-period transients so startling: as rotation-powered
    neutron stars they would sit *far* below any death line, yet they emit.
    """
    p = np.asarray(period, dtype=float)
    return (b_over_p2_threshold / 3.2e19) ** 2 * p**3
