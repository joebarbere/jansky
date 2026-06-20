"""Published-value (literature-anchored) accuracy tests.

The rest of the suite checks *internal* consistency (round-trips, scaling laws,
monotonicity) -- but a wrong shared constant round-trips happily. These tests pin
the helpers to numbers from the literature, so a perturbed constant or a broken
formula fails loudly. See ``src/jansky/constants.py`` for the single source of
truth they implicitly guard.
"""

from __future__ import annotations

import astropy.units as u
import numpy as np

from jansky import constants, molecular, solar, timing, transients, units


def test_constants_are_single_source_of_truth():
    """The modules re-export the centralised constants, not private copies."""
    assert transients.DM_CONST == constants.DM_CONST
    assert solar.R_SUN_KM == constants.R_SUN_KM
    assert molecular.CO_J10.to_value(u.GHz) == constants.CO_J10_GHZ


def test_ngc4258_central_mass():
    """The NGC 4258 maser disk (r ~ 0.2 pc, v ~ 1000 km/s) weighs the central
    black hole at ~4e7 Msun (Herrnstein et al. 1999; Humphreys et al. 2013)."""
    mass = molecular.maser_central_mass(0.2 * u.pc, 1000 * u.km / u.s)
    m_msun = mass.to_value(u.Msun)
    # Keplerian M = v^2 r / G lands at ~4.6e7; the published BH mass is ~3.9e7.
    assert 3e7 < m_msun < 6e7


def test_hellings_downs_quadrupole_minimum():
    """At 90 deg separation the HD curve sits at its anti-correlated value,
    Gamma(90) = (3/2)x ln x - x/4 + 1/2 with x = 1/2, i.e. ~ -0.145."""
    gamma_90 = timing.hellings_downs(np.pi / 2)
    assert np.isclose(gamma_90, -0.1449, atol=1e-3)
    assert gamma_90 < 0  # genuine anti-correlation near quadrature


def test_brightness_temperature_flux_published_scale():
    """A 1 K brightness temperature over 1 sr at 1.4 GHz is ~6.0e4 Jy by the
    Rayleigh-Jeans relation S = 2 k T nu^2 Omega / c^2 (hand-computed)."""
    flux = units.brightness_temperature_to_flux(1 * u.K, 1.4 * u.GHz, 1 * u.sr)
    assert np.isclose(flux.to_value(u.Jy), 6.02e4, rtol=1e-2)
    # And it inverts back to 1 K.
    t_b = units.flux_to_brightness_temperature(flux, 1.4 * u.GHz, 1 * u.sr)
    assert np.isclose(t_b.to_value(u.K), 1.0, rtol=1e-6)


def test_dispersion_delay_canonical_value():
    """k_DM = 4148.808 gives a 4.15 ms delay at DM = 1 between 1 GHz and infinity
    -- the textbook dispersion constant (Lorimer & Kramer)."""
    delay = transients.dispersion_delay(dm=1.0, f_lo_mhz=1000.0, f_hi_mhz=1e9)
    assert np.isclose(delay, 4.1488e-3, rtol=1e-3)


def test_macquart_redshift_real_burst():
    """A localised FRB with cosmic DM ~ 290 pc cm^-3 (e.g. FRB 180924, z = 0.32)
    yields z ~ 0.32 from the Macquart relation."""
    z = transients.macquart_redshift(290.0)
    assert np.isclose(z, 0.32, atol=0.02)


def test_type_ii_shock_speed_recovered():
    """A 1500 km/s CME-driven shock (a typical fast event) is recovered from its
    forward-modelled type II frequency drift via the Newkirk density model."""
    times, freqs = solar.type_ii_track(1500.0)
    recovered = solar.shock_speed_from_track(times, freqs)
    assert np.isclose(recovered, 1500.0, rtol=1e-3)
