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
