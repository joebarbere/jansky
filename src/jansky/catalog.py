"""A small built-in catalogue of bright radio sources, for mapping the radio sky.

A packaged, offline list of famous radio sources with the fields a beginner's project
needs: name, J2000 coordinates, flux density at three frequencies (0.408, 1.4, 5.0 GHz),
source type, dominant emission mechanism, and approximate distance. It is deliberately
small and hand-curated -- the brightest and most instructive objects -- so the
catalogue/sky-map chapter has real numbers without a network call. A short list of the
brightest optical stars is included so the radio map can be overlaid on the visible sky.

Flux densities are representative literature values (Baars et al. 1977 scale and common
compilations); for steep-spectrum objects a single power law fits the three points well,
while thermal (free-free) and peaked (synchrotron self-absorbed) sources are included
precisely because they do *not* -- that curvature is the point of the spectral-index
exercise. Use :func:`spectral_index` to fit each spectrum.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "BRIGHT_STARS",
    "CATALOG_FREQUENCIES_GHZ",
    "RadioSource",
    "Star",
    "find",
    "load_catalog",
    "of_type",
    "spectral_index",
]

#: The three reference frequencies (GHz) at which every catalogue flux is tabulated.
CATALOG_FREQUENCIES_GHZ = (0.408, 1.4, 5.0)


@dataclass(frozen=True)
class RadioSource:
    """One catalogue entry. Fluxes are in jansky at :data:`CATALOG_FREQUENCIES_GHZ`."""

    name: str
    ra_deg: float
    dec_deg: float
    flux_jy: tuple[float, float, float]
    source_type: str
    emission: str
    distance: str


@dataclass(frozen=True)
class Star:
    """A bright optical star for overlaying the visible sky on the radio map."""

    name: str
    ra_deg: float
    dec_deg: float
    v_mag: float


# name, RA(deg), Dec(deg), (S_0.408, S_1.4, S_5.0) Jy, type, emission, distance
_CATALOG: tuple[RadioSource, ...] = (
    RadioSource(
        "Cassiopeia A",
        350.850,
        58.815,
        (5373.0, 2080.0, 780.0),
        "supernova remnant",
        "synchrotron",
        "3.4 kpc",
    ),
    RadioSource(
        "Cygnus A",
        299.868,
        40.734,
        (5840.0, 1600.0, 420.0),
        "radio galaxy (FR II)",
        "synchrotron",
        "230 Mpc",
    ),
    RadioSource(
        "Taurus A (Crab)",
        83.633,
        22.014,
        (1383.0, 955.0, 652.0),
        "supernova remnant / PWN",
        "synchrotron",
        "2.0 kpc",
    ),
    RadioSource(
        "Virgo A (M87)",
        187.706,
        12.391,
        (576.0, 215.0, 78.0),
        "radio galaxy",
        "synchrotron",
        "16.4 Mpc",
    ),
    RadioSource(
        "Centaurus A",
        201.365,
        -43.019,
        (3152.0, 1330.0, 546.0),
        "radio galaxy",
        "synchrotron",
        "3.8 Mpc",
    ),
    RadioSource(
        "Hydra A (3C 218)",
        139.524,
        -12.096,
        (123.8, 40.8, 13.0),
        "radio galaxy",
        "synchrotron",
        "250 Mpc",
    ),
    RadioSource(
        "3C 295", 212.835, 52.203, (48.3, 22.5, 10.2), "radio galaxy", "synchrotron", "1.4 Gpc"
    ),
    RadioSource(
        "3C 273", 187.278, 2.052, (62.2, 55.0, 48.4), "quasar", "synchrotron (flat core)", "750 Mpc"
    ),
    RadioSource("3C 48", 24.422, 33.160, (42.9, 16.0, 5.8), "quasar", "synchrotron", "1.2 Gpc"),
    RadioSource(
        "3C 84 (Perseus A)",
        49.951,
        41.512,
        (18.0, 23.0, 45.0),
        "radio galaxy (Seyfert)",
        "synchrotron (inverted core)",
        "75 Mpc",
    ),
    RadioSource(
        "Fornax A", 50.674, -37.208, (308.0, 115.0, 41.5), "radio galaxy", "synchrotron", "19 Mpc"
    ),
    RadioSource(
        "Pictor A",
        79.957,
        -45.779,
        (177.0, 66.0, 23.8),
        "radio galaxy (FR II)",
        "synchrotron",
        "150 Mpc",
    ),
    RadioSource(
        "Vela SNR",
        128.750,
        -45.170,
        (1965.0, 1200.0, 721.0),
        "supernova remnant",
        "synchrotron",
        "0.29 kpc",
    ),
    RadioSource(
        "3C 58",
        31.408,
        64.828,
        (37.3, 33.0, 29.1),
        "pulsar wind nebula",
        "synchrotron (plerion)",
        "2.0 kpc",
    ),
    RadioSource(
        "Sagittarius A*",
        266.417,
        -29.008,
        (0.30, 0.70, 1.40),
        "galactic nucleus (SMBH)",
        "synchrotron (self-absorbed)",
        "8.2 kpc",
    ),
    RadioSource(
        "Orion A (M42)",
        83.822,
        -5.391,
        (180.0, 380.0, 400.0),
        "HII region",
        "thermal (free-free)",
        "0.41 kpc",
    ),
    RadioSource(
        "W3", 36.770, 61.870, (40.0, 80.0, 70.0), "HII region", "thermal (free-free)", "2.0 kpc"
    ),
    RadioSource(
        "PKS 1934-638",
        294.854,
        -63.713,
        (6.0, 14.0, 11.0),
        "GPS / compact",
        "synchrotron (self-absorbed)",
        "350 Mpc",
    ),
    RadioSource(
        "M82",
        148.969,
        69.680,
        (13.6, 10.0, 7.3),
        "starburst galaxy",
        "synchrotron + thermal",
        "3.6 Mpc",
    ),
    RadioSource(
        "PSR B1919+21",
        290.430,
        21.880,
        (0.081, 0.010, 0.0012),
        "pulsar",
        "coherent (steep)",
        "0.95 kpc",
    ),
)

#: The brightest optical stars (J2000), for overlaying the visible sky on the radio map.
BRIGHT_STARS: tuple[Star, ...] = (
    Star("Sirius", 101.287, -16.716, -1.46),
    Star("Canopus", 95.988, -52.696, -0.74),
    Star("Rigil Kentaurus", 219.902, -60.834, -0.27),
    Star("Arcturus", 213.915, 19.182, -0.05),
    Star("Vega", 279.234, 38.784, 0.03),
    Star("Capella", 79.172, 45.998, 0.08),
    Star("Rigel", 78.634, -8.202, 0.13),
    Star("Procyon", 114.825, 5.225, 0.34),
    Star("Betelgeuse", 88.793, 7.407, 0.50),
    Star("Achernar", 24.429, -57.237, 0.46),
    Star("Aldebaran", 68.980, 16.509, 0.85),
    Star("Antares", 247.352, -26.432, 1.09),
    Star("Spica", 201.298, -11.161, 0.97),
    Star("Pollux", 116.329, 28.026, 1.14),
    Star("Fomalhaut", 344.413, -29.622, 1.16),
    Star("Deneb", 310.358, 45.280, 1.25),
)


def load_catalog() -> list[RadioSource]:
    """Return the built-in radio-source catalogue as a list."""
    return list(_CATALOG)


def find(name: str) -> RadioSource:
    """Look up a source by (case-insensitive, substring) name. Raises if not unique."""
    key = name.strip().lower()
    hits = [s for s in _CATALOG if key in s.name.lower()]
    if not hits:
        raise KeyError(f"no catalogue source matching {name!r}")
    if len(hits) > 1:
        raise KeyError(f"{name!r} matches several sources: {[s.name for s in hits]}")
    return hits[0]


def of_type(substring: str) -> list[RadioSource]:
    """All catalogue sources whose ``source_type`` contains ``substring`` (case-insensitive)."""
    key = substring.strip().lower()
    return [s for s in _CATALOG if key in s.source_type.lower()]


def spectral_index(source: RadioSource) -> float:
    """Best-fit power-law spectral index :math:`\\alpha` (with :math:`S\\propto\\nu^\\alpha`).

    Fits a straight line to :math:`\\log_{10} S` versus :math:`\\log_{10}\\nu` over the three
    catalogue frequencies and returns the slope. For a clean synchrotron source this is the
    spectral index; for a thermal or peaked source the single slope only summarises a curved
    spectrum (which is exactly what the exercise is meant to reveal).
    """
    nu = np.log10(np.array(CATALOG_FREQUENCIES_GHZ, float))
    s = np.log10(np.array(source.flux_jy, float))
    slope, _intercept = np.polyfit(nu, s, 1)
    return float(slope)
