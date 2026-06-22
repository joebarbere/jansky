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
from scipy import special

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
    "closure_phase",
    "closure_amplitude",
    "disk_visibility",
    "hbt_g2",
    "solve_point_source_gains",
    "apply_gains",
    "solve_gains_stefcal",
    "apply_leakage",
    "solve_leakage",
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


def calibrate_phases(channels: np.ndarray, reference: int = 0) -> np.ndarray:
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
        return generator.normal(0, 1 / np.sqrt(2), size) + 1j * generator.normal(
            0, 1 / np.sqrt(2), size
        )

    return draw


# --------------------------------------------------------------------------- #
# Closure quantities (VLBI / the Event Horizon Telescope). A measured visibility
# carries per-station corruptions: V_ij_meas = g_i g_j* V_ij, where g = a e^{i*phi}.
# Certain products of visibilities cancel those station terms exactly:
#   - closure phase  (triangle i,j,k): arg(V_ij V_jk V_ki) is free of station PHASES;
#   - closure amplitude (quad i,j,k,l): |V_ij||V_kl| / (|V_ik||V_jl|) is free of station GAINS.
# They are the robust observables that let sparse global arrays image black holes.
# --------------------------------------------------------------------------- #
def closure_phase(v_ij: complex, v_jk: complex, v_ki: complex) -> float:
    """Closure phase of a station triangle: ``arg(V_ij · V_jk · V_ki)`` (radians).

    Invariant to per-station phase errors, because each station's phase appears
    once with each sign around the loop and cancels.
    """
    return float(np.angle(v_ij * v_jk * v_ki))


def closure_amplitude(v_ij: complex, v_kl: complex, v_ik: complex, v_jl: complex) -> float:
    """Closure amplitude of a station quadrangle: ``|V_ij||V_kl| / (|V_ik||V_jl|)``.

    Invariant to per-station amplitude (gain) errors, which cancel between
    numerator and denominator.
    """
    denom = abs(v_ik) * abs(v_jl)
    if denom == 0:
        raise ValueError("closure amplitude undefined (zero denominator visibility)")
    return float(abs(v_ij) * abs(v_kl) / denom)


# --------------------------------------------------------------------------- #
# Intensity interferometry (Hanbury Brown & Twiss, 1954). Instead of combining
# amplitude+phase, HBT correlates the INTENSITY fluctuations at two detectors.
# For chaotic (thermal) light the excess correlation is g2(b) = 1 + |V(b)|^2,
# where V(b) is the ordinary van Cittert-Zernike visibility. So measuring g2 vs
# baseline recovers |V|^2 and hence the source's angular size -- with timing only
# needing to match the bandwidth, not the phase. This sidesteps the phase-
# coherence problem that makes amplitude VLBI so hard (see field-notes.md).
# --------------------------------------------------------------------------- #
def disk_visibility(baseline: np.ndarray, angular_diameter: float, wavelength: float) -> np.ndarray:
    """Van Cittert--Zernike visibility of a uniform circular disk.

    :math:`V(b) = 2 J_1(x)/x` with :math:`x = \\pi\\,\\theta\\,b/\\lambda`, where
    :math:`\\theta` is the disk's angular diameter, ``b`` the baseline, and
    :math:`\\lambda` the wavelength (consistent units). The first zero at
    :math:`x=3.83` gives the classic resolution :math:`b \\approx 1.22\\lambda/\\theta`.
    """
    x = np.pi * angular_diameter * np.asarray(baseline, dtype=float) / wavelength
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(x == 0.0, 1.0, 2.0 * special.j1(x) / x)


def hbt_g2(baseline: np.ndarray, angular_diameter: float, wavelength: float) -> np.ndarray:
    """HBT second-order (intensity) correlation :math:`g^{(2)}(b) = 1 + |V(b)|^2`.

    Equals 2 at zero baseline (a fully correlated source) and falls to 1 as the
    baseline resolves the source. Fitting a measured ``g2`` curve recovers the
    angular diameter -- the principle behind Hanbury Brown & Twiss's stellar
    intensity interferometer.
    """
    return 1.0 + disk_visibility(baseline, angular_diameter, wavelength) ** 2


