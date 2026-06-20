"""Tests for jansky.vlf -- VLF monitoring and SID detection."""

from __future__ import annotations

import numpy as np

from jansky import vlf


def test_sid_profile_rises_then_decays():
    t = np.linspace(0, 24, 2000)
    p = vlf.sid_profile(t, onset=10.0, amplitude=8.0, rise_min=5, decay_min=40)
    assert np.all(p[t < 10.0] == 0.0)
    # peak occurs after onset, well before full decay
    peak_t = t[np.argmax(p)]
    assert 10.0 < peak_t < 11.0
    assert p.max() > 0


def test_detect_sids_recovers_flares():
    flares = [(8.0, 7.0), (13.5, 11.0), (19.0, 9.0)]
    hours, signal, onsets = vlf.simulate_vlf_day(flares=flares, seed=1)
    det = vlf.detect_sids(hours, signal, threshold=5.0)
    assert det.count == len(flares)
    # each detected onset is close to a true flare onset
    for true in onsets:
        assert np.min(np.abs(det.onsets - true)) < 0.3


def test_quiet_day_has_no_false_sids():
    hours, signal, _ = vlf.simulate_vlf_day(flares=[], seed=2)
    det = vlf.detect_sids(hours, signal, threshold=5.0)
    assert det.count == 0
