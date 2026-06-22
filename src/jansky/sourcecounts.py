"""Radio source counts and the extragalactic radio population.

The number of radio sources as a function of flux density -- the **log N-log S**
relation -- is one of radio astronomy's oldest cosmological probes (Essential Radio
Astronomy, Ch 2). In a static, uniformly-filled Euclidean universe the counts follow a
universal power law: the number brighter than flux :math:`S` goes as
:math:`N(>S) \\propto S^{-3/2}` (differential :math:`\\mathrm{d}N/\\mathrm{d}S \\propto
S^{-5/2}`), independent of the sources' luminosities. The **observed** counts are
steeper than Euclidean at bright flux and flatten at faint flux -- a departure that, in
the 1950s-60s, showed the source population evolves with cosmic time and helped end
steady-state cosmology (Ryle & Clarke 1961).

This module collects the teachable estimators: the Euclidean differential and integral
counts, empirical counts from a flux list, the Euclidean-**normalised** differential
count (flat for a non-evolving population), a power-law-slope fit, a toy radio luminosity
function, and a simple :math:`(1+z)^q` evolution factor. The morphological split of
powerful radio galaxies into edge-darkened **FR I** and edge-brightened **FR II** sources
(Fanaroff & Riley 1974) is illustrated in the chapter notebook.

References
----------
* Condon, J. J. & Ransom, S. M., *Essential Radio Astronomy*, Ch 2.
* Ryle, M. & Clarke, R. W. (1961), MNRAS 122, 349 -- evolving source counts.
* Fanaroff, B. L. & Riley, J. M. (1974), MNRAS 167, 31P -- the FR I / FR II split.
* Condon, J. J. (1992), ARA&A 30, 575 -- radio emission from normal galaxies.
* de Zotti, G. et al. (2010), A&ARv 18, 1 -- modern radio source counts.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "EUCLIDEAN_INTEGRAL_SLOPE",
    "EUCLIDEAN_DIFFERENTIAL_SLOPE",
    "euclidean_integral_counts",
    "euclidean_differential_counts",
    "integral_counts",
    "differential_counts",
    "euclidean_normalised_counts",
    "count_slope",
    "radio_luminosity_function",
    "evolution_factor",
]

#: Slope of the static-Euclidean *integral* counts, :math:`N(>S) \\propto S^{-3/2}`.
EUCLIDEAN_INTEGRAL_SLOPE: float = -1.5

#: Slope of the static-Euclidean *differential* counts,
#: :math:`\\mathrm{d}N/\\mathrm{d}S \\propto S^{-5/2}`.
EUCLIDEAN_DIFFERENTIAL_SLOPE: float = -2.5


def euclidean_integral_counts(
    s: np.ndarray | float,
    n_ref: float = 1.0,
    s_ref: float = 1.0,
) -> np.ndarray:
    """Static-Euclidean integral counts :math:`N(>S) = n_\\mathrm{ref}(S/S_\\mathrm{ref})^{-3/2}`.

    The number of sources per unit solid angle brighter than flux density ``s``. The
    :math:`-3/2` slope follows purely from Euclidean geometry: sources of a fixed
    luminosity fill a volume :math:`\\propto r^3` out to distance :math:`r \\propto
    S^{-1/2}`, so :math:`N(>S) \\propto r^3 \\propto S^{-3/2}`, independent of the
    luminosity function.

    Parameters
    ----------
    s
        Flux density (any unit, matching ``s_ref``).
    n_ref
        Normalisation: the count brighter than ``s_ref``.
    s_ref
        Reference flux density.

    Returns
    -------
    numpy.ndarray
        Number of sources brighter than ``s``.
    """
    s = np.asarray(s, dtype=float)
    return n_ref * (s / s_ref) ** EUCLIDEAN_INTEGRAL_SLOPE


def euclidean_differential_counts(
    s: np.ndarray | float,
    n_ref: float = 1.0,
    s_ref: float = 1.0,
) -> np.ndarray:
    """Static-Euclidean differential counts :math:`\\mathrm{d}N/\\mathrm{d}S \\propto S^{-5/2}`.

    The derivative of :func:`euclidean_integral_counts`: the number of sources per unit
    flux interval. ``n_ref`` is the differential count at ``s_ref``.

    Parameters
    ----------
    s
        Flux density.
    n_ref
        Differential count :math:`\\mathrm{d}N/\\mathrm{d}S` at ``s_ref``.
    s_ref
        Reference flux density.

    Returns
    -------
    numpy.ndarray
        Differential source count at ``s``.
    """
    s = np.asarray(s, dtype=float)
    return n_ref * (s / s_ref) ** EUCLIDEAN_DIFFERENTIAL_SLOPE


def integral_counts(fluxes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Empirical integral counts :math:`N(>S)` from a list of source flux densities.

    Returns the fluxes sorted in **descending** order together with the running count
    of sources at least that bright (1, 2, 3, ...). Plotting the second array against
    the first on log-log axes gives the observed log N-log S curve.

    Parameters
    ----------
    fluxes
        Measured flux densities of the sources in a survey.

    Returns
    -------
    tuple of numpy.ndarray
        ``(s_sorted_descending, n_brighter)``.
    """
    s = np.sort(np.asarray(fluxes, dtype=float))[::-1]
    n = np.arange(1, s.size + 1, dtype=float)
    return s, n


