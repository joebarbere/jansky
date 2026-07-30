"""Order-of-magnitude feedback for the chapters' "Back of the envelope" sections.

Each chapter opens with a back-of-the-envelope estimate the reader commits to
*before* the full treatment. :func:`check` grades such a guess the way an
envelope deserves: by decades, not decimal places. It is classroom plumbing,
deliberately free of physics — the one line that matters is::

    decades = abs(log10(guess / expected))

It never raises on learner input and treats a still-``None`` guess as "not
attempted yet", so notebooks that call it execute cleanly in CI whether or not
the reader has filled anything in.
"""

from __future__ import annotations

import math

__all__ = ["check"]


def check(
    guess: float | None,
    expected: float,
    *,
    dex: float = 0.5,
    name: str = "estimate",
    units: str = "",
) -> bool:
    """Compare an order-of-magnitude guess against the worked envelope answer.

    Parameters
    ----------
    guess
        The reader's estimate, or ``None`` if not attempted yet.
    expected
        The worked envelope answer, in the same units as ``guess``.
        Must be positive and finite (this is the author's input, so a bad
        value raises rather than prints).
    dex
        Half-width of the "envelope-grade" band, in decades (default 0.5).
    name
        Short label for the printed feedback, e.g. ``"time to 5 sigma"``.
    units
        Unit string appended to the printed numbers, e.g. ``"s"``.

    Returns
    -------
    bool
        ``True`` when the guess lands within ``dex`` decades of ``expected``.
    """
    if not math.isfinite(expected) or expected <= 0:
        raise ValueError("expected must be a positive, finite number")
    unit = f" {units}" if units else ""
    if guess is None:
        print(f"[{name}] no guess yet — fill in the cell above, then re-run this one.")
        return False
    if not isinstance(guess, (int, float)) or not math.isfinite(guess) or guess <= 0:
        print(f"[{name}] {guess!r} is not a positive, finite number — check signs and units.")
        return False
    decades = abs(math.log10(guess / expected))
    print(
        f"[{name}] your {guess:.3g}{unit} vs ~{expected:.3g}{unit} → {decades:.2f} decades apart."
    )
    if decades <= dex:
        print("Envelope-grade agreement — decades matter, factors of two don't. ✓")
        return True
    if decades <= 1.0:
        print("Right order of magnitude — sharpen it: recheck the factors you rounded away.")
        return False
    print(
        f"That is {decades:.1f} decades off — on a napkin that usually means a units slip "
        "(Hz vs MHz, seconds vs hours)."
    )
    return False
