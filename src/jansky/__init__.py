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
vlf
    VLF ionospheric monitoring and sudden-ionospheric-disturbance detection.
signals
    Noise generation, the radiometer equation, synthetic spectra, beam shapes.
seti
    The Doppler-drift technosignature search and the ON/OFF cadence test.
solar
    Coronal density, plasma frequency, and type II burst / CME shock speed.
interferometry
    uv-coverage, the dirty beam, a minimal Hogbom CLEAN, van Cittert--Zernike.
lightning
    Sferics, tweeks, whistlers, whistler de-dispersion, and TOA geolocation.
meteor
    Meteor-scatter echoes (underdense/overdense) and ping detection.
molecular
    The CO rotational ladder and the Keplerian maser-disk black-hole weigh-in.
eor
    Cosmic dawn & reionization: the redshifted 21 cm signal, spin temperature,
    the global-signal trough, and smooth-foreground removal.
data
    Cached downloaders for the sample datasets used in the research chapters.
formats
    Data formats & the ecosystem: GUPPI raw, SigMF, the Radio-Sky Spectrograph
    network protocol, and optional wrappers for the heavier I/O libraries.
transients
    Dispersion, de-dispersion, and single-pulse DM searching for FRBs/pulsars.
timing
    Pulsar timing arrays and the Hellings--Downs nanohertz-GW correlation.
plotting
    Shared matplotlib styling so every chapter's figures look consistent.
polarization
    Stokes parameters, the Faraday lambda^2 law, and RM synthesis.
synchrotron
    The non-thermal continuum: spectral index, SSA turnover, spectral aging, and
    the minimum-energy magnetic field.
rfi
    Robust statistics, spectral kurtosis, and the SumThreshold algorithm for RFI flagging.

The package is named after Karl Jansky, who in 1932 discovered radio emission
from the Milky Way and after whom the unit of spectral flux density is named.
"""

from __future__ import annotations

__version__ = "0.1.0"

from jansky import (
    data,
    eor,
    formats,
    interferometry,
    lightning,
    meteor,
    molecular,
    plotting,
    polarization,
    rfi,
    seti,
    signals,
    solar,
    synchrotron,
    timing,
    transients,
    units,
    vlf,
)

__all__ = [
    "__version__",
    "data",
    "eor",
    "formats",
    "interferometry",
    "lightning",
    "meteor",
    "molecular",
    "plotting",
    "polarization",
    "rfi",
    "seti",
    "signals",
    "solar",
    "synchrotron",
    "timing",
    "transients",
    "units",
    "vlf",
]
