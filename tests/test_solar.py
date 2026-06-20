"""Tests for jansky.solar -- coronal density and type II burst drift."""

from __future__ import annotations

import numpy as np

from jansky import solar


def test_plasma_frequency_roundtrip():
    n_e = np.array([1e6, 1e7, 1e8])
    f = solar.plasma_frequency(n_e)
    back = solar.density_from_plasma_frequency(f)
    assert np.allclose(back, n_e, rtol=1e-10)
    # 1e8 cm^-3 -> ~90 MHz
    assert np.isclose(solar.plasma_frequency(1e8), 89.77, rtol=1e-2)


def test_newkirk_inverse():
    r = np.array([1.5, 2.0, 3.0])
    n_e = solar.newkirk_density(r)
    assert np.allclose(solar.newkirk_radius(n_e), r, rtol=1e-10)
    # density falls with height
    assert n_e[0] > n_e[1] > n_e[2]


def test_type_ii_drifts_downward():
    t, f = solar.type_ii_track(1000.0, r_start=1.5, duration_s=600)
    # frequency decreases with time as the shock climbs
    assert f[0] > f[-1]
    assert np.all(np.diff(f) < 0)


def test_shock_speed_recovered():
    true_speed = 1200.0  # km/s
    t, f = solar.type_ii_track(true_speed, r_start=1.5, duration_s=500, harmonic=2)
    recovered = solar.shock_speed_from_track(t, f, harmonic=2)
    assert np.isclose(recovered, true_speed, rtol=1e-6)
