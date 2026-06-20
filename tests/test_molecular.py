"""Tests for jansky.molecular -- CO ladder and Keplerian maser masses."""

from __future__ import annotations

import astropy.units as u
import numpy as np

from jansky import molecular


def test_co_ladder():
    assert np.isclose(molecular.co_line_frequency(1).to_value(u.GHz), 115.271202)
    assert np.isclose(molecular.co_line_frequency(2).to_value(u.GHz), 230.542404)
    assert np.isclose(molecular.co_line_frequency(3).to_value(u.GHz), 345.81, atol=0.01)


def test_keplerian_mass_roundtrip():
    mass = 4e7 * u.Msun
    radius = 0.2 * u.pc
    v = molecular.keplerian_velocity(mass, radius)
    recovered = molecular.maser_central_mass(radius, v)
    assert np.isclose(recovered.to_value(u.Msun), mass.to_value(u.Msun), rtol=1e-6)


def test_keplerian_velocity_scaling():
    # v ∝ r^-1/2 at fixed mass
    m = 1e7 * u.Msun
    v1 = molecular.keplerian_velocity(m, 0.1 * u.pc)
    v4 = molecular.keplerian_velocity(m, 0.4 * u.pc)
    assert np.isclose((v1 / v4).to_value(u.dimensionless_unscaled), 2.0, rtol=1e-6)


def test_maser_central_mass_array_mean():
    mass = 4.1e7 * u.Msun
    radii = np.array([0.13, 0.18, 0.25]) * u.pc
    vels = molecular.keplerian_velocity(mass, radii)
    recovered = molecular.maser_central_mass(radii, vels)
    assert np.isclose(recovered.to_value(u.Msun), mass.to_value(u.Msun), rtol=1e-6)
