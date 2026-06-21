"""Tests for jansky.lightning -- sferics, tweeks, whistlers, and TOA geolocation."""

from __future__ import annotations

import numpy as np

from jansky import lightning


def test_return_stroke_field_is_normalised_and_broadband():
    t, field = lightning.return_stroke_field(n=4096, dt=1e-6)
    assert t.shape == field.shape == (4096,)
    # Normalised to unit peak amplitude.
    assert np.isclose(np.max(np.abs(field)), 1.0)
    # Bipolar: the field changes sign (a fast transient, not a DC step).
    assert field.min() < 0 < field.max()
    # Spectrum has real low-frequency content and rolls off at high frequency.
    spec = np.abs(np.fft.rfft(field))
    freqs = np.fft.rfftfreq(field.size, d=1e-6)
    lf = spec[(freqs > 1e3) & (freqs < 1e4)].mean()
    hf = spec[(freqs > 1e5) & (freqs < 5e5)].mean()
    assert lf > hf


def test_return_stroke_field_rejects_bad_taus():
    import pytest

    with pytest.raises(ValueError):
        lightning.return_stroke_field(tau_rise=50e-6, tau_fall=2e-6)


def test_whistler_group_delay_scales_as_inverse_sqrt_f():
    d = 80.0
    # Halving frequency multiplies the delay by sqrt(2).
    t_hi = lightning.whistler_group_delay(d, 8000.0)
    t_lo = lightning.whistler_group_delay(d, 4000.0)
    assert np.isclose(t_lo / t_hi, np.sqrt(2.0))
    # Lower frequencies always arrive later.
    f = np.array([2000.0, 4000.0, 8000.0])
    delays = lightning.whistler_group_delay(d, f)
    assert np.all(np.diff(delays) < 0)


def test_tweek_group_delay_diverges_at_cutoff_and_nan_below():
    fc = lightning.TWEEK_CUTOFF_HZ
    near = lightning.tweek_group_delay(fc * 1.001, distance_km=3000.0)
    far = lightning.tweek_group_delay(fc * 5.0, distance_km=3000.0)
    # Just above cutoff the delay is much larger than well above it.
    assert near > 5.0 * far
    # Below cutoff: no propagation.
    assert np.isnan(lightning.tweek_group_delay(fc * 0.5, distance_km=3000.0))
    # Very far above cutoff the delay approaches the free-path light-time L/c.
    asymptote = lightning.tweek_group_delay(fc * 100.0, distance_km=3000.0)
    assert np.isclose(asymptote, 3000.0 / lightning.C_KM_S, rtol=1e-3)


def test_whistler_dedispersion_realigns_the_pulse():
    freqs = np.linspace(800.0, 10000.0, 200)
    dt = 2e-3
    n_time = 2000  # 4.0 s window: long enough for the D=80 low-frequency tail
    disp = 80.0
    dynspec = lightning.synthesize_whistler(
        freqs, n_time=n_time, dt=dt, dispersion=disp, t0=0.05, noise=0.0, seed=1
    )
    # Before de-dispersion the per-channel peak times span a wide range (the glide).
    raw_peaks = dynspec.argmax(axis=1)
    assert np.ptp(raw_peaks) > 50
    # After de-dispersion the peaks line up to within a couple of samples.
    aligned = lightning.dedisperse_whistler(dynspec, freqs, dt=dt, dispersion=disp)
    peaks = aligned.argmax(axis=1)
    assert np.ptp(peaks) <= 3
    # Summing over frequency gives a single sharp impulse: de-dispersed S/N beats raw.
    summed = aligned.sum(axis=0)
    raw_sum = dynspec.sum(axis=0)
    assert summed.max() > 1.5 * raw_sum.max()


def test_geolocation_recovers_a_known_stroke():
    stations = np.array([[0.0, 0.0], [400.0, 0.0], [0.0, 400.0], [400.0, 400.0]])
    truth = (150.0, 220.0)
    times = lightning.simulate_arrival_times(truth, stations, t0=0.0, noise_us=1.0, seed=3)
    fix = lightning.geolocate_toa(stations, times)
    # With ~1 µs timing (~0.3 km), recover the position to a few km.
    assert np.hypot(fix.x - truth[0], fix.y - truth[1]) < 5.0
    assert fix.residual_rms_us < 5.0


def test_geolocation_needs_three_stations():
    import pytest

    with pytest.raises(ValueError):
        lightning.geolocate_toa(np.array([[0.0, 0.0], [1.0, 0.0]]), np.array([0.0, 1e-3]))


def test_geolocation_improves_with_lower_timing_noise():
    stations = np.array([[0.0, 0.0], [500.0, 0.0], [0.0, 500.0], [500.0, 500.0], [250.0, 600.0]])
    truth = (180.0, 240.0)
    err = {}
    for noise_us in (10.0, 0.5):
        times = lightning.simulate_arrival_times(truth, stations, noise_us=noise_us, seed=7)
        fix = lightning.geolocate_toa(stations, times)
        err[noise_us] = np.hypot(fix.x - truth[0], fix.y - truth[1])
    assert err[0.5] < err[10.0]