# --------------------------------------------------------------------------- #
# Gain calibration as linear algebra (the calibration Maths Lab). A measured
# visibility matrix of an unresolved calibrator is V_ij = g_i g_j^*, i.e. the
# outer product g g^H -- a rank-1 Hermitian matrix. So the complex per-antenna
# gains are recovered from its leading eigenvector (up to one global phase).
# Real packages (CASA, StefCal) generalise this to resolved models and noise.
# --------------------------------------------------------------------------- #
def solve_point_source_gains(vis: np.ndarray) -> np.ndarray:
    """Recover complex antenna gains from a point-source visibility matrix.

    For an unresolved calibrator, ``V = g gᴴ``; the gains are the top eigenvector
    of the Hermitian ``V`` scaled by the square root of its (positive) leading
    eigenvalue. The solution is determined only up to a global phase, so the
    result is rotated to make ``g[0]`` real and positive.

    Parameters
    ----------
    vis
        ``(n_ant, n_ant)`` complex visibility matrix of a point source.

    Returns
    -------
    numpy.ndarray
        Complex per-antenna gains, ``(n_ant,)``.
    """
    vis = np.asarray(vis, dtype=complex)
    # Use the magnitude of the largest-|eigenvalue| eigenpair.
    evals, evecs = np.linalg.eigh(vis)
    top = int(np.argmax(np.abs(evals)))
    gains = evecs[:, top] * np.sqrt(abs(evals[top]))
    # Fix the global phase so g[0] is real positive.
    if gains[0] != 0:
        gains = gains * np.exp(-1j * np.angle(gains[0]))
    return gains


def apply_gains(vis_model: np.ndarray, gains: np.ndarray) -> np.ndarray:
    """Corrupt model visibilities with per-antenna complex gains (the forward model).

    Applies the radio-interferometer measurement equation
    :math:`V^\\mathrm{obs}_{ij} = g_i\\,V^\\mathrm{model}_{ij}\\,g_j^{*}`, i.e.
    ``diag(g) · V · diag(g)ᴴ``. Inverting this -- solving for the gains and dividing
    them out -- is what calibration does.

    Parameters
    ----------
    vis_model
        ``(n_ant, n_ant)`` true/model visibility matrix.
    gains
        ``(n_ant,)`` complex per-antenna gains.

    Returns
    -------
    numpy.ndarray
        The corrupted ``(n_ant, n_ant)`` visibility matrix.
    """
    g = np.asarray(gains, dtype=complex)
    v = np.asarray(vis_model, dtype=complex)
    return g[:, None] * v * np.conj(g)[None, :]


def solve_gains_stefcal(
    vis_obs: np.ndarray,
    vis_model: np.ndarray,
    n_iter: int = 100,
    tol: float = 1e-10,
) -> np.ndarray:
    """Solve antenna gains against a sky model (the StefCal algorithm).

    Given observed visibilities :math:`V^\\mathrm{obs}` and a model
    :math:`V^\\mathrm{model}`, find the per-antenna complex gains minimising
    :math:`\\sum_{i\\neq j} |V^\\mathrm{obs}_{ij} - g_i\\,V^\\mathrm{model}_{ij}\\,g_j^{*}|^2`.
    Each iteration updates every antenna in closed form,
    :math:`g_i = \\sum_{j\\neq i} V^\\mathrm{obs}_{ij}\\,z_j^{*} / \\sum_{j\\neq i}|z_j|^2`
    with :math:`z_j = g_j^{*}\\,V^\\mathrm{model}_{ij}`, then averages successive iterates
    for stability (Mitchell et al. 2008; Salvini & Wijnholds 2014). This is the engine
    of both gain calibration (model = a calibrator) and self-calibration (model = the
    current image); for a point source it agrees with
    :func:`solve_point_source_gains`.

    Parameters
    ----------
    vis_obs
        ``(n_ant, n_ant)`` observed (corrupted) visibility matrix.
    vis_model
        ``(n_ant, n_ant)`` model visibility matrix (e.g. ``np.ones`` for a point source).
    n_iter
        Maximum number of iterations.
    tol
        Convergence tolerance on the fractional gain change.

    Returns
    -------
    numpy.ndarray
        Complex per-antenna gains, ``(n_ant,)``, with ``g[0]`` rotated real-positive.
    """
    vobs = np.asarray(vis_obs, dtype=complex)
    vmod = np.asarray(vis_model, dtype=complex)
    n = vobs.shape[0]
    off = ~np.eye(n, dtype=bool)  # exclude autocorrelations from the solve
    gains = np.ones(n, dtype=complex)
    for _it in range(n_iter):
        g_new = gains.copy()
        for i in range(n):
            z = np.conj(gains) * vmod[i, :]  # z_j = conj(g_j) * V_model_ij
            num = np.sum((vobs[i, :] * np.conj(z))[off[i]])
            den = np.sum((np.abs(z) ** 2)[off[i]])
            if den > 0:
                g_new[i] = num / den
        # StefCal stabilisation: average the new iterate with the old.
        updated = 0.5 * (gains + g_new)
        change = np.linalg.norm(updated - gains) / (np.linalg.norm(gains) + 1e-30)
        gains = updated
        if change < tol:
            break
    if gains[0] != 0:
        gains = gains * np.exp(-1j * np.angle(gains[0]))
    return gains


