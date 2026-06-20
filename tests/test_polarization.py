"""Tests for jansky.polarization -- Stokes, Faraday rotation, and RM synthesis."""

from __future__ import annotations

import numpy as np

from jansky import polarization as pol


def test_stokes_linear_roundtrip():
    """Q/U built from (p, chi) invert back to the same fraction and angle."""
    intensity, frac, chi = 2.0, 0.4, 0.7
    q, u = pol.stokes_linear(intensity, frac, chi)
    assert np.isclose(pol.linear_polarization_fraction(intensity, q, u), frac)
    # chi is pi-periodic; compare modulo pi.
    recovered = pol.polarization_angle(q, u)
    assert np.isclose((recovered - chi) % np.pi, 0.0, atol=1e-9) or np.isclose(
        (recovered - chi) % np.pi, np.pi, atol=1e-9
    )


def test_fully_polarized_has_unit_fraction():
    q, u = pol.stokes_linear(1.0, 1.0, 0.0)
    assert np.isclose(pol.linear_polarization_fraction(1.0, q, u), 1.0)
    assert np.isclose(q, 1.0) and np.isclose(u, 0.0)


def test_faraday_rotate_lambda_squared():
    """Angle rotates by RM * lambda^2; doubling lambda quadruples the rotation."""
    rm = 30.0
    d1 = pol.faraday_rotate(0.0, rm, 0.2) - 0.0
    d2 = pol.faraday_rotate(0.0, rm, 0.4) - 0.0
    assert np.isclose(d2 / d1, 4.0)
    assert np.isclose(d1, rm * 0.2**2)


def _polarized_spectrum(rm, chi0, freqs_hz):
    c = 299792458.0
    lam = c / np.asarray(freqs_hz)
    chi = pol.faraday_rotate(chi0, rm, lam)
    q, u = pol.stokes_linear(1.0, 0.7, chi)
    return lam, pol.complex_polarization(q, u)


def test_rotation_measure_fit_recovers_injected_rm():
    freqs = np.linspace(700e6, 1800e6, 200)
    rm_true, chi0 = 45.0, 0.3
    lam, _ = _polarized_spectrum(rm_true, chi0, freqs)
    chi = pol.faraday_rotate(chi0, rm_true, lam)
    rm_fit, chi0_fit = pol.rotation_measure_fit(lam, chi)
    assert np.isclose(rm_fit, rm_true, rtol=1e-6)
    assert np.isclose(chi0_fit % np.pi, chi0 % np.pi, atol=1e-6)


def test_rm_synthesis_peaks_at_injected_rm():
    freqs = np.linspace(700e6, 1800e6, 256)
    rm_true = 50.0
    lam, p = _polarized_spectrum(rm_true, 0.3, freqs)
    phi = np.linspace(-200.0, 200.0, 2001)
    f = pol.rm_synthesis(lam, p, phi)
    peak = phi[np.argmax(np.abs(f))]
    assert np.isclose(peak, rm_true, atol=1.0)
    # The recovered peak amplitude approaches the input polarised fraction (0.7).
    assert np.isclose(np.abs(f).max(), 0.7, atol=0.05)


def test_rmsf_is_peaked_and_normalized_at_zero():
    freqs = np.linspace(700e6, 1800e6, 256)
    lam = 299792458.0 / freqs
    phi = np.linspace(-200.0, 200.0, 2001)
    r = pol.rmsf(lam, phi)
    # The RMSF is normalised to 1 at phi = 0 and peaks there.
    assert np.isclose(np.abs(r[np.argmin(np.abs(phi))]), 1.0, atol=1e-6)
    assert np.argmax(np.abs(r)) == np.argmin(np.abs(phi))
