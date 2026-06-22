"""Tests for jansky.synchrotron -- the non-thermal radio continuum helpers."""

from __future__ import annotations

import numpy as np

from jansky import synchrotron as syn


def test_spectral_index_electron_index_roundtrip():
    # N(E) ∝ E^-p radiates S ∝ ν^α with α = -(p-1)/2.
    assert np.isclose(syn.spectral_index(2.5), -0.75)
    assert np.isclose(syn.spectral_index(2.0), -0.5)
    assert np.isclose(syn.spectral_index(3.0), -1.0)
    p = np.array([2.0, 2.4, 3.0, 3.4])
    assert np.allclose(syn.electron_index(syn.spectral_index(p)), p)


def test_synchrotron_spectrum_thin_powerlaw():
    nu = np.geomspace(0.1, 100.0, 200)
    s = syn.synchrotron_spectrum(nu, s_ref=2.0, alpha=-0.7, nu_ref=1.0)
    # Matches the reference flux at nu_ref and follows the power-law slope.
    assert np.isclose(syn.synchrotron_spectrum(np.array([1.0]), 2.0, -0.7)[0], 2.0)
    slope = np.polyfit(np.log10(nu), np.log10(s), 1)[0]
    assert np.isclose(slope, -0.7, atol=1e-6)


def test_synchrotron_self_absorption_turnover():
    nu = np.geomspace(0.01, 100.0, 600)
    nu_ssa = 1.0
    s = syn.synchrotron_spectrum(nu, s_ref=2.0, alpha=-0.7, nu_ref=10.0, nu_ssa=nu_ssa)
    # The spectrum peaks near the turnover, not at the edges.
    nu_peak = nu[s.argmax()]
    assert 0.3 < nu_peak < 3.0
    # Optically-thick branch (well below turnover) approaches the universal 5/2 slope.
    lo = nu < 0.05
    slope_lo = np.polyfit(np.log10(nu[lo]), np.log10(s[lo]), 1)[0]
    assert np.isclose(slope_lo, 2.5, atol=0.1)
    # Optically-thin branch (well above) recovers alpha and the bare power law.
    hi = nu > 30.0
    slope_hi = np.polyfit(np.log10(nu[hi]), np.log10(s[hi]), 1)[0]
    assert np.isclose(slope_hi, -0.7, atol=0.05)
    thin = syn.synchrotron_spectrum(nu[hi], 2.0, -0.7, nu_ref=10.0)
    assert np.allclose(s[hi], thin, rtol=1e-3)


def test_aged_spectrum_steepens_above_break():
    nu = np.geomspace(0.1, 100.0, 400)
    s = syn.aged_spectrum(nu, s_ref=1.0, alpha=-0.6, nu_ref=0.1, nu_break=5.0)
    below = nu < 2.0
    above = nu > 20.0
    slope_below = np.polyfit(np.log10(nu[below]), np.log10(s[below]), 1)[0]
    slope_above = np.polyfit(np.log10(nu[above]), np.log10(s[above]), 1)[0]
    assert np.isclose(slope_below, -0.6, atol=1e-6)
    assert np.isclose(slope_above, -1.1, atol=1e-6)  # steepened by delta=0.5


def test_spectral_age_scaling_and_value():
    # A lower break frequency means an older source (t ∝ nu_break^-1/2).
    t1 = syn.spectral_age(1.0, b_field_ug=10.0)
    t2 = syn.spectral_age(0.25, b_field_ug=10.0)
    assert np.isclose(t2 / t1, 2.0, rtol=1e-6)  # 1/sqrt(0.25) = 2
    # Order-of-magnitude sanity: ~tens of Myr for a 10 µG source breaking at 1 GHz.
    assert 10.0 < t1 < 100.0
    # Loss rate minimised (oldest age) at B = B_CMB / sqrt(3).
    bcmb = syn.b_cmb(0.0)
    fields = np.linspace(0.5, 12.0, 400)
    ages = np.array([syn.spectral_age(1.0, b) for b in fields])
    assert np.isclose(fields[ages.argmax()], bcmb / np.sqrt(3), atol=0.1)


def test_equipartition_field_scaling_and_ballpark():
    # 2/7 scaling in luminosity and volume.
    b1 = syn.equipartition_field(1e45, 3e69)
    b2 = syn.equipartition_field(1e46, 3e69)
    assert np.isclose(np.log(b2 / b1) / np.log(10.0), 2.0 / 7.0, rtol=1e-6)
    b3 = syn.equipartition_field(1e45, 3e70)
    assert np.isclose(np.log(b3 / b1) / np.log(10.0), -2.0 / 7.0, rtol=1e-6)
    # Cygnus A-scale source -> a few × 10 µG (1 µG = 1e-6 G).
    b_cyga_ug = syn.equipartition_field(2e45, 3e69) / 1e-6
    assert 10.0 < b_cyga_ug < 100.0


def test_brightness_temperature_limit():
    assert syn.brightness_temperature_limit() == syn.T_B_LIMIT_K == 1.0e12
