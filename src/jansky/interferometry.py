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
    "simulate_coherent_channels",
    "cross_correlate",
    "calibrate_phases",
    "fringe_phase",
    "estimate_source_angle",
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


# --------------------------------------------------------------------------- #
# Coherent multi-receiver interferometry (e.g. KrakenSDR: 5 phase-coherent
# RTL-SDR channels on one clock). A point source's wavefront reaches receiver i
# at position x_i with a geometric phase 2*pi*x_i*sin(theta)/lambda; each
# receiver adds an unknown instrumental phase offset (the calibration problem).
# Cross-correlating two channels gives a complex "visibility" whose phase
# encodes the source direction once the instrumental offsets are removed.
# These power the KrakenSDR chapter and connect back to Chapters 7-8.
# --------------------------------------------------------------------------- #
def simulate_coherent_channels(
    positions: np.ndarray,
    source_angle: float,
    wavelength: float,
    n_samples: int = 4096,
    snr: float = 5.0,
    phase_offsets: np.ndarray | None = None,
    seed: int | None = 0,
) -> np.ndarray:
    """Simulate complex baseband from a coherent multi-receiver array.

    All receivers share one clock (as in a KrakenSDR), so they see a common
    source signal modulated by each receiver's geometric + instrumental phase.

    Parameters
    ----------
    positions
        1-D receiver positions along the array axis (same length unit as
        ``wavelength``), shape ``(n_rx,)``.
    source_angle
        Source angle from boresight (broadside), in radians.
    wavelength
        Observing wavelength.
    n_samples
        Number of complex samples per receiver.
    snr
        Voltage signal-to-noise ratio per receiver.
    phase_offsets
        Per-receiver instrumental phase offsets (radians). Default: zeros.
        Pass random offsets to exercise calibration.
    seed
        Seed for reproducibility.

    Returns
    -------
    numpy.ndarray
        Complex array ``(n_rx, n_samples)``.
    """
    positions = np.asarray(positions, dtype=float)
    n_rx = positions.size
    if phase_offsets is None:
        phase_offsets = np.zeros(n_rx)
    phase_offsets = np.asarray(phase_offsets, dtype=float)

    generator = _complex_rng(seed)
    # Common source signal (unit-power complex Gaussian) seen by every receiver.
    source = generator(n_samples)
    geometric = 2 * np.pi * positions * np.sin(source_angle) / wavelength
    total_phase = (geometric + phase_offsets)[:, None]
    signal = snr * source[None, :] * np.exp(1j * total_phase)
    noise = generator((n_rx, n_samples))
    return signal + noise


def cross_correlate(channel_a: np.ndarray, channel_b: np.ndarray) -> complex:
    """Complex visibility between two channels: ``<a · conj(b)>``."""
    return complex(np.mean(np.asarray(channel_a) * np.conj(np.asarray(channel_b))))


def calibrate_phases(
    channels: np.ndarray, reference: int = 0
) -> np.ndarray:
    """Estimate per-receiver instrumental phase offsets from a boresight source.

    With a calibration source on boresight (geometric phase = 0), the
    cross-correlation phase between receiver ``i`` and the reference is exactly
    the instrumental phase difference. Returns offsets *relative to* the
    reference receiver, suitable for subtracting before imaging.

    Parameters
    ----------
    channels
        ``(n_rx, n_samples)`` complex data of a boresight calibration source.
    reference
        Index of the reference receiver.

    Returns
    -------
    numpy.ndarray
        Estimated phase offsets (radians), ``offsets[reference] == 0``.
    """
    channels = np.asarray(channels)
    ref = channels[reference]
    return np.array([np.angle(cross_correlate(ch, ref)) for ch in channels])


def fringe_phase(baseline: float, source_angle: float, wavelength: float) -> float:
    """Expected interferometer fringe phase ``2*pi*b*sin(theta)/lambda`` (radians)."""
    return 2 * np.pi * baseline * np.sin(source_angle) / wavelength


def estimate_source_angle(
    channel_a: np.ndarray,
    channel_b: np.ndarray,
    baseline: float,
    wavelength: float,
) -> float:
    """Recover a source angle from the measured fringe phase of one baseline.

    Inverts :func:`fringe_phase`: ``theta = arcsin(phase * lambda / (2*pi*b))``.
    Unambiguous only for baselines shorter than ~lambda/2 (otherwise the phase
    wraps); longer baselines give finer resolution but aliased angles.
    """
    phase = np.angle(cross_correlate(channel_a, channel_b))
    arg = phase * wavelength / (2 * np.pi * baseline)
    return float(np.arcsin(np.clip(arg, -1.0, 1.0)))


def _complex_rng(seed: int | None = 0):
    """Return a function drawing unit-power complex Gaussian samples."""
    generator = np.random.default_rng(seed)

    def draw(size):
        return (generator.normal(0, 1 / np.sqrt(2), size)
                + 1j * generator.normal(0, 1 / np.sqrt(2), size))

    return draw
