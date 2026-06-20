"""Molecular-line and maser radio astronomy.

Cold molecular gas radiates in rotational lines at millimetre wavelengths -- above
all **CO**, the workhorse tracer of the molecular interstellar medium. Some
sources host **masers** (microwave lasers): compact, fiercely bright spots that
act as point probes of their surroundings. The most famous result came from the
water masers in NGC 4258, which sit in a thin **Keplerian disk** around the
galaxy's central black hole: their line-of-sight velocities versus radius trace
:math:`v=\\sqrt{GM/r}`, weighing the black hole directly. This module provides the
CO rotational ladder and the Keplerian/maser-disk relations.
"""

from __future__ import annotations

import astropy.constants as const
import astropy.units as u
import numpy as np

__all__ = [
    "CO_J10",
    "co_line_frequency",
    "rigid_rotor_frequency",
    "keplerian_velocity",
    "maser_central_mass",
]

#: CO J=1->0 rest frequency.
CO_J10 = 115.271202 * u.GHz


def co_line_frequency(j_upper: int) -> u.Quantity:
    """Approximate rest frequency of the CO ``J_upper -> J_upper-1`` line.

    Uses the rigid-rotor ladder :math:`\\nu \\approx J_\\mathrm{upper}\\,\\nu_{1\\to0}`
    (ignoring small centrifugal-distortion corrections): J=1->0 is 115.27 GHz,
    2->1 is 230.5 GHz, 3->2 is 345.8 GHz, and so on.
    """
    if j_upper < 1:
        raise ValueError("j_upper must be >= 1")
    return j_upper * CO_J10


def rigid_rotor_frequency(j_upper: int, b0: u.Quantity) -> u.Quantity:
    """Rigid-rotor line frequency for ``J_upper -> J_upper-1``: :math:`2 B_0 J_\\mathrm{upper}`."""
    return (2 * u.Quantity(b0, u.GHz) * j_upper).to(u.GHz)


def keplerian_velocity(mass: u.Quantity, radius: u.Quantity) -> u.Quantity:
    """Circular orbital speed :math:`v=\\sqrt{GM/r}` at ``radius`` around ``mass``."""
    mass = u.Quantity(mass, u.Msun)
    radius = u.Quantity(radius, u.pc)
    return np.sqrt(const.G * mass / radius).to(u.km / u.s)


def maser_central_mass(radius: u.Quantity, velocity: u.Quantity) -> u.Quantity:
    """Enclosed (central) mass from a maser's orbital radius and speed.

    Inverts the Keplerian relation, :math:`M = v^2 r / G` -- the measurement that
    weighed the NGC 4258 black hole. Accepts scalars or arrays (returns the mean
    if several masers are given).

    Parameters
    ----------
    radius
        Orbital radius/radii (e.g. ``0.2 * u.pc``).
    velocity
        Orbital speed(s) at that radius (e.g. ``1000 * u.km/u.s``).

    Returns
    -------
    astropy.units.Quantity
        Enclosed mass in solar masses.
    """
    radius = u.Quantity(radius, u.pc)
    velocity = u.Quantity(velocity, u.km / u.s)
    mass = (velocity**2 * radius / const.G).to(u.Msun)
    return np.mean(mass) if mass.isscalar is False and mass.size > 1 else mass
