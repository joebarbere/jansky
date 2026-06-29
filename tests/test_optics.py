"""Tests for jansky.optics -- parabolic-reflector geometry and ray reflection."""

from __future__ import annotations

import numpy as np
import pytest

from jansky import optics


def test_parabola_surface():
    assert optics.parabola_z(0.0, 5.0) == 0.0
    assert abs(optics.parabola_z(10.0, 5.0) - 100.0 / 20.0) < 1e-12  # r^2/4f


def test_focal_ratio_and_depth():
    assert abs(optics.focal_ratio(7.5, 25.0) - 0.3) < 1e-12
    assert abs(optics.parabola_depth(25.0, 7.5) - (12.5**2) / (4 * 7.5)) < 1e-9


def test_surface_normal_is_unit_and_axial_at_vertex():
    n = optics.surface_normal(0.0, 5.0)
    assert np.allclose(n, [0.0, 1.0])
    n2 = optics.surface_normal(8.0, 5.0)
    assert abs(np.linalg.norm(n2) - 1.0) < 1e-12


def test_axial_ray_reflects_through_focus():
    """The defining property: every down-going axial ray reflects toward the focus."""
    f = 6.0
    for r in [0.5, 2.0, 5.0, 9.0]:
        reflected = optics.reflected_ray_to_focus(r, f)
        hit = np.array([r, optics.parabola_z(r, f)])
        to_focus = np.array([0.0, f]) - hit
        to_focus /= np.linalg.norm(to_focus)
        assert np.dot(reflected, to_focus) > 1.0 - 1e-9  # parallel: aims at the focus


def test_reflect_law_basic():
    # a ray going down reflecting off a horizontal surface goes back up
    out = optics.reflect([0.0, -1.0], [0.0, 1.0])
    assert np.allclose(out, [0.0, 1.0])


def test_equal_path_length_property():
    """All axial rays travel the same total path to the focus (2f from the focal plane)."""
    f = 6.0
    paths = [optics.path_length_to_focus(r, f) for r in [0.0, 3.0, 7.0, 11.0]]
    assert np.allclose(paths, 2.0 * f, atol=1e-9)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        optics.parabola_z(1.0, 0.0)
    with pytest.raises(ValueError):
        optics.focal_ratio(5.0, 0.0)
