"""Cached downloaders for the sample datasets used in the research chapters.

Two goals:

1. Make the research chapters reproducible -- everyone works from the same
   bytes, cached locally so you only download once.
2. Keep network access *explicit and inspectable*. Real archive access in the
   later chapters goes through ``astroquery``/``pyvo``; this module handles the
   handful of static sample files plus an offline synthetic fallback so the
   course still runs without a network connection.

Usage
-----
From Python::

    from jansky import data
    path = data.fetch("hi4pi-sample")

From the command line::

    python -m jansky.data --list
    python -m jansky.data --fetch hi4pi-sample
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

__all__ = [
    "DATASETS",
    "data_dir",
    "fetch",
    "list_datasets",
    "synthetic_hi_cube",
]


@dataclass(frozen=True)
class Dataset:
    """Metadata for a downloadable sample dataset."""

    name: str
    url: str
    filename: str
    description: str
    size_hint: str = "unknown"


# Registry of static sample datasets. Real, large archive queries are done with
# astroquery in the notebooks; these are small, stable starter files. When a URL
# is unavailable, fetch() raises with a clear message and points at the offline
# synthetic alternative where one exists.
DATASETS: dict[str, Dataset] = {
    "hi4pi-sample": Dataset(
        name="hi4pi-sample",
        url="https://lambda.gsfc.nasa.gov/data/foregrounds/HI4PI/NHI_HPX.fits",
        filename="HI4PI_NHI_HPX.fits",
        description="HI4PI all-sky neutral-hydrogen column-density map, HEALPix (HI 21cm).",
        size_hint="~576 MB",
    ),
}


def data_dir() -> Path:
    """Return the directory where datasets are cached.

    Defaults to ``<repo>/data``; override with the ``JANSKY_DATA_DIR`` env var.
    The directory is created on first use.
    """
    env = os.environ.get("JANSKY_DATA_DIR")
    if env:
        path = Path(env).expanduser()
    else:
        # src/jansky/data.py -> repo root is three parents up.
        path = Path(__file__).resolve().parents[2] / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_datasets() -> list[str]:
    """Return the names of all registered sample datasets."""
    return sorted(DATASETS)


def fetch(name: str, *, force: bool = False) -> Path:
    """Download (and cache) a registered dataset, returning its local path.

    Parameters
    ----------
    name
        A key from :data:`DATASETS`.
    force
        Re-download even if a cached copy exists.

    Returns
    -------
    pathlib.Path
        Path to the cached file.

    Raises
    ------
    KeyError
        If ``name`` is not a registered dataset.
    RuntimeError
        If the download fails (e.g. no network). The message suggests the
        offline synthetic alternative when one is available.
    """
    if name not in DATASETS:
        raise KeyError(
            f"Unknown dataset {name!r}. Known datasets: {', '.join(list_datasets())}"
        )
    spec = DATASETS[name]
    target = data_dir() / spec.filename
    if target.exists() and not force:
        return target

    try:
        _download(spec.url, target)
    except Exception as exc:  # noqa: BLE001 - re-raised with guidance below
        hint = (
            " For offline work, use jansky.data.synthetic_hi_cube() instead."
            if name == "hi4pi-sample"
            else ""
        )
        raise RuntimeError(
            f"Failed to download {name!r} from {spec.url}: {exc}.{hint}"
        ) from exc
    return target


def _download(url: str, target: Path) -> None:
    """Stream ``url`` to ``target`` with a progress bar, atomically."""
    import requests  # imported lazily so importing jansky stays cheap
    from tqdm import tqdm

    tmp = target.with_suffix(target.suffix + ".part")
    with requests.get(url, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        with open(tmp, "wb") as fh, tqdm(
            total=total, unit="B", unit_scale=True, desc=target.name
        ) as bar:
            for chunk in resp.iter_content(chunk_size=1 << 16):
                fh.write(chunk)
                bar.update(len(chunk))
    tmp.replace(target)


def synthetic_hi_cube(
    n_chan: int = 64,
    n_pix: int = 64,
    v_lsr: float = 0.0,
    seed: int | None = 0,
) -> np.ndarray:
    """Generate a small synthetic HI 21cm spectral-line cube for offline demos.

    Produces an emission feature whose centre velocity varies smoothly across
    the field (a toy galactic-rotation signature), plus noise. Useful when the
    real HI4PI file cannot be downloaded.

    Parameters
    ----------
    n_chan
        Number of spectral (velocity) channels.
    n_pix
        Spatial size (the cube is ``n_chan x n_pix x n_pix``).
    v_lsr
        Systemic velocity offset, in channel units.
    seed
        Seed for reproducible noise.

    Returns
    -------
    numpy.ndarray
        A ``(n_chan, n_pix, n_pix)`` brightness-temperature cube.
    """
    rng = np.random.default_rng(seed)
    channels = np.arange(n_chan)
    yy, xx = np.mgrid[0:n_pix, 0:n_pix]
    # Centre velocity sweeps with position to mimic differential rotation.
    centre = v_lsr + n_chan / 2 + 0.15 * (xx - n_pix / 2)
    width = 4.0
    cube = np.exp(
        -0.5 * ((channels[:, None, None] - centre[None, :, :]) / width) ** 2
    )
    cube += rng.normal(0.0, 0.02, size=cube.shape)
    return cube


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch jansky sample datasets.")
    parser.add_argument("--list", action="store_true", help="list known datasets")
    parser.add_argument("--fetch", metavar="NAME", help="download a dataset by name")
    parser.add_argument("--force", action="store_true", help="re-download if cached")
    args = parser.parse_args(argv)

    if args.list or not args.fetch:
        print(f"Cache directory: {data_dir()}")
        print("Available datasets:")
        for name in list_datasets():
            spec = DATASETS[name]
            print(f"  {name:18s} {spec.size_hint:>10s}  {spec.description}")
        if not args.fetch:
            return 0

    path = fetch(args.fetch, force=args.force)
    print(f"Ready: {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
