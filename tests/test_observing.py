"""Tests for jansky.observing -- sidereal time, transit, beam transit, drift scans."""

from __future__ import annotations

import numpy as np
import pytest

from jansky import observing


def test_gmst_at_j2000():
    """GMST at J2000.0 (JD 2451545.0) is the canonical 18h 41m 50.5s = 18.69737 h."""
    gst = observing.greenwich_sidereal_time(2451545.0)
    assert abs(gst - 18.697374558) < 1e-4


def test_lst_adds_longitude():
    """LST = GMST + longitude/15, wrapped to [0, 24)."""
    jd = 2451545.0
    gst = observing.greenwich_sidereal_time(jd)
    lst = observing.local_sidereal_time(jd, longitude_deg=-90.0)  # 6h west
    assert abs(lst - ((gst - 6.0) % 24.0)) < 1e-9


def test_hour_angle_wraps_and_zero_at_transit():
    assert abs(observing.hour_angle(10.0, 10.0)) < 1e-9  # LST == RA -> transit
    assert abs(observing.hour_angle(1.0, 23.0) - 2.0) < 1e-9  # wraps across 0h
    assert -12.0 <= observing.hour_angle(5.0, 20.0) < 12.0


def test_altitude_at_transit_matches_general_altitude():
    """At H = 0 the general altitude formula must equal 90 - |lat - dec|."""
    for dec, lat in [(22.0, 52.0), (-43.0, -30.0), (0.0, 40.0)]:
        a_general = observing.altitude(dec, lat, 0.0)
        a_transit = observing.altitude_at_transit(dec, lat)
        assert abs(a_general - a_transit) < 1e-9


def test_altitude_below_horizon_is_negative():
    # a far-southern source from a northern site never gets up
    assert observing.altitude_at_transit(dec_deg=-60.0, lat_deg=52.0) < 0


def test_is_circumpolar():
    assert observing.is_circumpolar(dec_deg=80.0, lat_deg=52.0)  # 80 >= 90-52
    assert not observing.is_circumpolar(dec_deg=0.0, lat_deg=52.0)
    assert observing.is_circumpolar(dec_deg=-80.0, lat_deg=-52.0)  # southern hemisphere


def test_hours_to_transit():
    assert abs(observing.hours_to_transit(10.0, 10.0)) < 1e-9  # already transiting
    # 6 sidereal hours ahead -> slightly fewer solar hours
    dt = observing.hours_to_transit(0.0, 6.0)
    assert abs(dt - 6.0 / observing.SOLAR_TO_SIDEREAL) < 1e-9
    assert dt < 6.0


def test_beam_transit_one_degree_is_four_minutes_at_equator():
    """A 1-degree beam takes ~4 minutes to drift through at the celestial equator."""
    t = observing.beam_transit_duration(fwhm_deg=1.0, dec_deg=0.0)
    assert abs(t - 239.34) < 1.0
    assert abs(t / 60.0 - 3.99) < 0.05


def test_beam_transit_stretches_as_sec_dec():
    """Time in the beam scales as 1/cos(dec): doubles at dec = 60 deg."""
    t0 = observing.beam_transit_duration(1.0, 0.0)
    t60 = observing.beam_transit_duration(1.0, 60.0)
    assert abs(t60 / t0 - 2.0) < 1e-6


def test_beam_transit_diverges_at_pole():
    with pytest.raises(ValueError):
        observing.beam_transit_duration(1.0, 90.0)


def test_noise_figure_to_temperature():
    assert abs(observing.noise_figure_to_temperature(0.0)) < 1e-9  # 0 dB -> 0 K
    assert abs(observing.noise_figure_to_temperature(3.0) - 290.0 * (10**0.3 - 1)) < 1e-6


def test_drift_scan_runs_and_is_self_consistent():
    scan = observing.simulate_drift_scan(
        flux_jy=100.0, dec_deg=0.0, fwhm_deg=0.5, diameter_m=25.0, seed=0
    )
    assert scan.peak_t_a > 0 and scan.peak_mv > 0
    assert scan.snr > 10  # a 100 Jy source on a 25 m dish is a strong detection
    # the trace's transit time matches the standalone beam-transit calculation
    assert abs(scan.transit_s - observing.beam_transit_duration(0.5, 0.0)) < 1e-6
    # chart position is time x speed
    assert np.allclose(scan.chart_mm, scan.time_s)  # default 1 mm/s


def test_drift_scan_brighter_source_gives_higher_snr():
    faint = observing.simulate_drift_scan(flux_jy=10.0, dec_deg=0.0, fwhm_deg=0.5, diameter_m=25.0)
    bright = observing.simulate_drift_scan(
        flux_jy=100.0, dec_deg=0.0, fwhm_deg=0.5, diameter_m=25.0
    )
    assert bright.snr > faint.snr


def test_drift_scan_extended_source_dilutes_peak():
    point = observing.simulate_drift_scan(flux_jy=100.0, dec_deg=0.0, fwhm_deg=0.5, diameter_m=25.0)
    extended = observing.simulate_drift_scan(
        flux_jy=100.0, dec_deg=0.0, fwhm_deg=0.5, diameter_m=25.0, source_size_deg=0.5
    )
    assert extended.peak_t_a < point.peak_t_a  # beam dilution lowers the peak
