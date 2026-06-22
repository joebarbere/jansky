"""Tests for jansky.eor -- the redshifted 21 cm cosmic-dawn / EoR helpers."""

from __future__ import annotations

import numpy as np

from jansky import eor


def test_freq_redshift_roundtrip_and_anchors():
    # The line at z=0 is at its rest frequency.
    assert np.isclose(eor.redshift_to_freq(0.0), eor.NU_21_MHZ)
    # Cosmic-dawn trough (z~17) lands near 78 MHz; reionization end (z~6) near 200 MHz.
    assert np.isclose(eor.redshift_to_freq(17.0), 78.9, atol=0.5)
    assert np.isclose(eor.redshift_to_freq(6.0), 203.0, atol=1.0)
    # Round-trip.
    z = np.array([6.0, 10.0, 17.0, 27.0])
    assert np.allclose(eor.freq_to_redshift(eor.redshift_to_freq(z)), z)


def test_cmb_temperature_scales_with_redshift():
    assert np.isclose(eor.cmb_temperature(0.0), 2.725)
    assert np.isclose(eor.cmb_temperature(17.0), 2.725 * 18.0)


def test_brightness_sign_follows_spin_temperature():
    z = 17.0
    t_cmb = eor.cmb_temperature(z)
    # T_S < T_CMB -> absorption (negative); > -> emission (positive); = -> zero.
    assert eor.differential_brightness(z, spin_temp_k=5.0) < 0
    assert eor.differential_brightness(z, spin_temp_k=500.0) > 0
    assert np.isclose(eor.differential_brightness(z, spin_temp_k=t_cmb), 0.0, atol=1e-9)


def test_brightness_saturates_for_hot_gas():
    # As T_S -> infinity the (1 - T_CMB/T_S) factor -> 1; signal approaches a finite cap.
    z = 8.0
    hot = eor.differential_brightness(z, spin_temp_k=1e6)
    cap = 27.0 * np.sqrt((1.0 + z) / 10.0) * (0.0223 / 0.023) * np.sqrt(0.15 / 0.143)
    assert np.isclose(hot, cap, rtol=1e-3)
    # Ionized gas (x_HI=0) gives no signal regardless of spin temperature.
    assert eor.differential_brightness(z, spin_temp_k=1e6, x_hi=0.0) == 0.0


def test_global_signal_trough_shape():
    nu = np.linspace(50.0, 120.0, 701)
    sig = eor.global_signal(nu, center_mhz=78.0, depth_mk=-500.0, width_mhz=19.0)
    # Minimum at the centre, reaching the stated depth.
    assert np.isclose(nu[np.argmin(sig)], 78.0, atol=0.2)
    assert np.isclose(sig.min(), -500.0, atol=1.0)
    # The wings are shallower than half the trough depth (the signal rises out of it).
    assert sig[0] > 0.5 * sig.min()
    assert sig[-1] > 0.5 * sig.min()
    # A flatter profile has a broader bottom: more channels within 10% of the depth.
    flat = eor.global_signal(nu, center_mhz=78.0, depth_mk=-500.0, width_mhz=19.0, flatness=4.0)
    near_gauss = np.sum(sig < 0.9 * -500.0)
    near_flat = np.sum(flat < 0.9 * -500.0)
    assert near_flat > near_gauss


def test_remove_smooth_foreground_recovers_faint_signal():
    nu = np.linspace(100.0, 200.0, 1000)
    # Bright smooth synchrotron foreground (~300 K at 150 MHz, index -2.5).
    foreground = 300.0 * (nu / 150.0) ** -2.5
    # A faint, spectrally structured 21 cm-like signal (~20 mK = 0.02 K).
    signal = 0.02 * np.sin(2 * np.pi * (nu - 100.0) / 12.0)
    temps = foreground + signal
    residual, fg_fit = eor.remove_smooth_foreground(nu, temps, degree=5)
    # The smooth model captures the foreground to << its amplitude.
    assert np.max(np.abs(fg_fit - foreground)) < 0.05
    # The residual recovers the injected signal (strongly correlated, right amplitude).
    corr = np.corrcoef(residual, signal)[0, 1]
    assert corr > 0.9
    assert np.std(residual) < 0.05  # far below the ~hundreds-of-K foreground


def test_remove_smooth_foreground_rejects_nonpositive():
    import pytest

    nu = np.linspace(100.0, 200.0, 10)
    with pytest.raises(ValueError):
        eor.remove_smooth_foreground(nu, np.zeros_like(nu))
