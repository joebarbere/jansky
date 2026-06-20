"""Meteor-scatter radio detection.

A meteor ablating in the upper atmosphere leaves a column of ionisation that
briefly reflects radio waves. Point a VHF receiver at a *distant* transmitter
(below the horizon) tuned to an otherwise-quiet frequency -- the GRAVES radar in
France, or a far-off FM/TV carrier -- and each meteor produces a short "ping" of
received signal: **forward meteor scatter**. This is cheap, beginner-friendly
real radio astronomy (see ``docs/projects.md``). The two classic echo types:

* **underdense** -- a faint trail; instantaneous rise then exponential decay
  (decay time set by ambipolar diffusion), milliseconds to ~1 s;
* **overdense** -- a dense trail that reflects for longer with an irregular,
  plateau-like envelope.

This module simulates such pings and detects them, so the chapter runs offline.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "underdense_echo",
    "overdense_echo",
    "simulate_meteor_timeseries",
    "detect_pings",
    "MeteorDetection",
]


def underdense_echo(t: np.ndarray, t0: float, amplitude: float, decay_time: float) -> np.ndarray:
    """Underdense meteor echo: instantaneous rise at ``t0`` then exponential decay."""
    t = np.asarray(t, dtype=float)
    echo = np.zeros_like(t)
    after = t >= t0
    echo[after] = amplitude * np.exp(-(t[after] - t0) / decay_time)
    return echo


def overdense_echo(t: np.ndarray, t0: float, amplitude: float, duration: float) -> np.ndarray:
    """Overdense meteor echo: a longer, roughly flat-topped reflection of length ``duration``."""
    t = np.asarray(t, dtype=float)
    echo = np.zeros_like(t)
    window = (t >= t0) & (t <= t0 + duration)
    # Smooth rise/fall (sine-squared window) for an irregular plateau-ish shape.
    phase = (t[window] - t0) / duration
    echo[window] = amplitude * np.sin(np.pi * phase) ** 0.5
    return echo


def simulate_meteor_timeseries(
    duration_s: float = 60.0,
    rate_per_min: float = 10.0,
    sample_rate: float = 100.0,
    *,
    noise: float = 1.0,
    seed: int | None = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate a meteor-scatter power time series with random pings.

    Parameters
    ----------
    duration_s
        Length of the record (s).
    rate_per_min
        Mean meteor rate (pings per minute); actual count is Poisson.
    sample_rate
        Samples per second.
    noise
        Std of the background noise.
    seed
        Seed for reproducibility.

    Returns
    -------
    (times, power, ping_times)
        Time axis (s), received power, and the true ping arrival times.
    """
    rng = np.random.default_rng(seed)
    n = int(duration_s * sample_rate)
    times = np.arange(n) / sample_rate
    power = rng.normal(0.0, noise, size=n)

    n_pings = rng.poisson(rate_per_min * duration_s / 60.0)
    ping_times = np.sort(rng.uniform(0, duration_s, n_pings))
    for t0 in ping_times:
        amp = rng.uniform(8, 25)
        if rng.random() < 0.8:  # mostly underdense
            power += underdense_echo(times, t0, amp, rng.uniform(0.05, 0.4))
        else:
            power += overdense_echo(times, t0, amp, rng.uniform(0.5, 2.0))
    return times, power, ping_times


@dataclass
class MeteorDetection:
    """Detected meteor pings (see :func:`detect_pings`)."""

    times: np.ndarray  #: detected ping times (s)
    count: int  #: number detected


def detect_pings(
    times: np.ndarray,
    power: np.ndarray,
    threshold: float = 6.0,
    min_separation_s: float = 0.3,
) -> MeteorDetection:
    """Detect pings as threshold crossings, merging samples within ``min_separation_s``.

    ``threshold`` is in units of the noise sigma (robust MAD estimate). Returns the
    time of each detected ping (the local power maximum within the crossing).
    """
    power = np.asarray(power, dtype=float)
    times = np.asarray(times, dtype=float)
    med = np.median(power)
    mad = np.median(np.abs(power - med))
    sigma = 1.4826 * mad if mad > 0 else power.std()
    above = np.where(power - med > threshold * sigma)[0]
    if above.size == 0:
        return MeteorDetection(times=np.array([]), count=0)

    # Group consecutive/near samples into events; take the peak time of each.
    groups = np.split(above, np.where(np.diff(times[above]) > min_separation_s)[0] + 1)
    peaks = [times[g[np.argmax(power[g])]] for g in groups]
    return MeteorDetection(times=np.array(peaks), count=len(peaks))
