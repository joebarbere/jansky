"""Radio-astronomy unit conversions, built on :mod:`astropy.units`.

Radio astronomers live in a handful of units that newcomers find unusual:

* the **jansky** (Jy), a unit of spectral flux density equal to
  :math:`10^{-26}\\,\\mathrm{W\\,m^{-2}\\,Hz^{-1}}`, named after Karl Jansky;
* **brightness temperature** :math:`T_b`, the temperature a blackbody would need
  in the Rayleigh--Jeans limit to produce the observed brightness; and
* the **decibel**, ubiquitous in the receiver/electronics side of the field.

These helpers wrap the conversions so the notebooks can state intent directly.
They all accept and return :class:`astropy.units.Quantity` objects (or plain
numbers, interpreted in the documented default unit).
"""

from __future__ import annotations

import astropy.constants as const
import astropy.units as u
import numpy as np

__all__ = [
    "JY",
    "to_jansky",
    "brightness_temperature_to_flux",
    "flux_to_brightness_temperature",
    "rayleigh_jeans_brightness",
    "planck_brightness",
    "to_decibels",
    "from_decibels",
]

#: The jansky, exposed for convenience (``astropy`` already defines ``u.Jy``).
JY = u.Jy


def to_jansky(flux: u.Quantity) -> u.Quantity:
    """Convert any spectral flux density quantity to janskys.

    Parameters
    ----------
    flux
        A spectral flux density, e.g. ``1e-26 * u.W / u.m**2 / u.Hz``.

    Returns
    -------
    astropy.units.Quantity
        The same flux expressed in janskys.
    """
    return flux.to(u.Jy)


def rayleigh_jeans_brightness(
    temperature: u.Quantity, frequency: u.Quantity
) -> u.Quantity:
    """Surface brightness of a blackbody in the Rayleigh--Jeans limit.

    :math:`B_\\nu = 2 k_B T \\nu^2 / c^2`. Valid when
    :math:`h\\nu \\ll k_B T`, which holds across essentially the whole radio
    band for astrophysical temperatures -- the assumption that underpins the
    use of brightness temperature in radio astronomy.

    Parameters
    ----------
    temperature
        Physical (or brightness) temperature, e.g. ``100 * u.K``.
    frequency
        Observing frequency, e.g. ``1.4 * u.GHz``.

    Returns
    -------
    astropy.units.Quantity
        Spectral radiance per unit solid angle
        (``W m^-2 Hz^-1 sr^-1``).
    """
    temperature = u.Quantity(temperature, u.K)
    frequency = u.Quantity(frequency, u.Hz)
    # The RJ brightness is per unit solid angle; steradian is dimensionless, so
    # we attach it explicitly to get the conventional surface-brightness units.
    b_nu = 2 * const.k_B * temperature * frequency**2 / const.c**2 / u.sr
    return b_nu.to(u.W / u.m**2 / u.Hz / u.sr)


def planck_brightness(temperature: u.Quantity, frequency: u.Quantity) -> u.Quantity:
    """Full Planck blackbody surface brightness :math:`B_\\nu(T)`.

    :math:`B_\\nu = \\dfrac{2 h \\nu^3}{c^2}\\dfrac{1}{e^{h\\nu/k_B T} - 1}`. Unlike
    :func:`rayleigh_jeans_brightness` it is exact at all frequencies; the two
    agree when :math:`h\\nu \\ll k_B T` (the radio regime). This is the curve the
    cosmic microwave background follows to extraordinary precision (Chapter 22).

    Parameters
    ----------
    temperature
        Blackbody temperature (e.g. ``2.725 * u.K`` for the CMB).
    frequency
        Observing frequency.

    Returns
    -------
    astropy.units.Quantity
        Spectral radiance per solid angle (``W m^-2 Hz^-1 sr^-1``).
    """
    temperature = u.Quantity(temperature, u.K)
    frequency = u.Quantity(frequency, u.Hz)
    x = (const.h * frequency / (const.k_B * temperature)).to_value(u.dimensionless_unscaled)
    b_nu = (2 * const.h * frequency**3 / const.c**2) / (np.expm1(x)) / u.sr
    return b_nu.to(u.W / u.m**2 / u.Hz / u.sr)


def brightness_temperature_to_flux(
    temperature: u.Quantity,
    frequency: u.Quantity,
    solid_angle: u.Quantity,
) -> u.Quantity:
    """Convert a brightness temperature over a solid angle to a flux density.

    Integrates the Rayleigh--Jeans brightness over the source solid angle:
    :math:`S_\\nu = B_\\nu \\,\\Omega`.

    Parameters
    ----------
    temperature
        Brightness temperature (K).
    frequency
        Observing frequency.
    solid_angle
        Source solid angle, e.g. ``(1 * u.arcmin**2).to(u.sr)`` or a value in
        steradians.

    Returns
    -------
    astropy.units.Quantity
        Flux density in janskys.
    """
    solid_angle = u.Quantity(solid_angle, u.sr)
    b_nu = rayleigh_jeans_brightness(temperature, frequency)
    return (b_nu * solid_angle).to(u.Jy)


def flux_to_brightness_temperature(
    flux: u.Quantity,
    frequency: u.Quantity,
    solid_angle: u.Quantity,
) -> u.Quantity:
    """Inverse of :func:`brightness_temperature_to_flux`.

    Inverts the Rayleigh--Jeans relation analytically,
    :math:`T_b = S_\\nu c^2 / (2 k_B \\nu^2 \\Omega)`, so it round-trips exactly
    with the forward conversion. (astropy also ships a ``brightness_temperature``
    equivalency; we keep the explicit form here for transparency in the lessons.)

    Parameters
    ----------
    flux
        Flux density (e.g. janskys).
    frequency
        Observing frequency.
    solid_angle
        Solid angle over which the flux is spread (e.g. the beam area).

    Returns
    -------
    astropy.units.Quantity
        Brightness temperature in kelvin.
    """
    flux = u.Quantity(flux, u.Jy)
    frequency = u.Quantity(frequency, u.Hz)
    solid_angle = u.Quantity(solid_angle, u.sr)
    # The explicit u.sr balances the per-steradian convention carried by the
    # forward Rayleigh--Jeans brightness (see rayleigh_jeans_brightness).
    t_b = flux * const.c**2 * u.sr / (2 * const.k_B * frequency**2 * solid_angle)
    return t_b.to(u.K)


def to_decibels(ratio: float | np.ndarray) -> float | np.ndarray:
    """Convert a (power) ratio to decibels: :math:`10\\log_{10}(\\text{ratio})`."""
    return 10.0 * np.log10(np.asarray(ratio, dtype=float))


def from_decibels(db: float | np.ndarray) -> float | np.ndarray:
    """Convert decibels back to a linear power ratio."""
    return np.power(10.0, np.asarray(db, dtype=float) / 10.0)
