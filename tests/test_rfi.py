"""Tests for jansky.rfi -- robust stats and spectral kurtosis."""

from __future__ import annotations

import numpy as np

from jansky import rfi


def test_mad_sigma_robust_to_outliers():
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 10000)
    base = rfi.mad_sigma(x)
    x[:50] = 1000.0  # strong RFI spikes
    assert abs(rfi.mad_sigma(x) - base) < 0.1  # MAD barely moves
    assert x.std() > 5  # but the std is wrecked


def test_flag_outliers_catches_spikes():
    rng = np.random.default_rng(1)
    x = rng.normal(0, 1, 1000)
    x[100] = 20.0
    x[500] = -15.0
    mask = rfi.flag_outliers(x, threshold=6.0)
    assert mask[100] and mask[500]
    assert mask.sum() <= 5  # few false positives


def test_spectral_kurtosis_gaussian_near_one():
    rng = np.random.default_rng(2)
    # power of complex Gaussian voltage is exponential; SK ~ 1
    volt = rng.normal(size=(4000, 8)) + 1j * rng.normal(size=(4000, 8))
    power = np.abs(volt) ** 2
    sk = rfi.spectral_kurtosis(power, axis=0)
    assert np.all(np.abs(sk - 1.0) < 0.15)


def test_spectral_kurtosis_flags_cw_tone():
    rng = np.random.default_rng(3)
    volt = rng.normal(size=(4000, 4)) + 1j * rng.normal(size=(4000, 4))
    power = np.abs(volt) ** 2
    # add a steady CW interferer to channel 2 -> power more constant -> SK < 1
    power[:, 2] += 50.0
    mask = rfi.flag_by_kurtosis(power, axis=0)
    assert mask[2]
    assert not mask[0]
