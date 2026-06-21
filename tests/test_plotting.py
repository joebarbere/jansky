"""Tests for jansky.plotting -- the shared matplotlib helpers.

Uses the non-interactive Agg backend so the figures render headlessly.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

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
