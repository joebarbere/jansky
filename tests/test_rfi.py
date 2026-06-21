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


def test_sumthreshold_low_false_positive_on_noise():
    rng = np.random.default_rng(7)
    noise = rng.normal(0.0, 1.0, 2000)
    mask = rfi.sumthreshold(noise, threshold=3.5)
    assert mask.mean() < 0.02  # very few false flags on clean noise


def test_sumthreshold_catches_extended_faint_burst():
    """A faint but extended bump (each sample below the single-sample cut) is
    caught by SumThreshold's window accumulation, where flag_outliers misses it."""
    rng = np.random.default_rng(8)
    series = rng.normal(0.0, 1.0, 512)
    series[200:208] += 2.8  # width-8 bump at +2.8 sigma each (< 3.5 single-sample cut)
    single = rfi.flag_outliers(series, threshold=3.5)
    st = rfi.sumthreshold(series, threshold=3.5, max_window=8)
    # The single-sample cut catches few of the bump samples; SumThreshold's window
    # accumulation catches most -- the whole point of the algorithm.
    assert single[200:208].sum() <= 3
    assert st[200:208].sum() >= 6
    assert st[200:208].sum() > single[200:208].sum()


def test_sumthreshold2d_flags_line_and_burst():
    rng = np.random.default_rng(9)
    ds = rng.normal(0.0, 1.0, (64, 32))
    ds[:, 10] += 6.0  # narrowband persistent line (a bright channel)
    ds[30, :] += 6.0  # broadband zero-DM burst (a bright time sample)
    mask = rfi.sumthreshold2d(ds, threshold=3.5)
    assert mask[:, 10].mean() > 0.8  # the line channel is largely flagged
    assert mask[30, :].mean() > 0.8  # the burst row is largely flagged
    # Clean pixels are mostly left alone.
    clean = mask.copy()
    clean[:, 10] = False
    clean[30, :] = False
    assert clean.mean() < 0.05


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
