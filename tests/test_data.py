"""Tests for jansky.data -- the dataset registry and offline fallbacks.

These tests do not hit the network; they exercise the registry, the cache-path
logic, and the synthetic fallback generator.
"""

from __future__ import annotations

import numpy as np
import pytest

from jansky import data


def test_registry_not_empty():
    names = data.list_datasets()
    assert "hi4pi-sample" in names


def test_data_dir_respects_env(tmp_path, monkeypatch):
    monkeypatch.setenv("JANSKY_DATA_DIR", str(tmp_path / "cache"))
    d = data.data_dir()
    assert d.exists()
    assert d == (tmp_path / "cache")


def test_fetch_unknown_raises():
    with pytest.raises(KeyError):
        data.fetch("does-not-exist")


def test_synthetic_hi_cube_shape_and_finiteness():
    cube = data.synthetic_hi_cube(n_chan=32, n_pix=16, seed=0)
    assert cube.shape == (32, 16, 16)
    assert np.all(np.isfinite(cube))
    # There is real signal: the peak sits well above the noise floor.
    assert cube.max() > 0.5


def test_synthetic_hi_cube_reproducible():
    a = data.synthetic_hi_cube(seed=42)
    b = data.synthetic_hi_cube(seed=42)
    assert np.array_equal(a, b)
