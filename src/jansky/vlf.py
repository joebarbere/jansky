"""VLF monitoring and the ionosphere (SuperSID / sudden ionospheric disturbances).

Very-low-frequency (3--30 kHz) navigation/military transmitters bounce off the
ionosphere's D-layer. Monitor a distant VLF carrier's received amplitude and you
are, in effect, measuring the D-layer in real time. When a **solar flare** hits,
its X-rays suddenly ionise the D-layer and the received signal jumps -- a
**sudden ionospheric disturbance (SID)**. A simple VLF receiver and loop antenna
(the Stanford/SARA *SuperSID* project, see ``docs/projects.md``) thus detects
solar flares from your desk, day or night. This module simulates a day of VLF
monitoring -- diurnal baseline plus flare-driven SIDs -- and detects the events.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "sid_profile",
    "simulate_vlf_day",
    "detect_sids",
    "SIDDetection",
]


def sid_profile(
    t_hours: np.ndarray,
    onset: float,
    amplitude: float,
    rise_min: float = 5.0,
    decay_min: float = 40.0,
) -> np.ndarray:
    """A sudden-ionospheric-disturbance profile: fast rise, slow recovery.

    Models the received-amplitude enhancement after a flare: a sharp rise over
    ``rise_min`` minutes then an exponential recovery over ``decay_min`` minutes.
    Times are in hours.
    """
    t = np.asarray(t_hours, dtype=float)
    out = np.zeros_like(t)
    after = t >= onset
    dt_min = (t[after] - onset) * 60.0
    out[after] = amplitude * (1.0 - np.exp(-dt_min / rise_min)) * np.exp(-dt_min / decay_min)
    return out


def simulate_vlf_day(
    flares: list[tuple[float, float]] | None = None,
    *,
    sample_per_hour: float = 240.0,
    diurnal_amp: float = 3.0,
    noise: float = 0.3,
    seed: int | None = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate 24 h of VLF received amplitude with a diurnal baseline and flares.

    Parameters
    ----------
    flares
        List of ``(onset_hour, amplitude)`` flare events. Default: a couple.
    sample_per_hour
        Samples per hour (240 ≈ every 15 s).
    diurnal_amp
        Amplitude of the slow day/night (D-layer) variation.
    noise
        Std of measurement noise.
    seed
        Seed for reproducibility.

    Returns
    -------
    (hours, signal, flare_onsets)
        Time axis (hours, 0-24), received amplitude, and the true flare onset hours.
    """
    if flares is None:
        flares = [(9.5, 6.0), (14.2, 10.0)]
    rng = np.random.default_rng(seed)
    n = int(24 * sample_per_hour)
    hours = np.linspace(0, 24, n, endpoint=False)
    # Smooth diurnal baseline: higher by day (sunlit D-layer), lower at night.
    baseline = 10.0 + diurnal_amp * np.sin((hours - 6) / 24 * 2 * np.pi)
    signal = baseline + rng.normal(0.0, noise, size=n)
    onsets = []
    for onset, amp in flares:
        signal += sid_profile(hours, onset, amp)
        onsets.append(onset)
    return hours, signal, np.array(onsets)


@dataclass
class SIDDetection:
    """Detected SID/flare events (see :func:`detect_sids`)."""

    onsets: np.ndarray  #: detected onset times (hours)
    count: int


def detect_sids(
    hours: np.ndarray,
    signal: np.ndarray,
    threshold: float = 5.0,
    window_hours: float = 2.0,
    min_separation_hours: float = 0.5,
) -> SIDDetection:
    """Detect SIDs by de-trending the diurnal baseline and thresholding.

    A running-median filter removes the slow day/night variation; excursions
    above ``threshold`` noise-sigma are flagged, and nearby samples are merged
    into one event (reported at the rise onset).
    """
    from scipy.ndimage import median_filter

    signal = np.asarray(signal, dtype=float)
    hours = np.asarray(hours, dtype=float)
    dt = hours[1] - hours[0]
    win = max(3, int(window_hours / dt) | 1)  # odd window
    detrended = signal - median_filter(signal, size=win, mode="nearest")
    mad = np.median(np.abs(detrended - np.median(detrended)))
    sigma = 1.4826 * mad if mad > 0 else detrended.std()
    above = np.where(detrended > threshold * sigma)[0]
    if above.size == 0:
        return SIDDetection(onsets=np.array([]), count=0)

    groups = np.split(above, np.where(np.diff(hours[above]) > min_separation_hours)[0] + 1)
    onsets = [hours[g[0]] for g in groups]  # rise onset = first crossing
    return SIDDetection(onsets=np.array(onsets), count=len(onsets))
