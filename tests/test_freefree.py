"""Tests for jansky.freefree -- the thermal (free-free) continuum helpers."""

from __future__ import annotations

import numpy as np

from jansky import freefree as ff


def test_optical_depth_frequency_scaling():
    # tau_ff ∝ nu^-2.1.
    nu = np.geomspace(0.1, 10.0, 200)
    tau = ff.freefree_optical_depth(nu, em=1.0e6)
    slope = np.polyfit(np.log10(nu), np.log10(tau), 1)[0]
    assert np.isclose(slope, -2.1, atol=1e-6)
    # tau is linear in EM.
    assert np.isclose(
        ff.freefree_optical_depth(1.0, 2.0e6), 2.0 * ff.freefree_optical_depth(1.0, 1.0e6)
    )


def test_optical_depth_temperature_scaling():
    # tau_ff ∝ T_e^-1.35; the 1e4 K normalisation reproduces the standard coefficient.
    tau_1e4 = ff.freefree_optical_depth(1.0, em=1.0e6, t_e=1.0e4)
    assert np.isclose(tau_1e4, ff.TAU_COEFF * 1.0e6, rtol=1e-9)
    tau_2e4 = ff.freefree_optical_depth(1.0, em=1.0e6, t_e=2.0e4)
    assert np.isclose(tau_2e4 / tau_1e4, 2.0**-1.35, rtol=1e-9)


def test_brightness_temperature_thick_and_thin_limits():
    t_e = 9000.0
    em = 1.0e7
    # Deep in the optically-thick regime T_B -> T_e.
    t_b_thick = ff.freefree_brightness_temperature(0.01, em, t_e)
    assert np.isclose(t_b_thick, t_e, rtol=1e-3)
    # Optically thin: T_B ≈ T_e * tau ∝ nu^-2.1.
    nu_hi = np.geomspace(20.0, 200.0, 100)
    t_b_thin = ff.freefree_brightness_temperature(nu_hi, em, t_e)
    slope = np.polyfit(np.log10(nu_hi), np.log10(t_b_thin), 1)[0]
    assert np.isclose(slope, -2.1, atol=0.02)


def test_spectrum_thick_nu2_and_thin_flat_slopes():
    t_e = 1.0e4
    em = 5.0e6
    # Optically thick: S ∝ nu^2.
    nu_lo = np.geomspace(0.02, 0.1, 100)
    s_lo = ff.freefree_spectrum(nu_lo, em, t_e)
    slope_lo = np.polyfit(np.log10(nu_lo), np.log10(s_lo), 1)[0]
    assert np.isclose(slope_lo, 2.0, atol=0.05)
    # Optically thin: S ∝ nu^-0.1 (the flat thermal index).
    nu_hi = np.geomspace(30.0, 300.0, 100)
    s_hi = ff.freefree_spectrum(nu_hi, em, t_e)
    slope_hi = np.polyfit(np.log10(nu_hi), np.log10(s_hi), 1)[0]
    assert np.isclose(slope_hi, ff.ALPHA_THIN, atol=0.02)


def test_turnover_frequency_is_where_tau_is_one():
    em, t_e = 5.0e6, 1.0e4
    nu_turn = ff.turnover_frequency(em, t_e)
    assert np.isclose(ff.freefree_optical_depth(nu_turn, em, t_e), 1.0, rtol=1e-9)
    # Orion-scale EM turns over near ~1 GHz.
    assert 0.3 < nu_turn < 3.0


def test_emission_measure_uniform_slab():
    assert np.isclose(ff.emission_measure(100.0, 5.0), 100.0**2 * 5.0)


def test_stromgren_radius_scaling_and_ballpark():
    # R_s ∝ Q^1/3 and ∝ n_e^-2/3.
    r1 = ff.stromgren_radius(1.0e49, 1.0e3)
    r2 = ff.stromgren_radius(8.0e49, 1.0e3)
    assert np.isclose(r2 / r1, 2.0, rtol=1e-6)  # 8^(1/3) = 2
    r3 = ff.stromgren_radius(1.0e49, 4.0e3)
    assert np.isclose(r3 / r1, 4.0 ** (-2.0 / 3.0), rtol=1e-6)
    # O5 star in dense gas -> a few tenths of a parsec.
    assert 0.1 < r1 < 1.0
