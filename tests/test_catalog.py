"""Tests for jansky.catalog -- the built-in radio-source catalogue."""

from __future__ import annotations

import numpy as np

from jansky import catalog


def test_catalog_loads_and_is_well_formed():
    sources = catalog.load_catalog()
    assert len(sources) >= 20
    for s in sources:
        assert len(s.flux_jy) == 3
        assert all(f > 0 for f in s.flux_jy)
        assert -90.0 <= s.dec_deg <= 90.0
        assert 0.0 <= s.ra_deg < 360.0
        assert s.source_type and s.emission


def test_find_by_substring():
    crab = catalog.find("Crab")
    assert "Taurus A" in crab.name
    cyg = catalog.find("Cygnus")
    assert cyg.source_type.startswith("radio galaxy")


def test_spectral_index_synchrotron_is_steep_negative():
    """Cassiopeia A is a clean synchrotron source with alpha ~ -0.77."""
    alpha = catalog.spectral_index(catalog.find("Cassiopeia"))
    assert -0.85 < alpha < -0.65


def test_spectral_index_thermal_is_flat_or_rising():
    """An HII region (free-free) should not look steep-negative like synchrotron."""
    alpha = catalog.spectral_index(catalog.find("Orion"))
    assert alpha > -0.2  # thermal: flat to rising, the diagnostic contrast


def test_of_type_groups_sources():
    snrs = catalog.of_type("supernova remnant")
    names = {s.name for s in snrs}
    assert "Cassiopeia A" in names
    assert len(snrs) >= 2


def test_bright_stars_for_overlay():
    assert len(catalog.BRIGHT_STARS) >= 10
    sirius = next(s for s in catalog.BRIGHT_STARS if s.name == "Sirius")
    assert abs(sirius.v_mag - (-1.46)) < 1e-9
    assert all(-90 <= s.dec_deg <= 90 for s in catalog.BRIGHT_STARS)


def test_frequencies_constant():
    assert catalog.CATALOG_FREQUENCIES_GHZ == (0.408, 1.4, 5.0)
    # spectral_index uses exactly these three points
    cas = catalog.find("Cassiopeia")
    nu = np.log10(catalog.CATALOG_FREQUENCIES_GHZ)
    assert len(nu) == len(cas.flux_jy)
