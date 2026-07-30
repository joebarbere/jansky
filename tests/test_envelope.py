"""Tests for jansky.envelope — the back-of-the-envelope checker."""

from __future__ import annotations

import pytest

from jansky.envelope import check


def test_none_guess_prompts_and_returns_false(capsys):
    assert check(None, 9.0, name="tau") is False
    out = capsys.readouterr().out
    assert "no guess yet" in out
    assert "tau" in out


def test_exact_guess_is_envelope_grade(capsys):
    assert check(9.0, 9.0, name="tau", units="s") is True
    out = capsys.readouterr().out
    assert "0.00 decades" in out
    assert "Envelope-grade" in out
    assert " s " in out or " s\n" in out or "9 s" in out


def test_within_half_decade_passes():
    assert check(9.0 * 10**0.49, 9.0) is True
    assert check(9.0 / 10**0.49, 9.0) is True


def test_right_order_of_magnitude_fails_gently(capsys):
    assert check(9.0 * 10**0.8, 9.0) is False
    assert "Right order of magnitude" in capsys.readouterr().out


def test_decades_off_hints_at_units(capsys):
    assert check(9000.0, 9.0) is False
    assert "units slip" in capsys.readouterr().out


def test_custom_dex_widens_the_band():
    assert check(80.0, 9.0, dex=1.0) is True


@pytest.mark.parametrize("bad", [-3.0, 0.0, float("nan"), float("inf")])
def test_nonpositive_or_nonfinite_guess_is_gentle(bad, capsys):
    assert check(bad, 9.0) is False
    assert "positive, finite" in capsys.readouterr().out


@pytest.mark.parametrize("bad", [0.0, -1.0, float("nan")])
def test_bad_expected_raises(bad):
    with pytest.raises(ValueError, match="expected must be"):
        check(1.0, bad)


def test_expected_log10_equivalent_to_expected(capsys):
    assert check(9.0, expected_log10=0.9542, name="tau", units="s") is True
    out = capsys.readouterr().out
    assert "Envelope-grade" in out
    assert "~9" in out  # the printed comparison recovers the real value


def test_expected_log10_none_guess_does_not_leak(capsys):
    assert check(None, expected_log10=0.9542) is False
    out = capsys.readouterr().out
    assert "no guess yet" in out
    assert "9" not in out  # nothing about the answer before a guess


def test_exactly_one_expected_form_required():
    with pytest.raises(ValueError, match="exactly one"):
        check(1.0, 9.0, expected_log10=0.9542)
    with pytest.raises(ValueError, match="exactly one"):
        check(1.0)


def test_nonfinite_expected_log10_raises():
    with pytest.raises(ValueError, match="expected_log10 must be"):
        check(1.0, expected_log10=float("nan"))
