"""Tests for jansky.transients -- dispersion, de-dispersion, DM search."""

from __future__ import annotations

import numpy as np

from jansky import transients


def test_dispersion_delay_law():
    # Lower frequency arrives later; matches k_DM * DM * (f_lo^-2 - f_hi^-2).
    d = transients.dispersion_delay(100.0, 400.0, 800.0)
    expected = transients.DM_CONST * 100.0 * (400.0**-2 - 800.0**-2)
    assert np.isclose(d, expected)
    assert d > 0
    # zero across equal frequencies
    assert transients.dispersion_delay(100.0, 600.0, 600.0) == 0.0


def test_dm_search_recovers_true_dm():
    freqs = np.linspace(400.0, 800.0, 64)  # MHz
    dt = 1e-3  # s
    true_dm = 150.0
    dynspec = transients.disperse_pulse(
        n_time=512, freqs_mhz=freqs, dm=true_dm, dt=dt,
        t0_index=50, amplitude=8.0, seed=1,
    )
    trials = np.arange(0, 300, 5.0)
    result = transients.dm_search(dynspec, freqs, dt, trials)
    # best trial DM within one grid step of the truth
    assert abs(result.best_dm - true_dm) <= 5.0
    # S/N peaks at the true DM, much higher than at DM=0
    assert result.best_snr > result.snr[0]


def test_dedisperse_peaks_at_true_dm():
    freqs = np.linspace(1200.0, 1500.0, 32)
    dt = 5e-4
    dynspec = transients.disperse_pulse(
        n_time=400, freqs_mhz=freqs, dm=80.0, dt=dt, t0_index=40, amplitude=6.0, seed=2
    )
    good = transients.dedisperse(dynspec, freqs, 80.0, dt)
    bad = transients.dedisperse(dynspec, freqs, 0.0, dt)
    assert good.max() > bad.max()


def test_boxcar_snr_prefers_matched_width():
    rng = np.random.default_rng(3)
    series = rng.normal(0, 1, 1000)
    series[500:508] += 4.0  # an 8-sample top-hat
    snr, width, idx = transients.boxcar_snr(series, widths=[1, 2, 4, 8, 16, 32])
    assert width in (4, 8, 16)  # near the true width, not 1 or 32
    assert 495 <= idx <= 512
    assert snr > 5


def test_macquart_redshift_monotonic():
    assert transients.macquart_redshift(900.0) == 1.0
    assert transients.macquart_redshift(450.0) < transients.macquart_redshift(900.0)
