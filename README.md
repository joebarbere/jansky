# jansky

**A hands-on radio astronomy course in Python** — from *"what is a radio wave from space?"*
to *downloading real telescope data and doing original analysis*.

Named after [Karl Jansky](https://en.wikipedia.org/wiki/Karl_Guthe_Jansky), who in 1932
discovered radio emission from the Milky Way (and after whom the unit of radio brightness,
the **jansky**, is named), this course teaches the fundamentals of radio astronomy through
executable Jupyter notebooks that mix prose, the physics (with equations), runnable code,
and plots — each chapter citing the seminal papers so you can read the originals.

Every chapter uses the real libraries working astronomers use — `astropy`, `astroquery`,
`spectral-cube`, CASA, PINT — so you build transferable skills, not toy ones.

## Quickstart

### Local (recommended)

```bash
# Install uv: https://docs.astral.sh/uv/
curl -LsSf https://astral.sh/uv/install.sh | sh

git clone https://github.com/joebarbere/jansky.git
cd jansky
uv sync                 # creates the env, pins Python 3.12
uv run jupyter lab      # open notebooks/01_what_is_radio_astronomy.ipynb
```

### Containers (podman or docker)

```bash
podman compose -f containers/compose.yaml up lab     # JupyterLab at http://localhost:8888
```

Heavy, chapter-specific tools live in their own images behind compose profiles
(`--profile interferometry` for CASA, `--profile sdr` for GNU Radio). See
[docs/setup.md](docs/setup.md) for details.

## The course map

| # | Chapter | Highlights |
|---|---------|-----------|
| **Part I — Foundations** ||
| 1 | What is Radio Astronomy? | Jansky & Reber; the jansky unit; the atmospheric window |
| 2 | The Physics of Radio Emission | Rayleigh–Jeans, brightness temperature, spectral index |
| 3 | Signals, Noise & the Radiometer Equation | Dicke 1946; watch a signal climb out of the noise |
| **Part II — Instrumentation** ||
| 4 | Antennas & Receivers | beam patterns, 1.22 λ/D resolution, A_eff, SEFD |
| 5 | Hands-on SDR *(optional)* | RTL-SDR, sampling, IQ data, power spectra |
| 6 | Detecting the Hydrogen Line | the 21 cm line; van de Hulst, Ewen & Purcell |
| **Part III — Interferometry** ||
| 7 | Why Interferometry? | two-element fringes; resolution from baselines |
| 8 | Aperture Synthesis & the uv-plane | van Cittert–Zernike; Earth-rotation synthesis; the dirty beam |
| 9 | Deconvolution & CLEAN | Högbom 1974, implemented by hand |
| **Part IV — Real Data & Research** ||
| 10 | Accessing Open Archives | astroquery / pyvo against NRAO, HEASARC, VizieR, the VO |
| 11 | HI 21 cm & Galactic Rotation | derive a rotation curve → the dark-matter problem |
| 12 | Continuum Imaging with the VLA | calibrate & image a real MS in CASA |
| 13 | Pulsars | Hewish & Bell 1968; dispersion, de-dispersion, folding |
| 14 | Multi-wavelength Diversion | cross-match radio with Gaia/SDSS; build an SED |
| 15 | Capstone | an open-ended mini research project |

Optional hardware chapters (5 & 6) have simulated/archival fallbacks, and every
research chapter degrades gracefully to offline synthetic data — so you can complete
the **entire** course with nothing but a laptop and no network.

## What's in the box

```
jansky/
├── notebooks/        # the course — 15 numbered, executable chapters
├── docs/             # MkDocs site (prose + the same notebooks, rendered) + bibliography
├── src/jansky/       # the helper package the notebooks lean on
│   ├── units.py          # janskys, brightness temperature, decibels
│   ├── signals.py        # noise, the radiometer equation, beams, spectra
│   ├── interferometry.py # uv-coverage, the dirty beam, Högbom CLEAN
│   ├── data.py           # cached dataset downloaders + offline fallbacks
│   └── plotting.py       # shared figure styling
├── containers/       # Dockerfiles + compose (JupyterLab, CASA, GNU Radio)
├── tests/            # pytest for the helpers; nbmake smoke-tests for Part I
└── .claude/agents/   # the subagents used to author & review the course
```

## Common tasks

```bash
make help            # list all targets
make lab             # JupyterLab
make docs-serve      # live docs at http://localhost:8000
make test            # unit tests
make test-notebooks  # execute the Part I notebooks end-to-end
make fetch-data      # list sample datasets (ARGS="--fetch hi4pi-sample" to download)
```

## Going deeper

The [References](docs/references.md) page collects the landmark papers (Jansky 1933,
Ewen & Purcell 1951, Högbom 1974, Hewish & Bell 1968, …) and the standing textbooks —
above all Condon & Ransom's free [*Essential Radio Astronomy*](https://science.nrao.edu/opportunities/courses/era),
the perfect companion to this course.

## License

MIT — see [LICENSE](LICENSE).
