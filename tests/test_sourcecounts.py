"""Tests for jansky.sourcecounts -- radio source counts and the radio population."""

from __future__ import annotations

import numpy as np

from jansky import sourcecounts as sc


def _pareto_euclidean_sample(n, s_min=1.0, seed=0):
    """Draw fluxes whose integral counts follow the Euclidean N(>S) ∝ S^-1.5.

    P(S > x) = (x/s_min)^-1.5 is a Pareto law with index 1.5, so
    S = s_min * U^(-1/1.5) for U ~ Uniform(0, 1).
    """
    rng = np.random.default_rng(seed)
    u = rng.uniform(size=n)
    return s_min * u ** (-1.0 / 1.5)


def test_euclidean_slopes_are_exact():
    s = np.geomspace(0.01, 100.0, 200)
    n_int = sc.euclidean_integral_counts(s, n_ref=10.0, s_ref=1.0)
    n_diff = sc.euclidean_differential_counts(s, n_ref=10.0, s_ref=1.0)
    assert np.isclose(sc.count_slope(s, n_int), sc.EUCLIDEAN_INTEGRAL_SLOPE, atol=1e-9)
    assert np.isclose(sc.count_slope(s, n_diff), sc.EUCLIDEAN_DIFFERENTIAL_SLOPE, atol=1e-9)
    # Normalisation anchors at s_ref.
    assert np.isclose(sc.euclidean_integral_counts(1.0, n_ref=10.0), 10.0)


def test_integral_counts_recovers_euclidean_slope():
    fluxes = _pareto_euclidean_sample(40000, s_min=1.0, seed=1)
    s, n = sc.integral_counts(fluxes)
    # Descending fluxes, increasing cumulative count.
    assert s[0] == fluxes.max()
    assert np.all(np.diff(n) == 1)
    # Fit the slope over the well-populated range (avoid the rare bright tail).
    mid = (s > 1.5) & (s < 50.0)
    slope = sc.count_slope(s[mid], n[mid])
    assert np.isclose(slope, -1.5, atol=0.05)


def test_differential_counts_estimator_and_slope():
    fluxes = _pareto_euclidean_sample(60000, s_min=1.0, seed=2)
    bins = np.geomspace(1.0, 100.0, 25)
    centres, dn_ds, err = sc.differential_counts(fluxes, bins)
    assert centres.size == bins.size - 1
    assert np.all(err >= 0)
    good = dn_ds > 0
    slope = sc.count_slope(centres[good], dn_ds[good])
    assert np.isclose(slope, -2.5, atol=0.1)


def test_euclidean_normalised_counts_are_flat():
    # For a pure Euclidean differential count, S^2.5 dN/dS is constant.
    s = np.geomspace(0.1, 100.0, 50)
    dn_ds = sc.euclidean_differential_counts(s, n_ref=5.0)
    norm = sc.euclidean_normalised_counts(s, dn_ds)
    assert np.allclose(norm, norm[0], rtol=1e-9)


def test_radio_luminosity_function_shape():
    l_star = 1.0e25
    lum = np.geomspace(1.0e22, 1.0e28, 400)
    phi = sc.radio_luminosity_function(lum, l_star=l_star, alpha=0.7, beta=2.2)
    # Monotonically decreasing space density with luminosity.
    assert np.all(np.diff(phi) < 0)
    # Faint and bright wings follow the input slopes.
    faint = lum < 1.0e24
    bright = lum > 1.0e26
    s_faint = np.polyfit(np.log10(lum[faint]), np.log10(phi[faint]), 1)[0]
    s_bright = np.polyfit(np.log10(lum[bright]), np.log10(phi[bright]), 1)[0]
    assert np.isclose(s_faint, -0.7, atol=0.05)
    assert np.isclose(s_bright, -2.2, atol=0.05)


def test_evolution_factor():
    assert np.isclose(sc.evolution_factor(0.0), 1.0)
    assert np.isclose(sc.evolution_factor(1.0, q=3.0), 8.0)
    z = np.array([0.0, 1.0, 3.0])
    assert np.allclose(sc.evolution_factor(z, q=2.0), [1.0, 4.0, 16.0])
