"""Polarisation and Faraday rotation.

Polarisation is the fourth pillar of radio observation (after position, intensity,
and spectrum) and the primary probe of cosmic magnetic fields. A linearly
polarised wave is described by the **Stokes parameters** :math:`I, Q, U, V`; as it
travels through a magnetised plasma its plane of polarisation rotates by an amount
proportional to :math:`\\lambda^2` -- **Faraday rotation** -- set by the *rotation
measure* (RM), the integral of the electron density times the line-of-sight
magnetic field. Observing the polarisation angle across many wavelengths and
inverting that :math:`\\lambda^2` dependence -- **RM synthesis** (Burn 1966;
Brentjens & de Bruyn 2005) -- recovers the distribution of Faraday depth along the
sightline.

This module provides the Stokes constructions, the Faraday :math:`\\lambda^2` law,
a least-squares RM fit, and a minimal RM-synthesis (Faraday tomography) transform.
Everything is plain NumPy so the maths stays inspectable.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "stokes_linear",
    "linear_polarization_fraction",
    "polarization_angle",
    "complex_polarization",
    "faraday_rotate",
    "rotation_measure_fit",
    "rmsf",
    "rm_synthesis",
]


def stokes_linear(
    intensity: np.ndarray | float,
    frac: np.ndarray | float,
    angle: np.ndarray | float,
) -> tuple[np.ndarray, np.ndarray]:
    """Linear Stokes ``Q``, ``U`` from total intensity, polarised fraction, angle.

    :math:`Q = p\\,I\\cos 2\\chi`, :math:`U = p\\,I\\sin 2\\chi`, where ``p`` is the
    linear polarisation fraction and :math:`\\chi` the polarisation (E-vector
    position) angle in radians. The factor of two reflects that polarisation is a
    "headless vector": rotating by :math:`\\pi` returns the same state.
    """
    intensity = np.asarray(intensity, dtype=float)
    frac = np.asarray(frac, dtype=float)
    angle = np.asarray(angle, dtype=float)
    q = frac * intensity * np.cos(2.0 * angle)
    u = frac * intensity * np.sin(2.0 * angle)
    return q, u


def linear_polarization_fraction(
    intensity: np.ndarray | float,
    q: np.ndarray | float,
    u: np.ndarray | float,
) -> np.ndarray:
    """Linear polarisation fraction :math:`p = \\sqrt{Q^2 + U^2}/I`."""
    q = np.asarray(q, dtype=float)
    u = np.asarray(u, dtype=float)
    return np.sqrt(q**2 + u**2) / np.asarray(intensity, dtype=float)


def polarization_angle(q: np.ndarray | float, u: np.ndarray | float) -> np.ndarray:
    """Polarisation (E-vector position) angle :math:`\\chi = \\tfrac12\\arctan(U/Q)`.

    Returned in radians on :math:`(-\\pi/2, \\pi/2]`; uses ``arctan2`` so all four
    quadrants are handled.
    """
    q = np.asarray(q, dtype=float)
    u = np.asarray(u, dtype=float)
    return 0.5 * np.arctan2(u, q)


def complex_polarization(q: np.ndarray | float, u: np.ndarray | float) -> np.ndarray:
    """Complex linear polarisation :math:`P = Q + iU = p\\,I\\,e^{2i\\chi}`."""
    return np.asarray(q, dtype=float) + 1j * np.asarray(u, dtype=float)


def faraday_rotate(
    angle0: np.ndarray | float,
    rm: float,
    wavelength: np.ndarray | float,
) -> np.ndarray:
    """Apply the Faraday :math:`\\lambda^2` law to a polarisation angle.

    :math:`\\chi(\\lambda) = \\chi_0 + \\mathrm{RM}\\,\\lambda^2`, with ``rm`` in
    rad m\\ :sup:`-2` and ``wavelength`` in metres. The observed angle rotates more
    at longer wavelengths -- the signature that lets RM be measured.
    """
    angle0 = np.asarray(angle0, dtype=float)
    wavelength = np.asarray(wavelength, dtype=float)
    return angle0 + rm * wavelength**2


def rotation_measure_fit(
    wavelength: np.ndarray,
    angle: np.ndarray,
) -> tuple[float, float]:
    """Least-squares RM from polarisation angle versus wavelength.

    Fits :math:`\\chi = \\chi_0 + \\mathrm{RM}\\,\\lambda^2`. The angle is unwrapped
    (on :math:`2\\chi`, since :math:`\\chi` is :math:`\\pi`-periodic) before the fit
    to reduce -- but not fully remove -- the :math:`n\\pi` ambiguity. Returns
    ``(rm, angle0)`` with ``rm`` in rad m\\ :sup:`-2` and ``angle0`` in radians.

    For widely spaced or noisy bands the unwrap can fail; RM synthesis
    (:func:`rm_synthesis`) is the robust alternative.
    """
    lam2 = np.asarray(wavelength, dtype=float) ** 2
    chi = np.asarray(angle, dtype=float)
    order = np.argsort(lam2)
    lam2_sorted = lam2[order]
    # Unwrap on 2*chi (the pi-periodic quantity), then halve back.
    chi_unwrapped = 0.5 * np.unwrap(2.0 * chi[order])
    slope, intercept = np.polyfit(lam2_sorted, chi_unwrapped, 1)
    return float(slope), float(intercept)


def rmsf(wavelength: np.ndarray, phi: np.ndarray, weights: np.ndarray | None = None) -> np.ndarray:
    """Rotation-measure spread function (the RM-synthesis "dirty beam").

    :math:`R(\\phi) = \\dfrac{\\sum_i w_i\\, e^{-2i\\phi(\\lambda_i^2-\\lambda_0^2)}}
    {\\sum_i w_i}`, the instrumental response in Faraday depth set purely by the
    :math:`\\lambda^2` sampling. Its width sets the Faraday-depth resolution.
    """
    lam2 = np.asarray(wavelength, dtype=float) ** 2
    lam0_2 = lam2.mean()
    phi = np.asarray(phi, dtype=float)
    w = np.ones_like(lam2) if weights is None else np.asarray(weights, dtype=float)
    phase = np.exp(-2j * phi[:, None] * (lam2[None, :] - lam0_2))
    return (phase * w[None, :]).sum(axis=1) / w.sum()


def rm_synthesis(
    wavelength: np.ndarray,
    p_complex: np.ndarray,
    phi: np.ndarray,
    weights: np.ndarray | None = None,
) -> np.ndarray:
    """Faraday dispersion function via RM synthesis (Brentjens & de Bruyn 2005).

    :math:`F(\\phi) = \\dfrac{\\sum_i w_i\\, P_i\\, e^{-2i\\phi(\\lambda_i^2-\\lambda_0^2)}}
    {\\sum_i w_i}`, reconstructing the polarised emission as a function of Faraday
    depth :math:`\\phi`. For a single Faraday-thin screen, :math:`|F(\\phi)|` peaks
    at :math:`\\phi=\\mathrm{RM}`.

    Parameters
    ----------
    wavelength
        Observing wavelengths (m), one per channel.
    p_complex
        Complex linear polarisation :math:`P = Q + iU` per channel
        (see :func:`complex_polarization`).
    phi
        Faraday-depth axis (rad m\\ :sup:`-2`) to evaluate on.
    weights
        Optional per-channel weights (e.g. inverse variance). Uniform if omitted.
    """
    lam2 = np.asarray(wavelength, dtype=float) ** 2
    lam0_2 = lam2.mean()
    p = np.asarray(p_complex, dtype=complex)
    phi = np.asarray(phi, dtype=float)
    w = np.ones_like(lam2) if weights is None else np.asarray(weights, dtype=float)
    phase = np.exp(-2j * phi[:, None] * (lam2[None, :] - lam0_2))
    return (p[None, :] * phase * w[None, :]).sum(axis=1) / w.sum()
