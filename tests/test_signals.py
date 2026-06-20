"""Tests for jansky.signals -- noise, the radiometer equation, beams."""

from __future__ import annotations

import numpy as np
import pytest
from scipy.optimize import curve_fit

from jansky import signals


def test_radiometer_sqrt_scaling():
    """Sensitivity improves as sqrt(B*t): 4x time -> 2x better."""
    s1 = signals.radiometer_sensitivity(50.0, 1e6, 1.0)
    s4 = signals.radiometer_sensitivity(50.0, 1e6, 4.0)
    assert np.isclose(s1 / s4, 2.0)


def test_radiometer_polarisation_gain():
    """Averaging two polarisations improves sensitivity by sqrt(2)."""
    s1 = signals.radiometer_sensitivity(50.0, 1e6, 1.0, n_pol=1)
    s2 = signals.radiometer_sensitivity(50.0, 1e6, 1.0, n_pol=2)
    assert np.isclose(s1 / s2, np.sqrt(2.0))


def test_radiometer_accepts_arrays():
    """The vectorised path (used by integrate_noise) must work."""
    times = np.array([1.0, 4.0, 16.0])
    out = signals.radiometer_sensitivity(50.0, 1e6, times)
    assert out.shape == times.shape
    assert np.isclose(out[0] / out[2], 4.0)


def test_radiometer_rejects_nonpositive():
    with pytest.raises(ValueError):
        signals.radiometer_sensitivity(50.0, 0.0, 1.0)
    with pytest.raises(ValueError):
        signals.radiometer_sensitivity(50.0, 1e6, -1.0)


def test_integrate_noise_converges():
    """The running estimate ends near the true signal and within the envelope."""
    res = signals.integrate_noise(
        t_sys=30.0, bandwidth=1e6, total_time=100.0, signal=0.05, n_samples=2000, seed=1
    )
    assert abs(res.estimate[-1] - 0.05) < 3 * res.expected_sigma[-1]
    # Envelope shrinks monotonically with time.
    assert res.expected_sigma[0] > res.expected_sigma[-1]


def test_recover_spectral_index():
    """A power-law spectrum's index is recoverable by fitting."""
    freq = np.linspace(0.1, 10.0, 200)
    true_alpha = -0.7
    flux = signals.power_law(freq, amplitude=5.0, spectral_index=true_alpha)

    def model(nu, amp, alpha):
        return signals.power_law(nu, amp, alpha)

    popt, _ = curve_fit(model, freq, flux, p0=[1.0, -1.0])
    assert np.isclose(popt[1], true_alpha, atol=1e-6)


def test_gaussian_beam_peak_and_fwhm():
    assert np.isclose(signals.gaussian_beam(0.0, fwhm=1.0), 1.0)
    # At the half-maximum point the response is 0.5.
    assert np.isclose(signals.gaussian_beam(0.5, fwhm=1.0), 0.5)


def test_airy_beam_first_null():
    """The Airy power pattern hits its first null near sin(theta)=1.22 lambda/D."""
    diameter, wavelength = 25.0, 0.21
    theta_null = np.arcsin(1.2197 * wavelength / diameter)
    val = signals.airy_beam(theta_null, diameter, wavelength)
    assert val < 1e-4
    # Peak on boresight is 1.
    assert np.isclose(signals.airy_beam(0.0, diameter, wavelength), 1.0)
