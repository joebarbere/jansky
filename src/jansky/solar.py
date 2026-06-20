"""Solar (and planetary) radio bursts.

Low-frequency radio astronomy hears the Sun loudly. A **type II** burst is the
radio signature of a shock -- often driven by a coronal mass ejection -- ploughing
outward through the corona. The corona's electron density falls with height, so
the plasma frequency falls too, and the burst **drifts down in frequency** as the
shock climbs. Measuring that drift, with a model of the coronal density, gives the
shock's speed -- real science doable with a ~1 m antenna (see the Radio JOVE
project in ``docs/projects.md``). This module provides the density model, the
plasma-frequency relation, and the forward/inverse burst-drift calculation.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "R_SUN_KM",
    "plasma_frequency",
    "density_from_plasma_frequency",
    "newkirk_density",
    "newkirk_radius",
    "type_ii_track",
    "shock_speed_from_track",
]

#: Solar radius in km.
R_SUN_KM = 6.957e5

# Plasma frequency: f_p[MHz] = 8.977e-3 * sqrt(n_e[cm^-3]).
_FP_COEFF = 8.977e-3
# Newkirk (1961) coronal density model: n_e = fold * 4.2e4 * 10^(4.32 / r).
_NEWKIRK_A = 4.2e4
_NEWKIRK_B = 4.32


def plasma_frequency(n_e_cm3: np.ndarray) -> np.ndarray:
    """Electron plasma frequency in MHz for a density in cm^-3."""
    return _FP_COEFF * np.sqrt(np.asarray(n_e_cm3, dtype=float))


def density_from_plasma_frequency(f_mhz: np.ndarray) -> np.ndarray:
    """Inverse of :func:`plasma_frequency`: density (cm^-3) for a plasma frequency (MHz)."""
    return (np.asarray(f_mhz, dtype=float) / _FP_COEFF) ** 2


def newkirk_density(r_rsun: np.ndarray, fold: float = 1.0) -> np.ndarray:
    """Newkirk (1961) coronal electron density (cm^-3) at heliocentric radius.

    :math:`n_e = f \\cdot 4.2\\times10^4 \\cdot 10^{4.32/r}`, with ``r`` in solar
    radii (measured from Sun centre). ``fold`` (1--4) scales for denser
    streamers/active regions.
    """
    r = np.asarray(r_rsun, dtype=float)
    return fold * _NEWKIRK_A * 10 ** (_NEWKIRK_B / r)


def newkirk_radius(n_e_cm3: np.ndarray, fold: float = 1.0) -> np.ndarray:
    """Invert the Newkirk model: heliocentric radius (solar radii) for a density."""
    n_e = np.asarray(n_e_cm3, dtype=float)
    return _NEWKIRK_B / np.log10(n_e / (fold * _NEWKIRK_A))


def type_ii_track(
    speed_km_s: float,
    *,
    r_start: float = 1.5,
    duration_s: float = 600.0,
    n_points: int = 200,
    harmonic: int = 2,
    fold: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Forward-model a type II burst's frequency-time drift.

    A shock moves radially outward at constant ``speed_km_s`` from ``r_start``
    (solar radii). At each height the emission appears at ``harmonic`` times the
    local plasma frequency (harmonic=1 fundamental, 2 harmonic).

    Returns
    -------
    (times_s, freqs_mhz)
        Time since burst onset (s) and the emitted frequency (MHz).
    """
    times = np.linspace(0.0, duration_s, n_points)
    r = r_start + (speed_km_s / R_SUN_KM) * times  # solar radii
    n_e = newkirk_density(r, fold=fold)
    freqs = harmonic * plasma_frequency(n_e)
    return times, freqs


def shock_speed_from_track(
    times_s: np.ndarray,
    freqs_mhz: np.ndarray,
    *,
    harmonic: int = 2,
    fold: float = 1.0,
) -> float:
    """Recover the shock speed (km/s) from an observed type II frequency drift.

    Converts each frequency to a plasma frequency (dividing by ``harmonic``), then
    to a density, then to a heliocentric radius via the Newkirk model, and fits a
    straight line to radius-vs-time. The slope is the radial shock speed.
    """
    f_p = np.asarray(freqs_mhz, dtype=float) / harmonic
    n_e = density_from_plasma_frequency(f_p)
    r = newkirk_radius(n_e, fold=fold)  # solar radii
    slope = np.polyfit(np.asarray(times_s, dtype=float), r, 1)[0]  # R_sun / s
    return float(slope * R_SUN_KM)  # km / s
