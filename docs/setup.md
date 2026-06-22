# Setup

You can run the course two ways: **locally with [uv](https://docs.astral.sh/uv/)** (fast,
recommended for most chapters) or **in containers** (best for the heavy, system-level tools
in Chapters 5–6 and 12). Pick whichever suits you; you can mix and match.

## Option A — Local with uv

uv manages the Python version and the virtual environment for you.

```bash
# 1. Install uv (see https://docs.astral.sh/uv/ for other methods)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and enter the project
git clone https://github.com/joebarbere/jansky.git
cd jansky

# 3. Create the environment (pins Python 3.12 automatically)
uv sync

# 4. Launch JupyterLab and open notebooks/01_what_is_radio_astronomy.ipynb
uv run jupyter lab
```

### Optional feature sets

Some chapters use heavier libraries kept in optional extras so the base install stays light:

```bash
uv sync --extra pulsar     # Chapter 13: pint-pulsar, your
uv sync --extra dynamics   # Chapter 11: galpy
uv sync --extra sdr        # Chapters 5–6: pyrtlsdr (needs system librtlsdr)
uv sync --extra cmb        # Chapter 22: healpy (all-sky HEALPix maps & power spectra)
```

!!! note "Python version"
    The environment pins **Python 3.12**, not your system Python. CASA
    (`casatools`/`casatasks`, used in Chapter 12) supports only Python ≤ 3.12, and
    many astronomy wheels lag the newest releases. uv downloads 3.12 for you.

## Option B — Containers (podman or docker)

The default `lab` service builds the same environment as `uv sync` and serves JupyterLab:

```bash
# From the repo root. Works with `docker compose` too.
podman compose -f containers/compose.yaml up lab
# then open http://localhost:8888
```

Chapter-specific images are behind compose **profiles** so they don't build by default:

```bash
# Chapter 12 — CASA / VLA imaging
podman compose -f containers/compose.yaml --profile interferometry up casa   # :8889

# Chapters 5–6 — GNU Radio / SDR (pass a USB SDR through with --device)
podman compose -f containers/compose.yaml --profile sdr up gnuradio          # :8890
```

## Datasets

The research chapters pull from open archives at runtime (via `astroquery`/`pyvo`) and
from a small set of cached sample files. The helper module manages the cache:

```bash
uv run python -m jansky.data --list                 # see available sample datasets
uv run python -m jansky.data --fetch hi4pi-sample   # download + cache one
```

Downloads land in `data/` (override with the `JANSKY_DATA_DIR` environment variable).
Every download has an offline synthetic fallback so the course still runs without a
network connection — see `jansky.data.synthetic_hi_cube()`.

## Sanity check

```bash
uv run python -c "import jansky; print(jansky.__version__)"
uv run pytest          # runs the helper-package tests
uv run ruff check .    # lint
```

If those pass, you're ready. Open [Chapter 1](notebooks/01_what_is_radio_astronomy.ipynb).
