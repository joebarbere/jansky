"""Synchrotron radiation: the non-thermal radio continuum.

Relativistic electrons spiralling in magnetic fields radiate **synchrotron** emission --
the dominant non-thermal mechanism behind supernova remnants, AGN jets and lobes, radio
galaxies, and the diffuse Galactic background (Essential Radio Astronomy, Ch 5). A
power-law electron energy distribution :math:`N(E) \\propto E^{-p}` produces a power-law
spectrum :math:`S_\\nu \\propto \\nu^{\\alpha}` with :math:`\\alpha = -(p-1)/2`, so the
*observed* spectral index reads back the electron index. This module collects the small,
teachable relations: the index mapping, a spectrum with an optional
synchrotron-self-absorption turnover, a radiatively-aged (steepened) spectrum and its
age, the minimum-energy / equipartition magnetic field, and the inverse-Compton
brightness-temperature limit.

Sign convention: spectra are written :math:`S_\\nu \\propto \\nu^{\\alpha}`, so a typical
optically-thin synchrotron source has a **negative** index (e.g. :math:`\\alpha = -0.7`).

References
----------
* Condon, J. J. & Ransom, S. M., *Essential Radio Astronomy*, Ch 5.
* Rybicki, G. B. & Lightman, A. P. (1979), *Radiative Processes in Astrophysics*.
* Pacholczyk, A. G. (1970), *Radio Astrophysics* -- the minimum-energy field.
* Miley, G. (1980), ARA&A 18, 165 -- the radiative (spectral) age.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "T_B_LIMIT_K",
    "spectral_index",
    "electron_index",
    "synchrotron_spectrum",
    "aged_spectrum",
    "b_cmb",
    "spectral_age",
    "equipartition_field",
    "brightness_temperature_limit",
]

#: Inverse-Compton brightness-temperature ceiling for incoherent synchrotron sources, in
#: K (Kellermann & Pauliny-Toth 1969): above ~10^12 K the relativistic electrons cool
#: catastrophically by inverse-Compton scattering their own synchrotron photons.
T_B_LIMIT_K: float = 1.0e12


def spectral_index(electron_p: np.ndarray | float) -> np.ndarray:
    """Synchrotron spectral index :math:`\\alpha = -(p-1)/2` for electron index ``p``.

    A power-law electron distribution :math:`N(E)\\propto E^{-p}` radiates
    :math:`S_\\nu\\propto\\nu^{\\alpha}`. Example: ``p = 2.5`` gives ``alpha = -0.75``.
    """
    p = np.asarray(electron_p, dtype=float)
    return -(p - 1.0) / 2.0


def electron_index(alpha: np.ndarray | float) -> np.ndarray:
    """Electron power-law index :math:`p = 1 - 2\\alpha` from the spectral index ``alpha``.

    The inverse of :func:`spectral_index`: a measured ``alpha = -0.7`` implies ``p = 2.4``.
    """
    return 1.0 - 2.0 * np.asarray(alpha, dtype=float)


def synchrotron_spectrum(
    nu: np.ndarray,
    s_ref: float,
    alpha: float,
    nu_ref: float = 1.0,
    nu_ssa: float | None = None,
) -> np.ndarray:
    """A synchrotron spectrum, optionally with synchrotron self-absorption (SSA).

    Without ``nu_ssa`` this is the optically-thin power law
    :math:`S_\\nu = S_\\mathrm{ref}\\,(\\nu/\\nu_\\mathrm{ref})^{\\alpha}`.

    With ``nu_ssa`` the source is optically thick at low frequency: below the turnover
    the flux rises as the universal :math:`\\nu^{5/2}` law (independent of ``alpha``) and
    above it relaxes to :math:`\\nu^{\\alpha}`. The form used is
    :math:`S_\\nu \\propto \\nu^{5/2}\\,(1-e^{-\\tau_\\nu})` with
    :math:`\\tau_\\nu = (\\nu/\\nu_\\mathrm{ssa})^{\\alpha-5/2}`, normalised so the
    optically-thin branch matches the bare power law.

    Parameters
    ----------
    nu
        Frequency axis (same unit as ``nu_ref`` and ``nu_ssa``).
    s_ref
        Flux density at ``nu_ref`` on the optically-thin branch.
    alpha
        Optically-thin spectral index (negative for typical synchrotron).
    nu_ref
        Reference frequency for ``s_ref``.
    nu_ssa
        SSA turnover frequency (where :math:`\\tau = 1`); ``None`` for no absorption.

    Returns
    -------
    numpy.ndarray
        Flux density on the ``nu`` grid.
    """
    nu = np.asarray(nu, dtype=float)
    thin = s_ref * (nu / nu_ref) ** alpha
    if nu_ssa is None:
        return thin
    tau = (nu / nu_ssa) ** (alpha - 2.5)
    # Normalise the nu^{5/2}(1-e^-tau) form so its thin limit equals the bare power law.
    norm = s_ref * nu_ref ** (-alpha) * nu_ssa ** (alpha - 2.5)
    return norm * nu**2.5 * (1.0 - np.exp(-tau))


def aged_spectrum(
    nu: np.ndarray,
    s_ref: float,
    alpha: float,
    nu_ref: float,
    nu_break: float,
    delta: float = 0.5,
) -> np.ndarray:
    """A radiatively-aged synchrotron spectrum: a power law that steepens above a break.

    Radiative (synchrotron + inverse-Compton) losses deplete the highest-energy electrons
    first, so the spectrum steepens above a **break frequency**. In the continuous-injection
    picture the index steepens by ``delta = 0.5`` (from :math:`\\alpha` to
    :math:`\\alpha-0.5`) above ``nu_break``; a single-burst (JP/KP) model steepens more
    sharply -- pass a larger ``delta`` to mimic it.

    Returns the flux density on the ``nu`` grid, continuous at ``nu_break``.
    """
    nu = np.asarray(nu, dtype=float)
    base = s_ref * (nu / nu_ref) ** alpha
    steepening = np.where(nu > nu_break, (nu / nu_break) ** (-delta), 1.0)
    return base * steepening


def b_cmb(z: float = 0.0) -> float:
    """Inverse-Compton-equivalent magnetic field of the CMB, in µG.

    :math:`B_\\mathrm{CMB} = 3.25\\,(1+z)^2\\ \\mu\\mathrm{G}` -- the field whose energy
    density equals that of the CMB at redshift ``z``. It sets the floor on radiative
    losses (and on :func:`spectral_age`), since electrons always inverse-Compton scatter
    CMB photons even where the magnetic field is weak.
    """
    return 3.25 * (1.0 + z) ** 2


def spectral_age(nu_break_ghz: float, b_field_ug: float, z: float = 0.0) -> float:
    """Radiative (synchrotron) age from the spectral break, in Myr (Miley 1980).

    .. math::

        t = 1590\\,\\frac{B^{1/2}}{B^2 + B_\\mathrm{CMB}^2}\\,
            \\big[(1+z)\\,\\nu_\\mathrm{break}\\big]^{-1/2}\\ \\mathrm{Myr},

    with ``B`` and :math:`B_\\mathrm{CMB}` (:func:`b_cmb`) in µG and
    ``nu_break_ghz`` in GHz. The break frequency drops as the source ages, so a lower
    observed break implies an older source. The loss rate is minimised (oldest inferred
    age) when :math:`B = B_\\mathrm{CMB}/\\sqrt{3}`.

    Parameters
    ----------
    nu_break_ghz
        Observed spectral break frequency, in GHz.
    b_field_ug
        Magnetic field strength, in µG.
    z
        Source redshift.

    Returns
    -------
    float
        Radiative age in Myr.
    """
    bic = b_cmb(z)
    return (
        1590.0 * np.sqrt(b_field_ug) / (b_field_ug**2 + bic**2) * ((1.0 + z) * nu_break_ghz) ** -0.5
    )


def equipartition_field(
    luminosity_erg_s: float,
    volume_cm3: float,
    k: float = 1.0,
    c12: float = 1.6e7,
) -> float:
    """Minimum-energy (≈ equipartition) magnetic field, in Gauss (Pacholczyk 1970).

    The total energy in relativistic particles plus magnetic field,
    :math:`E = (1+k)\\,E_\\mathrm{e} + B^2 V/8\\pi`, is minimised when
    :math:`E_\\mathrm{particles} \\approx \\tfrac{2}{3}\\,E_\\mathrm{field}` -- the two are
    equal to within a factor of order unity; the minimising field is

    .. math:: B_\\mathrm{min} = \\left[\\frac{24\\pi}{7}\\,(1+k)\\,c_{12}\\,
        \\frac{L}{V}\\right]^{2/7},

    in cgs (Gauss). ``k`` is the proton-to-electron energy ratio (1 for a pure-electron
    plasma) and ``c12`` is Pacholczyk's slowly-varying constant for the spectrum and
    frequency band (~1.6×10⁷ cgs for a typical :math:`\\alpha=-0.75`, 10 MHz–100 GHz).
    For a powerful radio galaxy (:math:`L\\sim10^{45}` erg s⁻¹, ~50 kpc) this returns a
    few × 10 µG.

    Parameters
    ----------
    luminosity_erg_s
        Radio (synchrotron) luminosity over the band, in erg s⁻¹.
    volume_cm3
        Emitting volume, in cm³.
    k
        Proton-to-electron energy ratio.
    c12
        Pacholczyk constant (cgs) for the assumed band and spectral index.

    Returns
    -------
    float
        Minimum-energy magnetic field, in Gauss.
    """
    return ((24.0 * np.pi / 7.0) * (1.0 + k) * c12 * luminosity_erg_s / volume_cm3) ** (2.0 / 7.0)


def brightness_temperature_limit() -> float:
    """The inverse-Compton brightness-temperature ceiling, ~10¹² K (:data:`T_B_LIMIT_K`).

    An incoherent synchrotron source brighter than ~10¹² K would have its electrons
    cool catastrophically by inverse-Compton scattering off their own synchrotron
    photons (Kellermann & Pauliny-Toth 1969) -- so apparent temperatures far above this
    signal relativistic beaming (Doppler boosting) rather than a hotter source.
    """
    return T_B_LIMIT_K
