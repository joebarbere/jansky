"""Tests for jansky.plotting -- the shared matplotlib helpers.

Uses the non-interactive Agg backend so the figures render headlessly.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

from jansky import plotting  # noqa: E402


def test_use_jansky_style_applies_rcparams():
    plotting.use_jansky_style()
    assert plt.rcParams["image.cmap"] == "inferno"
    assert plt.rcParams["image.origin"] == "lower"
    assert plt.rcParams["axes.spines.top"] is False


def test_use_jansky_style_sets_colorblind_cycle():
    plotting.use_jansky_style()
    cycle_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    assert cycle_colors == plotting.COLORBLIND_CYCLE
    # The Okabe-Ito palette has no pure red/green pair as adjacent defaults.
    assert "#0072B2" in cycle_colors  # blue first


def test_plot_uv_coverage_returns_axes():
    uv = np.column_stack([np.linspace(-100, 100, 50), np.linspace(50, -50, 50)])
    ax = plotting.plot_uv_coverage(uv)
    assert ax.get_xlabel() == "u  [m]"
    assert ax.get_aspect() == 1.0  # equal aspect
    assert len(ax.collections) == 1  # the scatter
    plt.close(ax.figure)


def test_plot_uv_coverage_reuses_given_axes():
    uv = np.zeros((3, 2))
    fig, ax = plt.subplots()
    out = plotting.plot_uv_coverage(uv, ax=ax)
    assert out is ax
    plt.close(fig)


def test_show_image_adds_colorbar_and_title():
    img = np.arange(16, dtype=float).reshape(4, 4)
    ax = plotting.show_image(img, title="test")
    assert ax.get_title() == "test"
    assert len(ax.images) == 1
    # A colorbar adds a second axes to the figure.
    assert len(ax.figure.axes) == 2
    plt.close(ax.figure)


def test_percentile_limits_are_nan_safe_and_ordered():
    data = np.concatenate([np.linspace(0.0, 100.0, 1000), [np.nan, np.inf]])
    lo, hi = plotting.percentile_limits(data, low=1.0, high=99.0)
    assert 0.0 <= lo < hi <= 100.0
    assert np.isclose(lo, 1.0, atol=0.5) and np.isclose(hi, 99.0, atol=0.5)
    # All-NaN input degrades to a sane default rather than crashing.
    assert plotting.percentile_limits(np.full(5, np.nan)) == (0.0, 1.0)


def test_robust_rms_ignores_a_bright_outlier():
    rng = np.random.default_rng(0)
    noise = rng.normal(0.0, 2.0, size=10000)
    clean = plotting.robust_rms(noise)
    noise[0] = 1e6  # a bright source / artefact
    assert np.isclose(plotting.robust_rms(noise), clean, rtol=0.05)  # barely moves
    assert np.isclose(clean, 2.0, rtol=0.1)


def test_dynamic_range_peak_over_noise():
    rng = np.random.default_rng(1)
    img = rng.normal(0.0, 1.0, size=(200, 200))
    img[100, 100] = 1000.0  # a 1000-sigma peak
    dr = plotting.dynamic_range(img)
    assert 800 < dr < 1200  # ~ peak / unit-rms


def test_radio_norm_maps_clip_limits_to_unit_interval():
    img = np.linspace(0.0, 10.0, 100).reshape(10, 10)
    norm = plotting.radio_norm(img, stretch="asinh", low=0.0, high=100.0)
    assert np.isclose(norm.vmin, 0.0, atol=1e-6)
    assert np.isclose(norm.vmax, 10.0, atol=1e-6)
    # The stretch sends the clip limits to 0 and 1.
    assert np.isclose(float(norm(norm.vmin)), 0.0, atol=1e-6)
    assert np.isclose(float(norm(norm.vmax)), 1.0, atol=1e-6)
    for s in ("linear", "log", "sqrt", "asinh"):
        plotting.radio_norm(img, stretch=s)
    with pytest.raises(ValueError):
        plotting.radio_norm(img, stretch="rainbow")


def test_recommend_cmap_avoids_jet():
    assert plotting.recommend_cmap("sequential") == "inferno"
    assert plotting.recommend_cmap("gentle") == "viridis"
    assert plotting.recommend_cmap("diverging") == "RdBu_r"
    assert "jet" not in plotting._CMAP_BY_KIND.values()
    # "spectral" is deliberately not a key (matplotlib's "Spectral" is a different map).
    assert "spectral" not in plotting._CMAP_BY_KIND
    with pytest.raises(ValueError):
        plotting.recommend_cmap("rainbow")


def test_add_beam_adds_an_ellipse():
    fig, ax = plt.subplots()
    ax.imshow(np.zeros((10, 10)))
    e = plotting.add_beam(ax, bmaj=3.0, bmin=1.5, bpa_deg=30.0, xy=(2, 2))
    assert e in ax.patches
    plt.close(fig)


def test_dynamic_spectrum_renders_with_colorbar():
    rng = np.random.default_rng(2)
    waterfall = rng.normal(0.0, 1.0, size=(64, 256))
    ax = plotting.dynamic_spectrum(waterfall, extent=(0, 10, 1, 2))
    assert ax.get_xlabel() == "time"
    assert ax.get_ylabel() == "frequency"
    assert len(ax.images) == 1
    assert len(ax.figure.axes) == 2  # image + colorbar
    plt.close(ax.figure)
