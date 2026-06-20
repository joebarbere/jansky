"""Aperture synthesis essentials: uv-coverage, the dirty beam, and CLEAN.

These helpers power the interferometry chapters. They are intentionally small,
single-frequency, 2-D demonstrations -- enough to *understand* the van
Cittert--Zernike relationship and Hogbom's CLEAN (1974) without the bookkeeping
of a full measurement-set pipeline (that comes later, with CASA, in Chapter 12).

The central idea: an interferometer samples the Fourier transform of the sky
brightness at spatial frequencies (u, v) set by its baselines. The image you
get back by inverse-transforming those samples is the true sky *convolved* with
the "dirty beam" (the transform of the sampling pattern). CLEAN deconvolves it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "uv_coverage",
    "grid_visibilities",
    "dirty_beam",
    "dirty_image",
    "hogbom_clean",
    "CleanResult",
]


def uv_coverage(
    antenna_xy: np.ndarray,
    hour_angles: np.ndarray | None = None,
    declination: float = np.pi / 2,
) -> np.ndarray:
    """Compute (u, v) samples for an array of antennas.

    For every pair of antennas the baseline vector contributes a visibility
    sample at (u, v) and, by Hermitian symmetry, its conjugate at (-u, -v).
    Optionally rotates the baselines through a set of hour angles to mimic how
    Earth rotation fills in the uv-plane ("Earth-rotation synthesis").

    Parameters
    ----------
    antenna_xy
        ``(n_ant, 2)`` array of antenna positions in metres (a simple planar
        array; good enough for the teaching demo).
    hour_angles
        Optional array of hour angles in radians. If ``None``, a single
        snapshot at hour angle 0 is returned.
    declination
        Source declination in radians (affects the v projection).

    Returns
    -------
    numpy.ndarray
        ``(n_samples, 2)`` array of (u, v) coordinates in metres, including the
        conjugate points.
    """
    antenna_xy = np.asarray(antenna_xy, dtype=float)
    n_ant = antenna_xy.shape[0]
    if hour_angles is None:
        hour_angles = np.array([0.0])
    hour_angles = np.atleast_1d(np.asarray(hour_angles, dtype=float))

    samples = []
    for i in range(n_ant):
        for j in range(i + 1, n_ant):
            bx, by = antenna_xy[j] - antenna_xy[i]
            for ha in hour_angles:
                # Standard baseline -> (u, v) projection for a planar array.
                u = bx * np.cos(ha) - by * np.sin(ha)
                v = (bx * np.sin(ha) + by * np.cos(ha)) * np.sin(declination)
                samples.append((u, v))
                samples.append((-u, -v))  # Hermitian conjugate
    return np.array(samples)


def grid_visibilities(uv: np.ndarray, npix: int = 256, cell: float | None = None) -> np.ndarray:
    """Grid (u, v) samples onto a square sampling mask in the Fourier plane.

    Parameters
    ----------
    uv
        ``(n_samples, 2)`` uv-coordinates from :func:`uv_coverage`.
    npix
        Size of the (square) grid in pixels.
    cell
        uv cell size (metres per pixel). If ``None``, chosen so the data fill
        ~80% of the grid.

    Returns
    -------
    numpy.ndarray
        ``(npix, npix)`` real array: 1 where a sample lands, 0 elsewhere.
    """
    uv = np.asarray(uv, dtype=float)
    if cell is None:
        extent = np.abs(uv).max() if uv.size else 1.0
        cell = 2.0 * extent / (0.8 * npix)
    grid = np.zeros((npix, npix), dtype=float)
    center = npix // 2
    ix = np.round(uv[:, 0] / cell).astype(int) + center
    iy = np.round(uv[:, 1] / cell).astype(int) + center
    inside = (ix >= 0) & (ix < npix) & (iy >= 0) & (iy < npix)
    grid[iy[inside], ix[inside]] = 1.0
    return grid


def _ift(mask: np.ndarray) -> np.ndarray:
    """Inverse-transform a centered Fourier-plane mask to an image (real part)."""
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(mask))).real


def dirty_beam(sampling: np.ndarray) -> np.ndarray:
    """Point-spread function (dirty beam) from a uv sampling mask.

    The dirty beam is the inverse Fourier transform of the sampling function;
    every point source in the dirty image is smeared by this pattern.
    Normalised to a peak of 1.
    """
    beam = _ift(sampling)
    peak = np.abs(beam).max()
    return beam / peak if peak else beam


def dirty_image(sky: np.ndarray, sampling: np.ndarray) -> np.ndarray:
    """Form the dirty image of a model ``sky`` seen with a given uv sampling.

    Transforms the sky to the Fourier plane, keeps only the sampled
    visibilities, and transforms back -- i.e. the sky convolved with the dirty
    beam.

    Parameters
    ----------
    sky
        ``(npix, npix)`` true sky brightness.
    sampling
        ``(npix, npix)`` uv sampling mask (same shape as ``sky``).

    Returns
    -------
    numpy.ndarray
        The dirty image.
    """
    vis = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(sky)))
    return _ift(vis * sampling)


@dataclass
class CleanResult:
    """Result of :func:`hogbom_clean`."""

    model: np.ndarray
    """Recovered sky model: a list of clean components on the pixel grid."""
    residual: np.ndarray
    """Residual dirty image after component subtraction."""
    components: list[tuple[int, int, float]]
    """(row, col, flux) of each clean component, in subtraction order."""


def hogbom_clean(
    dirty: np.ndarray,
    beam: np.ndarray,
    gain: float = 0.1,
    n_iter: int = 100,
    threshold: float = 0.0,
) -> CleanResult:
    """A minimal Hogbom (1974) CLEAN deconvolution.

    Iteratively finds the brightest pixel in the residual, records a fraction
    ``gain`` of it as a clean component, and subtracts a scaled, shifted copy of
    the dirty beam. Repeats until ``n_iter`` or until the peak drops below
    ``threshold``. This is the algorithm that made aperture-synthesis imaging
    practical.

    Parameters
    ----------
    dirty
        The dirty image to deconvolve.
    beam
        The dirty beam (point-spread function), same shape as ``dirty`` and
        peaking at its centre.
    gain
        Loop gain (0 < gain <= 1). Smaller is more conservative/stable.
    n_iter
        Maximum number of CLEAN iterations.
    threshold
        Stop when the residual peak falls below this absolute value.

    Returns
    -------
    CleanResult
        The clean component model, the residual, and the component list.
    """
    residual = np.array(dirty, dtype=float, copy=True)
    model = np.zeros_like(residual)
    components: list[tuple[int, int, float]] = []
    beam_center = np.array(beam.shape) // 2

    for _ in range(n_iter):
        idx = np.unravel_index(np.argmax(np.abs(residual)), residual.shape)
        peak = residual[idx]
        if abs(peak) <= threshold:
            break
        flux = gain * peak
        model[idx] += flux
        components.append((int(idx[0]), int(idx[1]), float(flux)))
        # Subtract a shifted, scaled dirty beam centred on the found pixel.
        shift = (idx[0] - beam_center[0], idx[1] - beam_center[1])
        shifted_beam = np.roll(np.roll(beam, shift[0], axis=0), shift[1], axis=1)
        residual = residual - flux * shifted_beam

    return CleanResult(model=model, residual=residual, components=components)