def apply_leakage(stokes_i: float, d_terms: np.ndarray) -> np.ndarray:
    """Cross-hand visibilities of an unpolarised source under per-antenna leakage (D-terms).

    Real feeds are never perfectly orthogonal: a small fraction of one polarisation
    "leaks" into the other (the instrumental **D-terms**). To first order, the cross-hand
    correlation of an **unpolarised** calibrator (Stokes :math:`Q = U = V = 0`, only
    :math:`I`) is pure leakage,

    .. math:: V^{RL}_{ij} \\approx (d_i + d_j^{*})\\, I,

    where :math:`d_i` is antenna :math:`i`'s complex leakage. This is the polarisation
    analogue of :func:`apply_gains`; solving it (:func:`solve_leakage`) is polarisation
    calibration. (A teaching first-order model with one leakage per antenna; real packages
    such as CASA's ``polcal`` solve the two feeds separately and include the source's own
    polarisation.)

    Parameters
    ----------
    stokes_i
        The calibrator's Stokes I flux (arbitrary units).
    d_terms
        ``(n_ant,)`` complex per-antenna leakage factors (typically a few percent).

    Returns
    -------
    numpy.ndarray
        The ``(n_ant, n_ant)`` cross-hand visibility matrix.
    """
    d = np.asarray(d_terms, dtype=complex)
    return (d[:, None] + np.conj(d)[None, :]) * stokes_i


def solve_leakage(vis_rl: np.ndarray, stokes_i: float) -> np.ndarray:
    """Recover per-antenna D-terms from an unpolarised calibrator's cross-hand visibilities.

    Inverts :func:`apply_leakage`: given :math:`V^{RL}_{ij} = (d_i + d_j^{*})\\,I`, solve
    the (linear) least-squares system for the per-antenna leakages, gauge-fixed to a
    reference antenna with ``d[0] = 0`` (an unpolarised calibrator alone cannot constrain
    the absolute R--L phase, exactly as gain calibration cannot constrain the global phase
    in :func:`solve_gains_stefcal` — an angle calibrator supplies it).

    Parameters
    ----------
    vis_rl
        ``(n_ant, n_ant)`` cross-hand visibility matrix of an unpolarised calibrator.
    stokes_i
        The calibrator's Stokes I flux.

    Returns
    -------
    numpy.ndarray
        Complex per-antenna D-terms ``(n_ant,)`` with ``d[0] = 0`` (reference antenna).
    """
    m = np.asarray(vis_rl, dtype=complex) / stokes_i  # m_ij = d_i + conj(d_j)
    n = m.shape[0]
    n_un = n - 1  # antenna 0 is the reference gauge (d_0 = 0)
    rows: list[np.ndarray] = []
    rhs: list[float] = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # Real part:  Re(d_i) + Re(d_j) = Re(m_ij)
            r = np.zeros(2 * n_un)
            if i > 0:
                r[i - 1] += 1.0
            if j > 0:
                r[j - 1] += 1.0
            rows.append(r)
            rhs.append(m[i, j].real)
            # Imag part:  Im(d_i) - Im(d_j) = Im(m_ij)
            r2 = np.zeros(2 * n_un)
            if i > 0:
                r2[n_un + i - 1] += 1.0
            if j > 0:
                r2[n_un + j - 1] -= 1.0
            rows.append(r2)
            rhs.append(m[i, j].imag)
    sol, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
    d = np.zeros(n, dtype=complex)
    for a in range(1, n):
        d[a] = sol[a - 1] + 1j * sol[n_un + a - 1]
    return d
