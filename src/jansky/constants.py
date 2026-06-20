"""Shared physical constants for the :mod:`jansky` helpers.

A single source of truth for the dimensional constants that appear in more than
one module (or in both the code and the prose). Centralising them means the
package and the chapters cannot silently diverge, and a published-value test
(``tests/test_accuracy.py``) can pin them to the literature. Each entry carries a
provenance comment so the number is traceable, not magic.

Only *physical/empirical* constants live here. Fundamental constants
(:math:`k_B`, :math:`c`, :math:`G`, :math:`h`) come from :mod:`astropy.constants`
so they stay CODATA-current.
"""

from __future__ import annotations

__all__ = [
    "DM_CONST",
    "FP_COEFF_MHZ",
    "R_SUN_KM",
    "NEWKIRK_A",
    "NEWKIRK_B",
    "CO_J10_GHZ",
    "MACQUART_SLOPE",
]

#: Dispersion constant :math:`k_\mathrm{DM}` in MHz^2 pc^-1 cm^3 s. The
#: *conventional* value used throughout pulsar/FRB astronomy, fixed by definition
#: rather than re-derived from fundamental constants so DMs are comparable across
#: instruments (Manchester & Taylor 1972; see Kulkarni 2020 for the history).
DM_CONST = 4.148808e3

#: Plasma-frequency coefficient: :math:`f_p[\mathrm{MHz}] = 8.977\times10^{-3}
#: \sqrt{n_e[\mathrm{cm^{-3}}]}`. Equivalent to
#: :math:`f_p = \tfrac{1}{2\pi}\sqrt{n_e e^2/\varepsilon_0 m_e}`.
FP_COEFF_MHZ = 8.977e-3

#: Solar radius in km (IAU 2015 nominal value, rounded).
R_SUN_KM = 6.957e5

#: Newkirk (1961) coronal-density model :math:`n_e = f\cdot A\cdot 10^{B/r}`
#: (``r`` in solar radii, ``f`` the streamer fold factor): the leading coefficient
#: A = 4.2e4 cm^-3 ...
NEWKIRK_A = 4.2e4
#: ... and the exponent scale B = 4.32 (Newkirk 1961).
NEWKIRK_B = 4.32

#: CO J=1->0 rest frequency in GHz; the rotational ladder is ~J times this
#: (CDMS/JPL line catalogues; 115.271202 GHz).
CO_J10_GHZ = 115.271202

#: Macquart-relation slope: mean cosmic dispersion per unit redshift, ~900 pc cm^-3
#: per z (Macquart et al. 2020). NOTE: this is *cosmology- and baryon-fraction-
#: dependent*, not a universal constant -- treat redshifts from it as estimates.
MACQUART_SLOPE = 900.0
