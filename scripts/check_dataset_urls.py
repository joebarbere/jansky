#!/usr/bin/env python3
"""Check that every URL in jansky.data.DATASETS still resolves.

Sends a lightweight request per dataset (HEAD, falling back to a ranged GET for
hosts that reject HEAD) and reports the HTTP status and size. Intended to be run
manually or on a schedule — archive/raw-GitHub URLs rot, and a green run is the
evidence the starter datasets are still fetchable.

Usage::

    uv run python scripts/check_dataset_urls.py
    uv run python scripts/check_dataset_urls.py --category small

Exits non-zero if any URL fails, so it can gate CI.
"""

from __future__ import annotations

import argparse
import sys

import requests

from jansky.data import DATASETS


def check(url: str, timeout: float = 30.0) -> tuple[bool, str]:
    """Return (ok, detail) for a single URL."""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code >= 400 or resp.status_code == 405:
            # Some hosts reject HEAD; retry with a 0-byte ranged GET.
            resp = requests.get(url, headers={"Range": "bytes=0-0"}, stream=True, timeout=timeout)
        ok = resp.status_code < 400
        size = resp.headers.get("content-length", "?")
        return ok, f"HTTP {resp.status_code}, {size} bytes"
    except Exception as exc:  # noqa: BLE001 - report any failure
        return False, f"ERROR: {exc}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", choices=["small", "large"], help="only check one category")
    args = parser.parse_args(argv)

    failures = 0
    for name in sorted(DATASETS):
        spec = DATASETS[name]
        if args.category and spec.category != args.category:
            continue
        ok, detail = check(spec.url)
        flag = "ok " if ok else "FAIL"
        print(f"[{flag}] {name:22s} {detail}")
        if not ok:
            failures += 1

    if failures:
        print(f"\n{failures} dataset URL(s) failed.", file=sys.stderr)
        return 1
    print("\nAll dataset URLs resolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
