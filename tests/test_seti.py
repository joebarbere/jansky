"""Tests for jansky.seti -- the Doppler-drift technosignature search."""

from __future__ import annotations

import numpy as np

from jansky import seti


def test_drift_search_recovers_true_drift():
    true_drift = 0.25  # channels per time sample
    wf = seti.drifting_tone(
        n_time=128, n_freq=512, drift_rate=true_drift, snr=6.0, seed=1
    )
    trials = np.arange(-1.0, 1.01, 0.05)
    result = seti.drift_search(wf, trials)
    assert abs(result.best_drift - true_drift) <= 0.05
    assert result.best_snr > result.snr[0]


def test_dedrift_aligns_at_true_drift():
    wf = seti.drifting_tone(n_time=100, n_freq=400, drift_rate=0.3, snr=5.0, seed=2)
    aligned = seti.dedrift(wf, 0.3)
    misaligned = seti.dedrift(wf, -0.3)
    assert aligned.max() > misaligned.max()


def test_blank_pointing_has_no_signal():
    wf = seti.drifting_tone(n_time=64, n_freq=256, drift_rate=0.2, present=False, seed=3)
    trials = np.arange(-0.5, 0.51, 0.1)
    result = seti.drift_search(wf, trials)
    # No injected tone -> low S/N everywhere.
    assert result.best_snr < 8.0


def test_cadence_rejects_interference():
    trials = np.arange(-0.5, 0.51, 0.05)
    # ON scans: strong drifting tone present
    on = [seti.drift_search(
        seti.drifting_tone(80, 400, 0.2, snr=10, seed=s), trials) for s in (10, 11, 12)]
    # OFF scans: blank
    off = [seti.drift_search(
        seti.drifting_tone(80, 400, 0.2, snr=10, present=False, seed=s), trials)
        for s in (20, 21)]
    assert seti.cadence_detection(on, off, threshold=8.0)
    # Interference present in OFF too -> rejected
    off_rfi = [seti.drift_search(
        seti.drifting_tone(80, 400, 0.0, snr=10, seed=s), trials) for s in (30, 31)]
    assert not seti.cadence_detection(on, off_rfi, threshold=8.0)