def differential_counts(
    fluxes: np.ndarray,
    bins: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Empirical differential counts :math:`\\mathrm{d}N/\\mathrm{d}S` in flux bins.

    Bins the fluxes and divides each bin's source count by the bin width, with Poisson
    (:math:`\\sqrt{N}`) error bars. Bin centres are the geometric means of the edges,
    appropriate for logarithmically-spaced ``bins``.

    Parameters
    ----------
    fluxes
        Measured flux densities.
    bins
        Bin edges (typically ``np.geomspace(...)``).

    Returns
    -------
    tuple of numpy.ndarray
        ``(centres, dN_dS, dN_dS_error)``.
    """
    fluxes = np.asarray(fluxes, dtype=float)
    edges = np.asarray(bins, dtype=float)
    counts, _ = np.histogram(fluxes, bins=edges)
    width = np.diff(edges)
    centres = np.sqrt(edges[:-1] * edges[1:])
    dn_ds = counts / width
    dn_ds_err = np.sqrt(counts) / width
    return centres, dn_ds, dn_ds_err


def euclidean_normalised_counts(
    s: np.ndarray,
    dn_ds: np.ndarray,
) -> np.ndarray:
    """Euclidean-normalised differential counts :math:`S^{5/2}\\,\\mathrm{d}N/\\mathrm{d}S`.

    The standard way to plot radio source counts: multiplying the differential count by
    :math:`S^{5/2}` divides out the steep Euclidean slope, so a non-evolving Euclidean
    population is a **flat horizontal line** and any real structure (the bright-end
    excess, the faint-end upturn from star-forming galaxies) stands out clearly.

    Parameters
    ----------
    s
        Flux densities at which ``dn_ds`` is evaluated.
    dn_ds
        Differential counts :math:`\\mathrm{d}N/\\mathrm{d}S`.

    Returns
    -------
    numpy.ndarray
        :math:`S^{5/2}\\,\\mathrm{d}N/\\mathrm{d}S`.
    """
    s = np.asarray(s, dtype=float)
    return s**2.5 * np.asarray(dn_ds, dtype=float)


def count_slope(s: np.ndarray, counts: np.ndarray) -> float:
    """Fit the power-law slope of counts versus flux on log-log axes.

    A least-squares fit of :math:`\\log_{10}(\\text{counts})` against
    :math:`\\log_{10} S`. Applied to integral counts a pure Euclidean population returns
    :data:`EUCLIDEAN_INTEGRAL_SLOPE` (:math:`-1.5`); to differential counts,
    :data:`EUCLIDEAN_DIFFERENTIAL_SLOPE` (:math:`-2.5`). Only strictly positive points
    are used.

    Parameters
    ----------
    s
        Flux densities.
    counts
        Integral or differential counts at ``s``.

    Returns
    -------
    float
        The fitted log-log slope.
    """
    s = np.asarray(s, dtype=float)
    counts = np.asarray(counts, dtype=float)
    mask = (s > 0) & (counts > 0)
    return float(np.polyfit(np.log10(s[mask]), np.log10(counts[mask]), 1)[0])


def radio_luminosity_function(
    luminosity: np.ndarray | float,
    phi_star: float = 1.0e-6,
    l_star: float = 1.0e25,
    alpha: float = 0.7,
    beta: float = 2.2,
) -> np.ndarray:
    """A toy double-power-law radio luminosity function :math:`\\Phi(L)`.

    The space density of sources per unit :math:`\\log L`, modelled as a smoothly broken
    power law that is shallow below the break luminosity ``l_star`` and steep above it:

    .. math::

        \\Phi(L) = \\frac{\\Phi_\\star}{(L/L_\\star)^{\\alpha} + (L/L_\\star)^{\\beta}}.

    This captures the qualitative shape of the local radio luminosity function (e.g.
    Condon 1992): many faint star-forming galaxies and a steep cut-off of rare, powerful
    radio-loud AGN. It is illustrative, not a fit to data.

    Parameters
    ----------
    luminosity
        Radio luminosity (e.g. W Hz⁻¹), matching ``l_star``.
    phi_star
        Normalisation (space density per unit log L at the break).
    l_star
        Break luminosity.
    alpha
        Faint-end (low-L) slope.
    beta
        Bright-end (high-L) slope.

    Returns
    -------
    numpy.ndarray
        Space density :math:`\\Phi(L)`.
    """
    x = np.asarray(luminosity, dtype=float) / l_star
    return phi_star / (x**alpha + x**beta)


def evolution_factor(z: np.ndarray | float, q: float = 3.0) -> np.ndarray:
    """A toy cosmic-evolution factor :math:`(1+z)^q` for the source population.

    Radio-source counts require the comoving space density (or luminosity) of sources to
    rise toward higher redshift; a common shorthand is a :math:`(1+z)^q` boost with
    :math:`q \\approx 3` out to :math:`z \\sim 2`. This single factor is what tilts the
    observed counts away from the static-Euclidean slope -- the teaching point of the
    chapter. It is a toy, not a real evolutionary model.

    Parameters
    ----------
    z
        Redshift.
    q
        Evolution exponent.

    Returns
    -------
    numpy.ndarray
        The enhancement factor :math:`(1+z)^q`.
    """
    return (1.0 + np.asarray(z, dtype=float)) ** q
