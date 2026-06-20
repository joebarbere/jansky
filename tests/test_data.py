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


def test_registry_well_formed():
    """Every entry has a valid category and a unique cache filename."""
    filenames = [d.filename for d in data.DATASETS.values()]
    assert len(filenames) == len(set(filenames)), "duplicate cache filenames"
    for spec in data.DATASETS.values():
        assert spec.category in {"small", "large"}
        assert spec.url.startswith("https://")


def test_small_datasets_are_the_default_path():
    """The real starter files are 'small'; HI4PI is demoted to 'large'."""
    small = data.small_datasets()
    assert "pint-ngc6440e-par" in small
    assert "psrfits-small" in small
    assert "filterbank-example" in small
    # The 576 MB map is no longer on the default (small) path.
    assert "hi4pi-sample" not in small
    assert data.DATASETS["hi4pi-sample"].category == "large"


def _online() -> bool:
    """Quick connectivity probe so the network test skips cleanly offline."""
    import urllib.request

    try:
        urllib.request.urlopen("https://raw.githubusercontent.com", timeout=5)
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _online(), reason="no network")
def test_fetch_small_real_file(tmp_path, monkeypatch):
    """A small real dataset downloads, caches, and is non-empty (network-gated)."""
    monkeypatch.setenv("JANSKY_DATA_DIR", str(tmp_path))
    path = data.fetch("pint-ngc6440e-par")
    assert path.exists()
    assert path.stat().st_size > 0
    # Cached: a second fetch returns the same path without re-downloading.
    assert data.fetch("pint-ngc6440e-par") == path


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
