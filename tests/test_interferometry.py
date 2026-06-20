"""Tests for jansky.interferometry -- uv-coverage, dirty beam, CLEAN."""

from __future__ import annotations

import numpy as np

from jansky import interferometry


def _toy_array():
    return np.array([[0, 0], [10, 0], [0, 12], [7, 7], [-9, 3]], dtype=float)


def test_uv_coverage_is_hermitian():
    """Every (u, v) sample has its conjugate (-u, -v)."""
    uv = interferometry.uv_coverage(_toy_array())
    # Sum of all points should cancel to zero by conjugate symmetry.
    assert np.allclose(uv.sum(axis=0), 0.0)
    # n_baselines * 2 conjugates * n_hour_angles(=1) samples.
    n_ant = 5
    assert uv.shape == (n_ant * (n_ant - 1) // 2 * 2, 2)


def test_earth_rotation_increases_coverage():
    arr = _toy_array()
    snap = interferometry.uv_coverage(arr)
    track = interferometry.uv_coverage(arr, hour_angles=np.linspace(-1, 1, 30))
    assert track.shape[0] > snap.shape[0]


def test_dirty_beam_peaks_at_centre():
    uv = interferometry.uv_coverage(_toy_array(), np.linspace(-1, 1, 40))
    mask = interferometry.grid_visibilities(uv, npix=64)
    beam = interferometry.dirty_beam(mask)
    peak = np.unravel_index(np.argmax(beam), beam.shape)
    assert peak == (32, 32)
    assert np.isclose(beam[peak], 1.0)


def test_clean_recovers_point_source():
    """CLEAN should place its brightest component on the true source pixel."""
    npix = 64
    sky = np.zeros((npix, npix))
    sky[20, 40] = 1.0
    uv = interferometry.uv_coverage(_toy_array(), np.linspace(-1, 1, 40))
    mask = interferometry.grid_visibilities(uv, npix=npix)
    beam = interferometry.dirty_beam(mask)
    dirty = interferometry.dirty_image(sky, mask)
    result = interferometry.hogbom_clean(dirty, beam, gain=0.2, n_iter=300)
    recovered = np.unravel_index(np.argmax(result.model), result.model.shape)
    assert recovered == (20, 40)
    # Residual peak is much smaller than the original dirty-image peak.
    assert np.abs(result.residual).max() < 0.5 * np.abs(dirty).max()


def test_clean_threshold_stops_early():
    dirty = np.zeros((32, 32))
    dirty[16, 16] = 1.0
    beam = np.zeros((32, 32))
    beam[16, 16] = 1.0
    result = interferometry.hogbom_clean(dirty, beam, gain=0.5, n_iter=1000, threshold=0.1)
    # With a clean delta beam, geometric decay stops once peak < 0.1.
    assert np.abs(result.residual).max() <= 0.1


def test_coherent_calibration_recovers_offsets():
    import numpy as np
    lam = 1.0
    pos = np.arange(5) * 0.5
    offsets = np.array([0.0, 1.2, -0.7, 2.5, -1.9])
    cal = interferometry.simulate_coherent_channels(
        pos, 0.0, lam, snr=30, phase_offsets=offsets, seed=1
    )
    est = interferometry.calibrate_phases(cal)
    # wrap difference into (-pi, pi]; should be tiny at high SNR
    err = np.angle(np.exp(1j * (est - offsets)))
    assert np.max(np.abs(err)) < 0.02


def test_coherent_recovers_source_angle():
    import numpy as np
    lam = 1.0
    pos = np.arange(5) * 0.5
    offsets = np.array([0.0, 1.2, -0.7, 2.5, -1.9])
    true_angle = np.radians(18.0)
    cal = interferometry.simulate_coherent_channels(
        pos, 0.0, lam, snr=30, phase_offsets=offsets, seed=1
    )
    est = interferometry.calibrate_phases(cal)
    obs = interferometry.simulate_coherent_channels(
        pos, true_angle, lam, snr=30, phase_offsets=offsets, seed=2
    )
    corr = obs * np.exp(-1j * est)[:, None]
    angle = interferometry.estimate_source_angle(corr[1], corr[0], baseline=0.5, wavelength=lam)
    assert abs(np.degrees(angle) - 18.0) < 1.0


def test_fringe_phase_zero_on_boresight():
    import numpy as np
    assert interferometry.fringe_phase(2.0, 0.0, 0.21) == 0.0
    # and matches 2*pi*b*sin(theta)/lambda
    val = interferometry.fringe_phase(2.0, np.radians(30), 0.21)
    assert np.isclose(val, 2 * np.pi * 2.0 * 0.5 / 0.21)
