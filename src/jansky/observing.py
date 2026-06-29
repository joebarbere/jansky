"""Planning a radio observation: sidereal time, transit, beam transit, drift scans.

These helpers turn the geometry of a spinning Earth into the practical numbers an
observer needs before pointing a dish: *what is the local sidereal time*, *when does
my source cross the meridian and how high will it be*, *how long does it spend in the
beam*, and *what trace would a chart recorder draw as it drifts through*. Everything is
plain NumPy implementing the textbook formulae directly, so the mechanics stay
inspectable; the notebooks cross-check these against :mod:`astropy` for confidence.

Key results encoded here
------------------------
* **Greenwich/Local mean sidereal time** from the Julian Date (Meeus 1998,
  *Astronomical Algorithms*, eq. 12.4) -- the clock that runs ~3m56s a day fast on the
  Sun, the very drift Jansky used to fix his signal to the sky.
* **Transit geometry**: a source culminates at hour angle :math:`H = 0` with altitude
  :math:`a_\\mathrm{transit} = 90^\\circ - |\\phi - \\delta|` (Condon & Ransom 2016).
* **Beam transit time**: a source at declination :math:`\\delta` drifts through a beam of
  width :math:`\\theta` in :math:`t = \\theta / (\\omega_\\oplus \\cos\\delta)` -- the
  classic "one degree is four minutes at the equator", stretched by :math:`1/\\cos\\delta`.
* A **drift-scan simulation** of a simple total-power radiometer, composing the beam
  shapes and the radiometer equation in :mod:`jansky.signals`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "DriftScan",
    "SIDEREAL_RATE_DEG_PER_S",
    "altitude",
    "altitude_at_transit",
    "beam_transit_duration",
    "greenwich_sidereal_time",
    "hour_angle",
    "hours_to_transit",
    "is_circumpolar",
    "local_sidereal_time",
    "noise_figure_to_temperature",
    "simulate_drift_scan",
]

#: Earth's sidereal rotation rate in degrees of hour angle per second of time:
#: :math:`360^\circ / 86164.0905\,\mathrm{s}`. A source's *on-sky* drift speed at
#: declination :math:`\delta` is this times :math:`\cos\delta`.
SIDEREAL_RATE_DEG_PER_S = 360.0 / 86164.0905

#: Ratio of the mean solar day to the mean sidereal day (sidereal time runs fast).
SOLAR_TO_SIDEREAL = 1.0027379093


def greenwich_sidereal_time(jd: float | np.ndarray) -> float | np.ndarray:
    """Greenwich mean sidereal time (hours, 0--24) for a Julian Date ``jd`` (UT).

    Implements Meeus (1998) eq. 12.4 directly:
    :math:`\\theta_0 = 280.46061837 + 360.98564736629\\,(JD - 2451545) +
    3.87933\\times10^{-4} T^2 - T^3/38710000`, with :math:`T` in Julian centuries
    from J2000.0. Returned in hours wrapped to :math:`[0, 24)`.
    """
    d = np.asarray(jd, float) - 2451545.0
    t = d / 36525.0
    theta_deg = 280.46061837 + 360.98564736629 * d + 0.000387933 * t**2 - t**3 / 38710000.0
    return (theta_deg % 360.0) / 15.0


def local_sidereal_time(jd: float | np.ndarray, longitude_deg: float) -> float | np.ndarray:
    """Local mean sidereal time (hours, 0--24) at east longitude ``longitude_deg``.

    LST is GMST plus the observer's longitude (east positive). This is the right
    ascension currently on the meridian, so a source transits when LST equals its RA.
    """
    gst = greenwich_sidereal_time(jd)
    return (gst + longitude_deg / 15.0) % 24.0


def hour_angle(lst_hours: float | np.ndarray, ra_hours: float) -> float | np.ndarray:
    """Hour angle (hours, wrapped to :math:`[-12, 12)`) of a source of right ascension ``ra_hours``.

    :math:`H = \\mathrm{LST} - \\alpha`: negative east of the meridian (rising),
    zero at transit, positive west (setting).
    """
    h = (np.asarray(lst_hours, float) - ra_hours + 12.0) % 24.0 - 12.0
    return h


def altitude(
    dec_deg: float, lat_deg: float, hour_angle_hours: float | np.ndarray
) -> float | np.ndarray:
    """Altitude above the horizon (degrees) of a source at hour angle ``hour_angle_hours``.

    :math:`\\sin a = \\sin\\phi\\sin\\delta + \\cos\\phi\\cos\\delta\\cos H` for observer
    latitude :math:`\\phi`, declination :math:`\\delta`, hour angle :math:`H`.
    """
    phi = np.radians(lat_deg)
    dec = np.radians(dec_deg)
    h = np.radians(np.asarray(hour_angle_hours, float) * 15.0)
    sin_a = np.sin(phi) * np.sin(dec) + np.cos(phi) * np.cos(dec) * np.cos(h)
    return np.degrees(np.arcsin(np.clip(sin_a, -1.0, 1.0)))


def altitude_at_transit(dec_deg: float, lat_deg: float) -> float:
    """Altitude (degrees) of a source as it crosses the meridian (``H = 0``).

    At transit the source culminates at :math:`a = 90^\\circ - |\\phi - \\delta|`
    (taking the upper culmination toward the equator). A negative value means the
    source never rises above the horizon from this latitude.
    """
    return 90.0 - abs(lat_deg - dec_deg)


def is_circumpolar(dec_deg: float, lat_deg: float) -> bool:
    """Whether a source never sets (stays above the horizon) from latitude ``lat_deg``.

    A source is circumpolar when its lower culmination is still above the horizon,
    i.e. :math:`|\\delta| \\ge 90^\\circ - |\\phi|` with the same sign hemisphere.
    """
    if lat_deg >= 0:
        return dec_deg >= 90.0 - lat_deg
    return dec_deg <= -90.0 - lat_deg


def hours_to_transit(lst_hours: float, ra_hours: float) -> float:
    """Solar hours until a source of right ascension ``ra_hours`` next transits.

    The source transits when LST reaches its RA. The required advance in sidereal
    time, :math:`(\\alpha - \\mathrm{LST}) \\bmod 24`, is divided by
    :data:`SOLAR_TO_SIDEREAL` to convert to elapsed *solar* (wall-clock) hours.
    """
    delta_sidereal = (ra_hours - lst_hours) % 24.0
    return delta_sidereal / SOLAR_TO_SIDEREAL


def beam_transit_duration(fwhm_deg: float, dec_deg: float) -> float:
    """Time (seconds) a source at declination ``dec_deg`` takes to drift through the beam.

    As the Earth turns, a source at declination :math:`\\delta` sweeps across the sky
    along its parallel at :math:`\\omega_\\oplus \\cos\\delta` (:data:`SIDEREAL_RATE_DEG_PER_S`
    times :math:`\\cos\\delta`). Crossing a beam of angular width ``fwhm_deg`` near the
    meridian therefore takes :math:`t = \\theta / (\\omega_\\oplus \\cos\\delta)`. At the
    equator a :math:`1^\\circ` beam gives ~4 minutes; the :math:`1/\\cos\\delta` factor
    lengthens this toward the pole. Raises for :math:`|\\delta| \\ge 90^\\circ`.
    """
    if abs(dec_deg) >= 90.0:
        raise ValueError("beam transit time diverges at the celestial pole (|dec| >= 90)")
    cos_dec = np.cos(np.radians(dec_deg))
    return fwhm_deg / (SIDEREAL_RATE_DEG_PER_S * cos_dec)


def noise_figure_to_temperature(noise_figure_db: float, t_0: float = 290.0) -> float:
    """Receiver noise temperature (K) from a noise figure in dB.

    :math:`T_\\mathrm{rx} = T_0 (10^{NF/10} - 1)` with the IEEE reference
    :math:`T_0 = 290\\,\\mathrm{K}`.
    """
    return t_0 * (10.0 ** (noise_figure_db / 10.0) - 1.0)


@dataclass
class DriftScan:
    """Outcome of a simulated drift scan (see :func:`simulate_drift_scan`)."""

    #: Time since the start of the scan at each sample (s).
    time_s: np.ndarray
    #: Chart-recorder deflection at each sample (mV).
    deflection_mv: np.ndarray
    #: Position along the chart paper at each sample (mm).
    chart_mm: np.ndarray
    #: Peak source deflection above the baseline (mV).
    peak_mv: float
    #: Peak antenna temperature contributed by the source (K).
    peak_t_a: float
    #: System temperature used (K).
    t_sys: float
    #: 1-sigma radiometer noise on the trace (mV).
    noise_mv: float
    #: Signal-to-noise ratio of the peak.
    snr: float
    #: Time the source spends crossing the beam, FWHM (s).
    transit_s: float


def simulate_drift_scan(
    *,
    flux_jy: float,
    dec_deg: float,
    fwhm_deg: float,
    diameter_m: float,
    source_size_deg: float = 0.0,
    noise_figure_db: float = 1.0,
    extra_t_sys: float = 30.0,
    aperture_efficiency: float = 0.6,
    bandwidth_hz: float = 1.0e7,
    gain_mv_per_k: float = 100.0,
    mv_per_division: float = 50.0,
    chart_speed_mm_per_s: float = 1.0,
    pad_beamwidths: float = 3.0,
    sample_rate_hz: float = 5.0,
    seed: int | None = 0,
) -> DriftScan:
    """Simulate a drift scan of a point/extended source with a total-power radiometer.

    The dish sits still and the source drifts through the beam at the sidereal rate
    (:func:`beam_transit_duration`). The on-sky response is a Gaussian beam; a finite
    source of angular size ``source_size_deg`` broadens it (added in quadrature) and
    dilutes the peak. The source raises the antenna temperature by
    :math:`T_A = \\eta_a S A_\\mathrm{geom} / (2 k_B)` (point-source limit), where
    :math:`A_\\mathrm{geom} = \\pi D^2/4`; the receiver noise figure sets
    :math:`T_\\mathrm{rx}` and hence :math:`T_\\mathrm{sys}`; and the radiometer equation
    (:func:`jansky.signals.radiometer_sensitivity`) sets the noise on the trace. The
    output is the chart-recorder deflection in millivolts versus time and chart position.

    Parameters
    ----------
    flux_jy
        Source flux density (Jy).
    dec_deg
        Source declination (deg) -- sets the drift rate through the beam.
    fwhm_deg
        Beam full-width at half-maximum (deg).
    diameter_m
        Dish diameter (m) -- sets the collecting area.
    source_size_deg
        Source angular FWHM (deg); 0 for a point source. Broadens the trace and
        dilutes the peak by beam filling.
    noise_figure_db
        Receiver noise figure (dB) -> receiver temperature.
    extra_t_sys
        Sky + spillover + ground contribution added to the receiver temperature (K).
    aperture_efficiency
        Aperture efficiency :math:`\\eta_a` relating geometric to effective area.
    bandwidth_hz
        Pre-detection bandwidth (Hz).
    gain_mv_per_k
        Back-end gain converting antenna temperature to chart deflection (mV/K).
    mv_per_division
        Chart vertical scale (mV per division) -- for reporting in divisions.
    chart_speed_mm_per_s
        Chart paper speed (mm/s) -- sets the horizontal scale.
    pad_beamwidths
        How many beam FWHM of baseline to simulate on each side of transit.
    sample_rate_hz
        Samples per second of the recorded trace.
    seed
        RNG seed for the radiometer noise (``None`` for fresh noise).

    Returns
    -------
    DriftScan
        Time, deflection (mV), chart position (mm), and summary diagnostics.
    """
    from .signals import gaussian_beam, rng

    if flux_jy < 0 or fwhm_deg <= 0 or diameter_m <= 0:
        raise ValueError("flux_jy must be >= 0 and fwhm_deg, diameter_m > 0")

    k_b = 1.380649e-23  # Boltzmann constant (J/K)
    jy = 1.0e-26  # 1 Jy in W m^-2 Hz^-1

    # collecting area and point-source antenna temperature
    a_geom = np.pi * (diameter_m / 2.0) ** 2
    a_eff = aperture_efficiency * a_geom
    t_a_point = flux_jy * jy * a_eff / (2.0 * k_b)

    # a finite source broadens the effective beam (quadrature) and dilutes the peak
    eff_fwhm_deg = float(np.hypot(fwhm_deg, source_size_deg))
    dilution = (fwhm_deg / eff_fwhm_deg) ** 2  # peak filling factor (<= 1)
    peak_t_a = t_a_point * dilution

    # system temperature and the per-sample radiometer noise
    t_rx = noise_figure_to_temperature(noise_figure_db)
    t_sys = t_rx + extra_t_sys
    tau = 1.0 / sample_rate_hz
    noise_k = t_sys / np.sqrt(bandwidth_hz * tau)

    # time axis: the source drifts through the (broadened) beam at the sidereal rate
    transit_s = beam_transit_duration(fwhm_deg, dec_deg)
    eff_transit_s = beam_transit_duration(eff_fwhm_deg, dec_deg)
    half_span = pad_beamwidths * eff_transit_s
    n = int(2 * half_span * sample_rate_hz) + 1
    time_s = np.linspace(0.0, 2 * half_span, n)
    # angular offset of the source from beam centre, in degrees, vs time
    drift_rate = SIDEREAL_RATE_DEG_PER_S * np.cos(np.radians(dec_deg))
    offset_deg = (time_s - half_span) * drift_rate

    beam = gaussian_beam(offset_deg, eff_fwhm_deg)  # normalised power, peak 1
    t_a = peak_t_a * beam

    noise = rng(seed).normal(0.0, noise_k, size=n)
    deflection_mv = gain_mv_per_k * (t_a + noise)

    peak_mv = float(gain_mv_per_k * peak_t_a)
    noise_mv = float(gain_mv_per_k * noise_k)
    snr = float(peak_t_a / noise_k) if noise_k > 0 else float("inf")
    chart_mm = time_s * chart_speed_mm_per_s

    # mv_per_division is carried for reporting (deflection in divisions = mv / mv_per_division)
    _ = mv_per_division

    return DriftScan(
        time_s=time_s,
        deflection_mv=deflection_mv,
        chart_mm=chart_mm,
        peak_mv=peak_mv,
        peak_t_a=float(peak_t_a),
        t_sys=float(t_sys),
        noise_mv=noise_mv,
        snr=snr,
        transit_s=float(transit_s),
    )
