"""Tests for jansky.timing -- Hellings-Downs and PTA simulation."""

from __future__ import annotations

import numpy as np

from jansky import timing


def test_hellings_downs_known_values():
    # Autocorrelation normalised to 1.
    assert timing.hellings_downs(0.0) == 1.0
    # Just above zero the cross-correlation approaches 1/2.
    assert np.isclose(timing.hellings_downs(1e-6), 0.5, atol=1e-3)
    # The curve dips negative near ~80-100 deg then rises toward 180 deg.
    g90 = timing.hellings_downs(np.radians(90.0))
    assert g90 < 0
    assert timing.hellings_downs(np.radians(180.0)) > g90


def test_angular_separations_matrix():
    pos = np.array([[1, 0, 0], [0, 1, 0], [-1, 0, 0]], dtype=float)
    sep = timing.angular_separations(pos)
    assert np.isclose(sep[0, 1], np.pi / 2)
    assert np.isclose(sep[0, 2], np.pi)
    assert np.allclose(np.diag(sep), 0.0)


def _random_sky(n, seed):
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((n, 3))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def test_pta_simulation_recovers_hellings_downs():
    pos = _random_sky(30, seed=1)
    res = timing.simulate_pta_residuals(
        pos, n_epochs=4000, gwb_amplitude=1.0, white_noise=0.1, seed=2
    )
    pc = timing.pairwise_correlations(res, pos)
    # Binned measured correlation should track the HD prediction (strong positive
    # correlation between the measured points and Gamma(theta)).
    predicted = timing.hellings_downs(pc.separations)
    r = np.corrcoef(pc.correlations, predicted)[0, 1]
    assert r > 0.7


def test_pta_residuals_shape():
    pos = _random_sky(12, seed=3)
    res = timing.simulate_pta_residuals(pos, n_epochs=100, seed=4)
    assert res.shape == (12, 100)
