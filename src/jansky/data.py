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
    "small_datasets",
    "synthetic_hi_cube",
]


@dataclass(frozen=True)
class Dataset:
    """Metadata for a downloadable sample dataset.

    ``category`` is ``"small"`` for the real starter files the chapters reach for
    by default (mostly a couple of MB; the Radio JOVE ``.sps`` is the largest at
    ~12 MB) or ``"large"`` for opt-in bulk data that is never on the default/offline
    path.
    """

    name: str
    url: str
    filename: str
    description: str
    size_hint: str = "unknown"
    category: str = "small"


# Registry of static sample datasets. Real, large archive queries are done with
# astroquery in the notebooks; these are small, stable starter files served from
# stable raw-GitHub URLs. When a URL is unavailable, fetch() raises with a clear
# message and points at the offline synthetic alternative where one exists.
#
# The "small" entries are real bytes under ~2 MB so the research chapters can read
# an actual file rather than always falling back to simulation. The 576 MB HI4PI
# all-sky map is kept as an opt-in "large" entry, off the default path.
DATASETS: dict[str, Dataset] = {
    # --- small, real starter files (the default path; all < 2 MB) ---
    "psrfits-small": Dataset(
        name="psrfits-small",
        url="https://raw.githubusercontent.com/thepetabyteproject/your/main/tests/data/small.fits",
        filename="your_small.fits",
        description="Small real search-mode PSRFITS file (from the `your` test suite).",
        size_hint="~278 KB",
    ),
    "filterbank-small": Dataset(
        name="filterbank-small",
        url="https://raw.githubusercontent.com/thepetabyteproject/your/main/tests/data/small.fil",
        filename="your_small.fil",
        description="Small real SIGPROC filterbank file (from the `your` test suite).",
        size_hint="~4 KB",
    ),
    "filterbank-example": Dataset(
        name="filterbank-example",
        url="https://raw.githubusercontent.com/thepetabyteproject/your/main/tests/data/28.fil",
        filename="your_28.fil",
        description="The `your` example SIGPROC filterbank (real search-mode data) — "
        "large enough to de-disperse and inspect in Chapter 13.",
        size_hint="~1.6 MB",
    ),
    "pint-ngc6440e-par": Dataset(
        name="pint-ngc6440e-par",
        url="https://raw.githubusercontent.com/nanograv/PINT/master/src/pint/data/examples/NGC6440E.par",
        filename="NGC6440E.par",
        description="Timing model (.par) for PSR J1748-2021E in NGC 6440 — real NANOGrav "
        "data (PINT example); pairs with pint-ngc6440e-tim.",
        size_hint="~0.5 KB",
    ),
    "pint-ngc6440e-tim": Dataset(
        name="pint-ngc6440e-tim",
        url="https://raw.githubusercontent.com/nanograv/PINT/master/src/pint/data/examples/NGC6440E.tim",
        filename="NGC6440E.tim",
        description="TOAs (.tim) for PSR J1748-2021E in NGC 6440 — real NANOGrav data "
        "(PINT example); pairs with pint-ngc6440e-par.",
        size_hint="~4 KB",
    ),
    "radiojove-sps": Dataset(
        name="radiojove-sps",
        url="https://maser.obspm.fr/data/maser4py/tests/data/radiojove/sps/161210000000.sps",
        filename="radiojove_aj4co_20161210.sps",
        description="Real Radio JOVE Radio-Sky Spectrograph (.sps) recording — a "
        "dual-polarisation 16-32 MHz Jupiter/solar dynamic spectrum (AJ4CO/Typinski, "
        "2016-12-10); read with jansky.formats.read_sps.",
        size_hint="~12 MB",
    ),
    "vla-uvfits": Dataset(
        name="vla-uvfits",
        url="https://raw.githubusercontent.com/RadioAstronomySoftwareGroup/rasg-datasets/main/visibility_data/VLA/day2_TDEM0003_10s_norx_1src_1spw.uvfits",
        filename="vla_day2_TDEM0003_1src_1spw.uvfits",
        description="Real (E)VLA continuum visibilities (UVFITS) — the CASA-guides "
        "day2_TDEM0003 dataset: calibrator J1008+0730 at ~36 GHz, 18 antennas; "
        "inspect with pyuvdata (the `formats` extra), no CASA container needed.",
        size_hint="~4 MB",
    ),
    # --- large, opt-in (never on the default/offline path) ---
    "hi4pi-sample": Dataset(
        name="hi4pi-sample",
        url="https://lambda.gsfc.nasa.gov/data/foregrounds/HI4PI/NHI_HPX.fits",
        filename="HI4PI_NHI_HPX.fits",
        description="HI4PI all-sky neutral-hydrogen column-density map, HEALPix (HI 21cm). "
        "Large — prefer jansky.data.synthetic_hi_cube() for offline work.",
        size_hint="~576 MB",
        category="large",
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


def small_datasets() -> list[str]:
    """Return the names of the real starter datasets (the default path).

    These are the small real files the research chapters reach for, so they can
    read a real file offline-cached rather than always simulating. All are a few
    MB at most (the Radio JOVE ``.sps`` is the largest at ~12 MB).
    """
    return sorted(n for n, d in DATASETS.items() if d.category == "small")


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
        raise KeyError(f"Unknown dataset {name!r}. Known datasets: {', '.join(list_datasets())}")
    spec = DATASETS[name]
    target = data_dir() / spec.filename
    if target.exists() and not force:
        return target

    try:
        _download(spec.url, target)
    except Exception as exc:  # noqa: BLE001 - re-raised with guidance below
        if name == "hi4pi-sample":
            hint = " For offline work, use jansky.data.synthetic_hi_cube() instead."
        elif spec.category == "small":
            hint = " The chapters fall back to simulated data when this is unavailable offline."
        else:
            hint = ""
        raise RuntimeError(f"Failed to download {name!r} from {spec.url}: {exc}.{hint}") from exc
    return target


def _download(url: str, target: Path) -> None:
    """Stream ``url`` to ``target`` with a progress bar, atomically."""
    import requests  # imported lazily so importing jansky stays cheap
    from tqdm import tqdm

    tmp = target.with_suffix(target.suffix + ".part")
    with requests.get(url, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        with (
            open(tmp, "wb") as fh,
            tqdm(total=total, unit="B", unit_scale=True, desc=target.name) as bar,
        ):
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
    cube = np.exp(-0.5 * ((channels[:, None, None] - centre[None, :, :]) / width) ** 2)
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
        # Small real starter files first (the default path), then opt-in large data.
        for category, heading in (
            ("small", "Small real starter files"),
            ("large", "Large (opt-in)"),
        ):
            names = [n for n in list_datasets() if DATASETS[n].category == category]
            if not names:
                continue
            print(f"\n{heading}:")
            for name in names:
                spec = DATASETS[name]
                print(f"  {name:20s} {spec.size_hint:>10s}  {spec.description}")
        if not args.fetch:
            return 0

    path = fetch(args.fetch, force=args.force)
    print(f"Ready: {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
