"""Shared matplotlib styling so every chapter's figures look consistent.

Import :func:`use_jansky_style` at the top of a notebook and all subsequent
plots pick up a clean, legible default. The helpers here are thin conveniences
around matplotlib -- nothing is hidden, so learners can always drop down to raw
matplotlib when they want to.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import (
    AsinhStretch,
    ImageNormalize,
    LinearStretch,
    LogStretch,
    PowerStretch,
)
from cycler import cycler

__all__ = [
    "COLORBLIND_CYCLE",
    "use_jansky_style",
    "plot_uv_coverage",
    "show_image",
    "percentile_limits",
    "robust_rms",
    "dynamic_range",
    "radio_norm",
    "recommend_cmap",
    "add_beam",
    "dynamic_spectrum",
]


#: Okabe--Ito colourblind-safe categorical palette (Wong 2011, *Nature Methods*),
#: ordered so adjacent series stay distinguishable for the common colour-vision
#: deficiencies. Used as the default line-colour cycle so figures are legible
#: without relying on red/green contrast. Yellow is last as it is low-contrast on
#: white. https://www.nature.com/articles/nmeth.1618
COLORBLIND_CYCLE = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # bluish green
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
]


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
    # Colourblind-safe default line cycle (overridable per-plot).
    "axes.prop_cycle": cycler(color=COLORBLIND_CYCLE),
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


def show_image(image: np.ndarray, ax: plt.Axes | None = None, title: str | None = None, **kwargs):
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


# --- The visualisation toolkit (Chapter 46) -------------------------------------------

#: Recommended, perceptually-uniform colormaps by data kind. "jet"/"rainbow" are
#: deliberately absent: their non-monotonic luminance invents structure that isn't there.
_CMAP_BY_KIND = {
    "sequential": "inferno",  # single-sided intensity (most radio images)
    "gentle": "viridis",  # alt. sequential, softer than inferno (avoid the name "spectral":
    #                       matplotlib's "Spectral" is a *diverging* rainbow-adjacent map)
    "diverging": "RdBu_r",  # signed data around zero (Stokes Q/U/V, CMB Delta T)
    "colorblind": "cividis",  # sequential and robust to all colour-vision deficiencies
}


def percentile_limits(
    data: np.ndarray, low: float = 1.0, high: float = 99.5
) -> tuple[float, float]:
    """NaN-safe ``(vmin, vmax)`` clip limits at the given percentiles.

    Radio images have a few very bright pixels (cores, calibration artefacts) and a
    long faint tail; scaling to the raw min/max wastes the whole colour range on the
    background. Clipping to, say, the 1st and 99.5th percentiles is the simplest fix.
    """
    finite = np.asarray(data, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return (0.0, 1.0)
    lo, hi = np.percentile(finite, [low, high])
    return (float(lo), float(hi))


def robust_rms(data: np.ndarray) -> float:
    """Robust noise estimate, ``1.4826 * MAD`` (median absolute deviation).

    Unlike the plain standard deviation this is barely moved by bright sources, so it
    measures the *background* noise -- the denominator of the dynamic range.
    """
    d = np.asarray(data, dtype=float)
    d = d[np.isfinite(d)]
    if d.size == 0:
        return 0.0
    mad = np.median(np.abs(d - np.median(d)))
    return float(1.4826 * mad)


def dynamic_range(data: np.ndarray) -> float:
    """Image dynamic range: peak divided by the robust background RMS.

    A radio map of an AGN can reach 10^4-10^6 -- which is exactly why a linear stretch
    shows a single bright dot on black, and why the asinh/log stretches below exist.
    """
    rms = robust_rms(data)
    peak = float(np.nanmax(np.asarray(data, dtype=float)))
    return peak / rms if rms > 0 else float("inf")


def radio_norm(
    data: np.ndarray,
    stretch: str = "asinh",
    low: float = 1.0,
    high: float = 99.5,
    asinh_a: float = 0.1,
) -> ImageNormalize:
    """A matplotlib ``norm`` for high-dynamic-range radio images.

    Combines percentile clip limits (:func:`percentile_limits`) with a non-linear
    stretch so faint extended emission and a bright core are visible *at once*. Pass the
    result to ``imshow(..., norm=radio_norm(data))``.

    Parameters
    ----------
    stretch
        ``"asinh"`` (the radio default -- linear near the noise, logarithmic for bright
        pixels), ``"log"``, ``"sqrt"``, or ``"linear"``.
    asinh_a
        The asinh softening point as a fraction of the clipped range (smaller = more
        aggressive compression of the bright end).
    """
    vmin, vmax = percentile_limits(data, low, high)
    stretches = {
        "asinh": AsinhStretch(a=asinh_a),
        "log": LogStretch(),
        "sqrt": PowerStretch(0.5),
        "linear": LinearStretch(),
    }
    if stretch not in stretches:
        raise ValueError(f"unknown stretch {stretch!r}; choose from {sorted(stretches)}")
    return ImageNormalize(vmin=vmin, vmax=vmax, stretch=stretches[stretch], clip=True)


def recommend_cmap(kind: str = "sequential") -> str:
    """Return a perceptually-uniform colormap name for a kind of data.

    ``"sequential"`` (intensity), ``"gentle"`` (a softer sequential), ``"diverging"``
    (signed data), or ``"colorblind"``. The non-perceptual ``jet``/``rainbow`` maps are
    intentionally not offered -- their luminance is not monotonic, so they fabricate features.
    """
    if kind not in _CMAP_BY_KIND:
        raise ValueError(f"unknown kind {kind!r}; choose from {sorted(_CMAP_BY_KIND)}")
    return _CMAP_BY_KIND[kind]


def add_beam(
    ax: plt.Axes,
    bmaj: float,
    bmin: float,
    bpa_deg: float = 0.0,
    xy: tuple[float, float] = (0.1, 0.1),
    facecolor: str = "0.9",
    edgecolor: str = "black",
):
    """Draw the synthesised-beam (resolution) ellipse on an image, in data coordinates.

    ``bmaj``/``bmin`` are the FWHM axes and ``bpa_deg`` the angle in matplotlib's
    **anti-clockwise** convention (0 deg = major axis along +y; positive rotates toward
    -x). To use a radio position angle measured *east of north* (with East = -x in an
    RA/Dec image), pass ``bpa_deg = -BPA``. Placing the beam on a radio map is not
    optional -- it is the PSF, and no structure smaller than it is real.
    """
    from matplotlib.patches import Ellipse

    ellipse = Ellipse(
        xy,
        width=bmin,
        height=bmaj,
        angle=bpa_deg,
        facecolor=facecolor,
        edgecolor=edgecolor,
        lw=1.2,
    )
    ax.add_patch(ellipse)
    return ellipse


def dynamic_spectrum(
    data: np.ndarray,
    ax: plt.Axes | None = None,
    extent: tuple[float, float, float, float] | None = None,
    cmap: str = "inferno",
    stretch: str = "asinh",
    colorbar: bool = True,
    **kwargs,
):
    """Display a time-frequency dynamic spectrum (waterfall) with sensible defaults.

    Uses :func:`radio_norm` so faint drifting features (a pulsar, an FRB, a Jovian burst)
    stand out, ``aspect="auto"`` so the panel fills its axes, and a labelled colorbar.
    ``extent`` is ``(t_min, t_max, f_min, f_max)``.
    """
    if ax is None:
        _, ax = plt.subplots()
    kwargs.setdefault("origin", "lower")
    kwargs.setdefault("aspect", "auto")
    im = ax.imshow(data, extent=extent, cmap=cmap, norm=radio_norm(data, stretch=stretch), **kwargs)
    if colorbar:
        ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_xlabel("time")
    ax.set_ylabel("frequency")
    return ax
