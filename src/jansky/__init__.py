"""jansky -- a hands-on radio astronomy course.

This package collects the small, well-tested helper utilities that the course
notebooks lean on so the teaching code stays readable. The heavy lifting still
uses the real scientific libraries (``numpy``, ``scipy``, ``astropy``,
``astroquery``, ``spectral-cube`` ...); these helpers just remove boilerplate
and encode a few radio-astronomy conventions in one place.

Submodules
----------
units
    Conversions between janskys, brightness temperature, and decibels.
signals
    Noise generation, the radiometer equation, synthetic spectra, beam shapes.
interferometry
    uv-coverage, the dirty beam, a minimal Hogbom CLEAN, van Cittert--Zernike.
data
    Cached downloaders for the sample datasets used in the research chapters.
formats
    Data formats & the ecosystem: GUPPI raw, SigMF, the Radio-Sky Spectrograph
    network protocol, and optional wrappers for the heavier I/O libraries.
transients
    Dispersion, de-dispersion, and single-pulse DM searching for FRBs/pulsars.
plotting
    Shared matplotlib styling so every chapter's figures look consistent.

The package is named after Karl Jansky, who in 1932 discovered radio emission
from the Milky Way and after whom the unit of spectral flux density is named.
"""

from __future__ import annotations

__version__ = "0.1.0"

from jansky import (
    data,
    formats,
    interferometry,
    plotting,
    signals,
    transients,
    units,
)

__all__ = [
    "__version__",
    "data",
    "formats",
    "interferometry",
    "plotting",
    "signals",
    "transients",
    "units",
]
