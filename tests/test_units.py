"""Tests for jansky.units -- the radio-astronomy unit conversions."""

from __future__ import annotations

import astropy.units as u
import numpy as np
import pytest

from jansky import units


def test_jansky_si_value():
    """1 Jy is exactly 1e-26 W / m^2 / Hz."""
    one_jy = (1 * u.Jy).to(u.W / u.m**2 / u.Hz)
    assert np.isclose(one_jy.value, 1e-26)


def test_to_jansky_roundtrip():
    flux = 3e-26 * u.W / u.m**2 / u.Hz
    assert np.isclose(units.to_jansky(flux).to_value(u.Jy), 3.0)


def test_brightness_temperature_roundtrip():
    """flux <-> brightness temperature must invert exactly."""
    t_in = 120.0 * u.K
    freq = 1.42 * u.GHz
    omega = 1e-6 * u.sr
    flux = units.brightness_temperature_to_flux(t_in, freq, omega)
    t_out = units.flux_to_brightness_temperature(flux, freq, omega)
    assert np.isclose(t_out.to_value(u.K), t_in.to_value(u.K))


def test_rayleigh_jeans_scaling():
    """RJ brightness scales as nu^2 at fixed temperature."""
    t = 50 * u.K
    b1 = units.rayleigh_jeans_brightness(t, 1 * u.GHz)
    b2 = units.rayleigh_jeans_brightness(t, 2 * u.GHz)
    assert np.isclose((b2 / b1).to_value(u.dimensionless_unscaled), 4.0)


def test_decibel_roundtrip():
    for ratio in (1.0, 2.0, 10.0, 1000.0):
        assert np.isclose(units.from_decibels(units.to_decibels(ratio)), ratio)


def test_decibel_known_values():
    assert np.isclose(units.to_decibels(10.0), 10.0)
    assert np.isclose(units.to_decibels(2.0), 3.0103, atol=1e-3)


@pytest.mark.parametrize("freq", [0.4 * u.GHz, 1.4 * u.GHz, 5 * u.GHz])
def test_flux_positive(freq):
    flux = units.brightness_temperature_to_flux(100 * u.K, freq, 1e-7 * u.sr)
    assert flux.to_value(u.Jy) > 0


def test_planck_reduces_to_rayleigh_jeans_in_radio():
    # At radio frequencies (h nu << k T) Planck ~= Rayleigh-Jeans.
    T = 100 * u.K
    nu = 1.4 * u.GHz
    planck = units.planck_brightness(T, nu)
    rj = units.rayleigh_jeans_brightness(T, nu)
    assert np.isclose(planck.value, rj.to_value(planck.unit), rtol=1e-3)


def test_planck_peaks_and_positive():
    # CMB blackbody is positive and the value near its peak (~160 GHz) exceeds
    # a low-frequency point of the same curve.
    T = 2.725 * u.K
    low = units.planck_brightness(T, 5 * u.GHz)
    peak = units.planck_brightness(T, 160 * u.GHz)
    assert low.value > 0 and peak.value > 0
    assert peak.value > low.value
