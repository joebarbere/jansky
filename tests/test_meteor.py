"""Tests for jansky.meteor -- meteor-scatter echoes and detection."""

from __future__ import annotations

import numpy as np

from jansky import meteor


def test_underdense_echo_shape():
    t = np.linspace(0, 1, 1000)
    echo = meteor.underdense_echo(t, t0=0.2, amplitude=10.0, decay_time=0.1)
    assert np.all(echo[t < 0.2] == 0.0)          # nothing before arrival
    assert np.isclose(echo[np.searchsorted(t, 0.2)], 10.0, atol=0.1)  # rise to peak
    # exponential decay: one decay-time later ~ amplitude/e
    idx = np.searchsorted(t, 0.3)
    assert np.isclose(echo[idx], 10.0 / np.e, rtol=0.05)


def test_detect_pings_recovers_count():
    times, power, ping_times = meteor.simulate_meteor_timeseries(
        duration_s=60, rate_per_min=12, sample_rate=200, noise=1.0, seed=3
    )
    det = meteor.detect_pings(times, power, threshold=6.0)
    # Most injected pings (the bright ones) are recovered; no wild over-counting.
    assert det.count >= 0.5 * len(ping_times)
    assert det.count <= len(ping_times) + 2


def test_detect_pings_quiet_record_is_empty():
    rng = np.random.default_rng(0)
    times = np.arange(2000) / 100.0
    power = rng.normal(0, 1, 2000)  # pure noise
    det = meteor.detect_pings(times, power, threshold=6.0)
    assert det.count <= 1  # essentially nothing crosses 6 sigma
