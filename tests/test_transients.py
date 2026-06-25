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
        n_time=512,
        freqs_mhz=freqs,
        dm=true_dm,
        dt=dt,
        t0_index=50,
        amplitude=8.0,
        seed=1,
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


def test_fold_profile_stacks_pulse_in_one_bin():
    # A narrow periodic pulse should land (mostly) in a single phase bin when folded
    # at its true period.
    period = 7.0
    t = np.arange(0, 700.0, 0.5)
    phase = (t / period) % 1.0
    values = np.exp(
        -0.5 * ((phase - 0.3) / 0.05) ** 2
    )  # pulse at phase 0.3 (wide enough to sample)
    centres, profile, counts = transients.fold_profile(t, values, period, n_bins=20)
    assert centres.shape == profile.shape == counts.shape == (20,)
    assert counts.sum() == t.size  # every sample is binned
    # Empty bins (regular sampling commensurate with the period) come back as NaN.
    assert np.isnan(profile[counts == 0]).all()
    assert np.isclose(centres[np.nanargmax(profile)], 0.3, atol=0.05)


def test_epoch_folding_search_recovers_period():
    rng = np.random.default_rng(0)
    p_true = 53.0  # s (an LPT-like minutes-scale period in miniature)
    t = np.arange(0, 6000.0, 1.0)
    signal = (((t / p_true) % 1.0) < 0.08).astype(float) * 6.0  # 8%-duty boxcar
    values = signal + rng.normal(0, 1.0, t.size)
    periods = np.linspace(40.0, 70.0, 1200)
    res = transients.epoch_folding_search(t, values, periods, n_bins=25)
    assert res.stat.shape == periods.shape
    assert abs(res.best_period - p_true) < 0.3
    # The folding statistic peaks far above the off-period baseline.
    off = res.stat[np.abs(periods - p_true) > 2.0]
    assert res.best_stat > 8 * np.median(off)


def test_surface_bfield_and_characteristic_age():
    # Canonical 1 s pulsar with Pdot = 1e-15 -> B ~ 1e12 G, tau_c ~ 16 Myr.
    b = transients.surface_bfield(1.0, 1e-15)
    assert 0.9e12 < b < 1.1e12
    tau_s = transients.characteristic_age(1.0, 1e-15)
    assert np.isclose(tau_s, 5e14, rtol=1e-6)  # 1/(2e-15) s
    assert np.isclose(tau_s / (3.15576e7 * 1e6), 15.8, rtol=0.02)  # ~15.8 Myr
    # Magnetar-scale field for a slow, fast-spinning-down star.
    assert transients.surface_bfield(5.0, 1e-11) > 1e14


def test_death_line_slope_and_lpt_is_far_below():
    # Slope-3 line anchored near (1 s, 1e-16).
    assert np.isclose(transients.death_line_pdot(1.0), 1e-16, rtol=1e-6)
    assert np.isclose(
        transients.death_line_pdot(10.0) / transients.death_line_pdot(1.0), 1000.0, rtol=1e-6
    )
    # A long-period transient (P ~ 1 h) would need an absurd Pdot (~5e-6, vs <1e-10 for any
    # real compact object) to sit above the death line as a rotation-powered pulsar.
    assert transients.death_line_pdot(3600.0) > 1e-6
