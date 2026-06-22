"""Tests for jansky.interferometry -- uv-coverage, dirty beam, CLEAN."""

from __future__ import annotations

import numpy as np

from jansky import interferometry


def _toy_array():
    return np.array([[0, 0], [10, 0], [0, 12], [7, 7], [-9, 3]], dtype=float)


def test_uv_coverage_is_hermitian():
    """Every (u, v) sample has its conjugate (-u, -v)."""
    uv = interferometry.uv_coverage(_toy_array())
    # Sum of all points should cancel to zero by conjugate symmetry.
    assert np.allclose(uv.sum(axis=0), 0.0)
    # n_baselines * 2 conjugates * n_hour_angles(=1) samples.
    n_ant = 5
    assert uv.shape == (n_ant * (n_ant - 1) // 2 * 2, 2)


def test_earth_rotation_increases_coverage():
    arr = _toy_array()
    snap = interferometry.uv_coverage(arr)
    track = interferometry.uv_coverage(arr, hour_angles=np.linspace(-1, 1, 30))
    assert track.shape[0] > snap.shape[0]


def test_dirty_beam_peaks_at_centre():
    uv = interferometry.uv_coverage(_toy_array(), np.linspace(-1, 1, 40))
    mask = interferometry.grid_visibilities(uv, npix=64)
    beam = interferometry.dirty_beam(mask)
    peak = np.unravel_index(np.argmax(beam), beam.shape)
    assert peak == (32, 32)
    assert np.isclose(beam[peak], 1.0)


def test_clean_recovers_point_source():
    """CLEAN should place its brightest component on the true source pixel."""
    npix = 64
    sky = np.zeros((npix, npix))
    sky[20, 40] = 1.0
    uv = interferometry.uv_coverage(_toy_array(), np.linspace(-1, 1, 40))
    mask = interferometry.grid_visibilities(uv, npix=npix)
    beam = interferometry.dirty_beam(mask)
    dirty = interferometry.dirty_image(sky, mask)
    result = interferometry.hogbom_clean(dirty, beam, gain=0.2, n_iter=300)
    recovered = np.unravel_index(np.argmax(result.model), result.model.shape)
    assert recovered == (20, 40)
    # Residual peak is much smaller than the original dirty-image peak.
    assert np.abs(result.residual).max() < 0.5 * np.abs(dirty).max()


def test_clean_threshold_stops_early():
    dirty = np.zeros((32, 32))
    dirty[16, 16] = 1.0
    beam = np.zeros((32, 32))
    beam[16, 16] = 1.0
    result = interferometry.hogbom_clean(dirty, beam, gain=0.5, n_iter=1000, threshold=0.1)
    # With a clean delta beam, geometric decay stops once peak < 0.1.
    assert np.abs(result.residual).max() <= 0.1


def test_coherent_calibration_recovers_offsets():
    import numpy as np

    lam = 1.0
    pos = np.arange(5) * 0.5
    offsets = np.array([0.0, 1.2, -0.7, 2.5, -1.9])
    cal = interferometry.simulate_coherent_channels(
        pos, 0.0, lam, snr=30, phase_offsets=offsets, seed=1
    )
    est = interferometry.calibrate_phases(cal)
    # wrap difference into (-pi, pi]; should be tiny at high SNR
    err = np.angle(np.exp(1j * (est - offsets)))
    assert np.max(np.abs(err)) < 0.02


def test_coherent_recovers_source_angle():
    import numpy as np

    lam = 1.0
    pos = np.arange(5) * 0.5
    offsets = np.array([0.0, 1.2, -0.7, 2.5, -1.9])
    true_angle = np.radians(18.0)
    cal = interferometry.simulate_coherent_channels(
        pos, 0.0, lam, snr=30, phase_offsets=offsets, seed=1
    )
    est = interferometry.calibrate_phases(cal)
    obs = interferometry.simulate_coherent_channels(
        pos, true_angle, lam, snr=30, phase_offsets=offsets, seed=2
    )
    corr = obs * np.exp(-1j * est)[:, None]
    angle = interferometry.estimate_source_angle(corr[1], corr[0], baseline=0.5, wavelength=lam)
    assert abs(np.degrees(angle) - 18.0) < 1.0


def test_fringe_phase_zero_on_boresight():
    import numpy as np

    assert interferometry.fringe_phase(2.0, 0.0, 0.21) == 0.0
    # and matches 2*pi*b*sin(theta)/lambda
    val = interferometry.fringe_phase(2.0, np.radians(30), 0.21)
    assert np.isclose(val, 2 * np.pi * 2.0 * 0.5 / 0.21)


def test_closure_phase_invariant_to_station_phases():
    import numpy as np

    rng = np.random.default_rng(7)
    # true visibilities on a triangle (i,j,k)
    v = {k: complex(rng.normal(), rng.normal()) for k in ("ij", "jk", "ki")}
    cp_true = interferometry.closure_phase(v["ij"], v["jk"], v["ki"])
    # corrupt with per-station phases: V_ab -> e^{i(pa - pb)} V_ab
    p = {s: rng.uniform(-np.pi, np.pi) for s in "ijk"}
    vij = np.exp(1j * (p["i"] - p["j"])) * v["ij"]
    vjk = np.exp(1j * (p["j"] - p["k"])) * v["jk"]
    vki = np.exp(1j * (p["k"] - p["i"])) * v["ki"]
    cp_corrupt = interferometry.closure_phase(vij, vjk, vki)
    assert np.isclose(np.angle(np.exp(1j * (cp_true - cp_corrupt))), 0.0, atol=1e-9)


def test_closure_amplitude_invariant_to_station_gains():
    import numpy as np

    rng = np.random.default_rng(8)
    v = {k: complex(rng.normal(), rng.normal()) for k in ("ij", "kl", "ik", "jl")}
    ca_true = interferometry.closure_amplitude(v["ij"], v["kl"], v["ik"], v["jl"])
    a = {s: rng.uniform(0.5, 2.0) for s in "ijkl"}  # per-station amplitude errors
    vij = a["i"] * a["j"] * v["ij"]
    vkl = a["k"] * a["l"] * v["kl"]
    vik = a["i"] * a["k"] * v["ik"]
    vjl = a["j"] * a["l"] * v["jl"]
    ca_corrupt = interferometry.closure_amplitude(vij, vkl, vik, vjl)
    assert np.isclose(ca_true, ca_corrupt, rtol=1e-12)


def test_hbt_g2_limits():
    import numpy as np

    lam, theta = 1.0, 1e-3
    assert np.isclose(interferometry.disk_visibility(0.0, theta, lam), 1.0)
    assert np.isclose(interferometry.hbt_g2(0.0, theta, lam), 2.0)
    # at a large baseline the source is resolved -> g2 approaches 1
    assert interferometry.hbt_g2(50_000.0, theta, lam) < 1.05


def test_disk_visibility_first_null():
    import numpy as np

    lam, theta = 1.0, 1e-3
    b_null = 3.8317 * lam / (np.pi * theta)  # first zero of 2 J1(x)/x
    assert abs(interferometry.disk_visibility(b_null, theta, lam)) < 1e-3


def test_solve_point_source_gains_recovers_gains():
    import numpy as np

    rng = np.random.default_rng(11)
    g = rng.uniform(0.5, 2.0, 6) * np.exp(1j * rng.uniform(-np.pi, np.pi, 6))
    g = g * np.exp(-1j * np.angle(g[0]))  # reference phase
    vis = np.outer(g, np.conj(g))
    recovered = interferometry.solve_point_source_gains(vis)
    assert np.allclose(recovered, g, atol=1e-6)


def _random_gains(rng, n):
    g = rng.uniform(0.5, 2.0, n) * np.exp(1j * rng.uniform(-np.pi, np.pi, n))
    return g * np.exp(-1j * np.angle(g[0]))  # reference phase: g[0] real positive


def test_apply_gains_matches_measurement_equation():
    rng = np.random.default_rng(2)
    g = _random_gains(rng, 5)
    model = np.ones((5, 5), dtype=complex)
    obs = interferometry.apply_gains(model, g)
    # V_obs_ij = g_i conj(g_j); diagonal is |g_i|^2; matrix is Hermitian.
    assert np.allclose(obs, np.outer(g, np.conj(g)))
    assert np.allclose(np.diag(obs), np.abs(g) ** 2)
    assert np.allclose(obs, obs.conj().T)


def test_stefcal_recovers_point_source_gains():
    rng = np.random.default_rng(7)
    g = _random_gains(rng, 8)
    model = np.ones((8, 8), dtype=complex)
    obs = interferometry.apply_gains(model, g)
    recovered = interferometry.solve_gains_stefcal(obs, model)
    assert np.allclose(recovered, g, atol=1e-6)
    # Agrees with the eigen-solver on a point source.
    assert np.allclose(recovered, interferometry.solve_point_source_gains(obs), atol=1e-6)


def test_stefcal_recovers_gains_on_a_resolved_model():
    # A general (resolved-source) Hermitian model, not just a point source.
    rng = np.random.default_rng(20)
    n = 7
    base = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    model = base + base.conj().T  # Hermitian model visibilities
    g = _random_gains(rng, n)
    obs = interferometry.apply_gains(model, g)
    recovered = interferometry.solve_gains_stefcal(obs, model)
    # Correcting the observed data by the recovered gains returns the model.
    corrected = interferometry.apply_gains(obs, 1.0 / recovered)
    off = ~np.eye(n, dtype=bool)
    assert np.allclose(corrected[off], model[off], atol=1e-6)


def test_stefcal_is_robust_to_noise():
    rng = np.random.default_rng(31)
    g = _random_gains(rng, 10)
    model = np.ones((10, 10), dtype=complex)
    obs = interferometry.apply_gains(model, g)
    noise = 0.02 * (rng.normal(size=obs.shape) + 1j * rng.normal(size=obs.shape))
    noise = noise + noise.conj().T
    recovered = interferometry.solve_gains_stefcal(obs + noise, model)
    # Recovered gains stay close to truth despite 2% visibility noise.
    assert np.max(np.abs(recovered - g)) < 0.1


def _random_dterms(rng, n, scale=0.05):
    # Reference antenna 0 has zero leakage (the gauge); the rest are a few percent.
    d = scale * (rng.normal(size=n) + 1j * rng.normal(size=n))
    d[0] = 0.0
    return d


def test_apply_leakage_structure():
    d = np.array([0.0, 0.03 + 0.01j, -0.02 + 0.04j])
    v = interferometry.apply_leakage(2.0, d)
    # V_RL_ij = (d_i + conj(d_j)) * I; diagonal is 2 Re(d_i) * I.
    assert np.allclose(v, (d[:, None] + np.conj(d)[None, :]) * 2.0)
    assert np.allclose(np.diag(v), 2.0 * d.real * 2.0)


def test_solve_leakage_recovers_dterms():
    rng = np.random.default_rng(5)
    d = _random_dterms(rng, 7)
    v = interferometry.apply_leakage(3.0, d)
    recovered = interferometry.solve_leakage(v, 3.0)
    assert np.allclose(recovered, d, atol=1e-9)
    assert recovered[0] == 0.0  # reference-antenna gauge


def test_solve_leakage_robust_to_noise_and_corrects():
    rng = np.random.default_rng(8)
    d = _random_dterms(rng, 9)
    v = interferometry.apply_leakage(1.0, d)
    noise = 0.002 * (rng.normal(size=v.shape) + 1j * rng.normal(size=v.shape))
    recovered = interferometry.solve_leakage(v + noise, 1.0)
    assert np.max(np.abs(recovered - d)) < 0.02
    # Correcting the observed cross-hand by the recovered D-terms collapses the
    # off-diagonal leakage toward zero (an unpolarised source has no true cross-hand).
    corrected = (v + noise) - interferometry.apply_leakage(1.0, recovered)
    off = ~np.eye(9, dtype=bool)
    assert np.std(corrected[off]) < 0.01
