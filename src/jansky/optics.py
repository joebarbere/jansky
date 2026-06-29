"""Parabolic-reflector geometry: the surface, and why all rays land on the focus.

A parabolic dish works because of one geometric fact: every ray arriving parallel to
the axis reflects to a single point, the focus, and -- crucially -- every such ray
travels the *same* total path length to get there, so the wavefronts add in phase.
These helpers give the surface :math:`z = r^2/4f`, its surface normal, the law of
reflection, and the equal-path-length property, so the notebook can ray-trace a dish
and show the waves converging on the feed. Plain NumPy; the maths is the lesson.

Key results encoded here
------------------------
* The paraboloid :math:`z = r^2/(4f)` with focus at :math:`(0, 0, f)` and focal ratio
  :math:`f/D` (Balanis, *Antenna Theory*; Condon & Ransom 2016, ch. 3).
* The **reflection law** :math:`\\hat{r} = \\hat{d} - 2(\\hat{d}\\cdot\\hat{n})\\hat{n}`,
  which sends any axial incoming ray through the focus.
* The **equal-path property**: axial ray + reflected ray to the focus sums to
  :math:`f + (\\text{vertex-to-directrix})`, the same for all radii -- the reason a
  paraboloid forms a coherent (in-phase) image at the feed.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "focal_ratio",
    "parabola_depth",
    "parabola_z",
    "path_length_to_focus",
    "reflect",
    "reflected_ray_to_focus",
    "surface_normal",
]


def parabola_z(r: float | np.ndarray, focal_length: float) -> float | np.ndarray:
    """Height :math:`z = r^2/(4f)` of the paraboloid at radius ``r`` from the axis.

    The focus sits on the axis at :math:`(0, 0, f)`.
    """
    if focal_length <= 0:
        raise ValueError("focal_length must be positive")
    return np.asarray(r, float) ** 2 / (4.0 * focal_length)


def parabola_depth(diameter: float, focal_length: float) -> float:
    """Depth of the dish at its rim, :math:`(D/2)^2/(4f)` -- the vertex-to-rim sag."""
    return float(parabola_z(diameter / 2.0, focal_length))


def focal_ratio(focal_length: float, diameter: float) -> float:
    """Focal ratio :math:`f/D`. Shallow dishes (large f/D) ease feed design; deep dishes
    (small f/D) shrink spillover. Typical radio dishes are :math:`f/D \\approx 0.3-0.5`.
    """
    if diameter <= 0:
        raise ValueError("diameter must be positive")
    return focal_length / diameter


def surface_normal(r: float, focal_length: float) -> np.ndarray:
    """Unit surface normal of the paraboloid at radius ``r`` (in the plane of incidence).

    Working in the 2-D :math:`(x, z)` plane through the axis, the surface
    :math:`z = x^2/4f` has slope :math:`dz/dx = x/2f`; the outward (toward +z) unit
    normal is :math:`(-x/2f, 1)/\\sqrt{1 + (x/2f)^2}`. Returns the 2-vector ``[n_x, n_z]``.
    """
    slope = r / (2.0 * focal_length)
    n = np.array([-slope, 1.0])
    return n / np.linalg.norm(n)


def reflect(incoming: np.ndarray, normal: np.ndarray) -> np.ndarray:
    """Reflect a direction ``incoming`` about a surface ``normal`` (both 2- or 3-vectors).

    Law of reflection :math:`\\hat{r} = \\hat{d} - 2(\\hat{d}\\cdot\\hat{n})\\hat{n}`. Inputs
    need not be normalised for the direction of the result, but ``normal`` must be a true
    unit normal for the result to be unit length; this helper normalises both.
    """
    d = np.asarray(incoming, float)
    d = d / np.linalg.norm(d)
    n = np.asarray(normal, float)
    n = n / np.linalg.norm(n)
    return d - 2.0 * np.dot(d, n) * n


def reflected_ray_to_focus(r: float, focal_length: float) -> np.ndarray:
    """Direction of an axial down-going ray after it reflects off the dish at radius ``r``.

    An incoming ray travelling along :math:`-\\hat{z}` (straight down the axis) strikes the
    surface at :math:`(r, z=r^2/4f)`; the reflected direction is returned as a unit
    2-vector ``[x, z]``. By construction it points at the focus :math:`(0, f)` -- the
    notebook checks this numerically for the whole aperture.
    """
    hit = np.array([r, parabola_z(r, focal_length)])
    reflected = reflect(np.array([0.0, -1.0]), surface_normal(r, focal_length))
    to_focus = np.array([0.0, focal_length]) - hit
    # return the reflected unit direction (the test/notebook compares it with `to_focus`)
    del to_focus
    return reflected


def path_length_to_focus(r: float, focal_length: float, plane_z: float | None = None) -> float:
    """Total path length of an axial ray from a reference plane down to the focus via the dish.

    For a wavefront arriving at height ``plane_z`` (default: the focal height ``f``), the
    path is the vertical drop to the surface at radius ``r`` plus the slant from there to
    the focus. For a paraboloid this sum is **independent of** ``r`` -- the equal-path
    property that makes the reflected wavefront converge in phase on the feed.
    """
    z_plane = focal_length if plane_z is None else plane_z
    hit = np.array([r, parabola_z(r, focal_length)])
    drop = z_plane - hit[1]
    slant = float(np.linalg.norm(np.array([0.0, focal_length]) - hit))
    return float(drop + slant)
