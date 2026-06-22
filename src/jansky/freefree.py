"""Free-free radiation: the thermal continuum from ionized gas.

Free electrons scattering off ions in a warm ionized plasma -- HII regions, planetary
nebulae, the diffuse thermal Galactic background -- radiate **free-free** (thermal
bremsstrahlung) emission (Essential Radio Astronomy, Ch 4). Unlike synchrotron
(:mod:`jansky.synchrotron`), free-free emission is **unpolarised** and its spectrum is
**flat**: an HII region is optically thick at low frequency, where its brightness
temperature saturates at the electron temperature :math:`T_e` and the flux rises as
:math:`S_\\nu \\propto \\nu^2`; above a turnover frequency it becomes optically thin and
the spectrum flattens to :math:`S_\\nu \\propto \\nu^{-0.1}` (spectral index
:math:`\\alpha \\approx -0.1`). This flat-vs-steep contrast is *the* diagnostic that
separates thermal from non-thermal sources.

The whole shape is governed by the **emission measure**
:math:`\\mathrm{EM} = \\int n_e^2\\,\\mathrm{d}l`, the line-of-sight integral of the
squared electron density. This module collects the teachable relations: the radio
free-free optical depth (Altenhoff approximation), the brightness-temperature and flux
spectra across the thick-to-thin turnover, the turnover frequency, and the Stromgren
radius that sets the size of an ionization-bounded HII region.

References
----------
* Condon, J. J. & Ransom, S. M., *Essential Radio Astronomy*, Ch 4.
* Altenhoff, W. et al. (1960) -- the radio free-free optical-depth approximation.
* Mezger, P. G. & Henderson, A. P. (1967), ApJ 147, 471 -- HII-region radio continua.
* Stromgren, B. (1939), ApJ 89, 526 -- the ionized-sphere radius.
* Rohlfs, K. & Wilson, T. L., *Tools of Radio Astronomy*.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "TAU_COEFF",
    "ALPHA_THIN",
    "ALPHA_RECOMB_CASE_B",
    "freefree_optical_depth",
    "freefree_brightness_temperature",
    "freefree_spectrum",
    "emission_measure",
    "turnover_frequency",
    "stromgren_radius",
]

#: Coefficient in the radio free-free optical depth (Altenhoff approximation), for
#: :math:`T_e` in units of :math:`10^4` K, :math:`\\nu` in GHz, and EM in pc cm⁻⁶:
#: :math:`\\tau = 3.28\\times10^{-7}\\,(T_e/10^4)^{-1.35}\\,\\nu^{-2.1}\\,\\mathrm{EM}`.
TAU_COEFF: float = 3.28e-7

#: Optically-thin free-free spectral index, :math:`S_\\nu \\propto \\nu^{\\alpha}` with
#: :math:`\\alpha = 2 - 2.1 = -0.1` -- the canonical "flat" thermal slope.
ALPHA_THIN: float = -0.1

#: Case-B hydrogen recombination coefficient at :math:`T_e = 10^4` K, in cm³ s⁻¹
#: (Osterbrock & Ferland 2006) -- recombinations to all levels above the ground state.
ALPHA_RECOMB_CASE_B: float = 2.6e-13

#: Parsec in centimetres (for the Stromgren radius).
_PC_CM: float = 3.0856775814913673e18


def freefree_optical_depth(
    nu_ghz: np.ndarray | float,
    em: float,
    t_e: float = 1.0e4,
) -> np.ndarray:
    """Free-free optical depth :math:`\\tau_\\mathrm{ff}(\\nu)` (Altenhoff approximation).

    .. math::

        \\tau_\\mathrm{ff} \\approx 3.28\\times10^{-7}\\,
            \\left(\\frac{T_e}{10^4\\,\\mathrm{K}}\\right)^{-1.35}
            \\left(\\frac{\\nu}{\\mathrm{GHz}}\\right)^{-2.1}
            \\left(\\frac{\\mathrm{EM}}{\\mathrm{pc\\,cm^{-6}}}\\right),

    valid in the radio regime (:math:`h\\nu \\ll k T_e`). The steep
    :math:`\\nu^{-2.1}` dependence is why ionized gas is opaque at low frequency and
    transparent at high frequency.

    Parameters
    ----------
    nu_ghz
        Frequency, in GHz.
    em
        Emission measure :math:`\\int n_e^2\\,\\mathrm{d}l`, in pc cm⁻⁶.
    t_e
        Electron temperature, in K.

    Returns
    -------
    numpy.ndarray
        Optical depth (dimensionless).
    """
    nu = np.asarray(nu_ghz, dtype=float)
    return TAU_COEFF * (t_e / 1.0e4) ** -1.35 * nu**-2.1 * em


def freefree_brightness_temperature(
    nu_ghz: np.ndarray | float,
    em: float,
    t_e: float = 1.0e4,
) -> np.ndarray:
    """Brightness temperature of a free-free source, :math:`T_B = T_e(1 - e^{-\\tau})`.

    Below the turnover the source is optically thick and :math:`T_B \\to T_e`; above it
    the source is optically thin and :math:`T_B \\approx T_e\\,\\tau \\propto \\nu^{-2.1}`.

    Parameters
    ----------
    nu_ghz
        Frequency, in GHz.
    em
        Emission measure, in pc cm⁻⁶.
    t_e
        Electron temperature, in K.

    Returns
    -------
    numpy.ndarray
        Brightness temperature, in K.
    """
    tau = freefree_optical_depth(nu_ghz, em, t_e)
    return t_e * (1.0 - np.exp(-tau))


def freefree_spectrum(
    nu_ghz: np.ndarray | float,
    em: float,
    t_e: float = 1.0e4,
    solid_angle_sr: float = 1.0e-7,
) -> np.ndarray:
    """Flux-density spectrum of a free-free source across the thick-to-thin turnover.

    The flux density follows from the Rayleigh-Jeans law over a fixed solid angle
    :math:`\\Omega`, :math:`S_\\nu = 2 k T_B \\nu^2 \\Omega / c^2`, with
    :math:`T_B` from :func:`freefree_brightness_temperature`. The result is the
    characteristic thermal shape:

    * **optically thick** (low :math:`\\nu`): :math:`T_B \\to T_e` so
      :math:`S_\\nu \\propto \\nu^2`;
    * **optically thin** (high :math:`\\nu`): :math:`T_B \\propto \\nu^{-2.1}` so
      :math:`S_\\nu \\propto \\nu^{-0.1}` -- the flat thermal index
      (:data:`ALPHA_THIN`).

    Parameters
    ----------
    nu_ghz
        Frequency, in GHz.
    em
        Emission measure, in pc cm⁻⁶.
    t_e
        Electron temperature, in K.
    solid_angle_sr
        Source solid angle :math:`\\Omega`, in steradian (sets the overall flux scale;
        :math:`10^{-7}` sr is roughly a 1 arcmin source).

    Returns
    -------
    numpy.ndarray
        Flux density, in jansky (1 Jy = 10⁻²⁶ W m⁻² Hz⁻¹).
    """
    k_b = 1.380649e-23  # J/K
    c = 2.99792458e8  # m/s
    nu_hz = np.asarray(nu_ghz, dtype=float) * 1.0e9
    t_b = freefree_brightness_temperature(nu_ghz, em, t_e)
    s_si = 2.0 * k_b * t_b * nu_hz**2 / c**2 * solid_angle_sr  # W m^-2 Hz^-1
    return s_si / 1.0e-26  # -> jansky


def emission_measure(n_e: float, path_length_pc: float) -> float:
    """Emission measure :math:`\\mathrm{EM} = n_e^2\\,L` for a uniform slab, in pc cm⁻⁶.

    A convenience for the uniform-density case of
    :math:`\\mathrm{EM} = \\int n_e^2\\,\\mathrm{d}l`.

    Parameters
    ----------
    n_e
        Electron density, in cm⁻³.
    path_length_pc
        Path length through the ionized gas, in pc.

    Returns
    -------
    float
        Emission measure, in pc cm⁻⁶.
    """
    return n_e**2 * path_length_pc


def turnover_frequency(em: float, t_e: float = 1.0e4) -> float:
    """Free-free turnover frequency where :math:`\\tau_\\mathrm{ff} = 1`, in GHz.

    Solving :func:`freefree_optical_depth` ``= 1`` for :math:`\\nu`:

    .. math::

        \\nu_\\mathrm{turn} = \\left[3.28\\times10^{-7}\\,
            \\left(\\frac{T_e}{10^4}\\right)^{-1.35}\\mathrm{EM}\\right]^{1/2.1}
            \\ \\mathrm{GHz}.

    Below this frequency the source is optically thick (:math:`S \\propto \\nu^2`); above
    it the source is optically thin and the spectrum flattens.

    Parameters
    ----------
    em
        Emission measure, in pc cm⁻⁶.
    t_e
        Electron temperature, in K.

    Returns
    -------
    float
        Turnover frequency, in GHz.
    """
    return (TAU_COEFF * (t_e / 1.0e4) ** -1.35 * em) ** (1.0 / 2.1)


def stromgren_radius(
    q_ionizing: float,
    n_e: float,
    alpha_b: float = ALPHA_RECOMB_CASE_B,
) -> float:
    """Stromgren radius of an ionization-bounded HII region, in pc (Stromgren 1939).

    In ionization balance the ionizing-photon rate :math:`Q` from the central star(s)
    equals the total recombination rate in the surrounding sphere,
    :math:`Q = \\tfrac{4}{3}\\pi R_s^3\\, n_e^2\\, \\alpha_B`, giving

    .. math::

        R_s = \\left(\\frac{3 Q}{4\\pi n_e^2 \\alpha_B}\\right)^{1/3}.

    For an O5 star (:math:`Q \\sim 10^{49}` s⁻¹) in gas of :math:`n_e \\sim 10^3`
    cm⁻³ this is a few tenths of a parsec.

    Parameters
    ----------
    q_ionizing
        Stellar ionizing-photon luminosity :math:`Q`, in photons s⁻¹.
    n_e
        Electron (≈ proton) density, in cm⁻³.
    alpha_b
        Case-B recombination coefficient, in cm³ s⁻¹ (:data:`ALPHA_RECOMB_CASE_B`).

    Returns
    -------
    float
        Stromgren radius, in pc.
    """
    r_cm = (3.0 * q_ionizing / (4.0 * np.pi * n_e**2 * alpha_b)) ** (1.0 / 3.0)
    return r_cm / _PC_CM
