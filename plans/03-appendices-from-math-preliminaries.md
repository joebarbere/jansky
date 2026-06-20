# Plan 03 — Maths Lab appendices ✅ Delivered

Worked, executable deep-dives promoting the [math preliminaries](../docs/math-preliminaries.md)
into a new **"Appendices — Maths Lab"** nav group. **All six shipped** (PR #21), runnable offline.

| Lab | Notebook | Reuses / adds |
|---|---|---|
| A | [31 · Fourier & Convolution](../notebooks/31_mathslab_fourier_convolution.ipynb) | FFT conventions, the convolution theorem, windowing & leakage |
| B | [32 · Detection Theory & Matched Filtering](../notebooks/32_mathslab_matched_filtering.ipynb) | `jansky.transients`, `jansky.seti`; ROC curves, the 5σ/trials factor |
| C | [33 · Noise Statistics & RFI Excision](../notebooks/33_mathslab_noise_rfi.ipynb) | **`jansky.rfi`** (MAD, spectral kurtosis, flagging) |
| D | [34 · Coordinates, Time & the Sky](../notebooks/34_mathslab_coordinates_time.ipynb) | `astropy.coordinates` (offline), sidereal time, hour angle, LSR |
| E | [35 · Linear Algebra for Calibration](../notebooks/35_mathslab_calibration.ipynb) | **`interferometry.solve_point_source_gains`**, closure quantities, SVD |
| F | [36 · Special Functions & Beams](../notebooks/36_mathslab_special_functions.ipynb) | `jansky.signals` (sinc, Gaussian, Airy/J1, power law, windows) |

New helpers `jansky.rfi` and `interferometry.solve_point_source_gains` are unit-tested; each Lab
has an `nbmake` smoke test. Nothing outstanding.
