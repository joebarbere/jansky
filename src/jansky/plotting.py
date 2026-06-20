"""Shared matplotlib styling so every chapter's figures look consistent.

Import :func:`use_jansky_style` at the top of a notebook and all subsequent
plots pick up a clean, legible default. The helpers here are thin conveniences
around matplotlib -- nothing is hidden, so learners can always drop down to raw
matplotlib when they want to.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

__all__ = ["use_jansky_style", "plot_uv_coverage", "show_image"]


#: The course's matplotlib rcParams, applied by :func:`use_jansky_style`.
JANSKY_STYLE = {
    "figure.figsize": (8.0, 5.0),
    "figure.dpi": 100,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": "large",
    "axes.titleweight": "bold",
    "font.size": 11,
    "image.cmap": "inferno",
    "image.origin": "lower",
}


def use_jansky_style() -> None:
    """Apply the course-wide plot style to the current matplotlib session."""
    plt.rcParams.update(JANSKY_STYLE)


def plot_uv_coverage(uv: np.ndarray, ax: plt.Axes | None = None, **kwargs):
    """Scatter-plot a uv-coverage sampling, in kilolambda-agnostic metres.

    Parameters
    ----------
    uv
        ``(n_samples, 2)`` array of (u, v) points.
    ax
        Optional existing axes; a new figure is created if omitted.
    **kwargs
        Forwarded to :meth:`~matplotlib.axes.Axes.scatter`.
    """
    if ax is None:
        _, ax = plt.subplots()
    kwargs.setdefault("s", 2)
    kwargs.setdefault("color", "#1f77b4")
    ax.scatter(uv[:, 0], uv[:, 1], **kwargs)
    ax.set_xlabel("u  [m]")
    ax.set_ylabel("v  [m]")
    ax.set_title("uv coverage")
    ax.set_aspect("equal")
    return ax


def show_image(image: np.ndarray, ax: plt.Axes | None = None, title: str | None = None,
               **kwargs):
    """Display a 2-D image with a colorbar using the course defaults.

    Parameters
    ----------
    image
        2-D array to display.
    ax
        Optional existing axes.
    title
        Optional axes title.
    **kwargs
        Forwarded to :meth:`~matplotlib.axes.Axes.imshow`.
    """
    if ax is None:
        _, ax = plt.subplots()
    im = ax.imshow(image, **kwargs)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if title:
        ax.set_title(title)
    return ax
