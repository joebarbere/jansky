"""Radio-astronomy data formats and the software ecosystem.

This module is the helper layer behind the course's *"Data formats & talking to
the ecosystem"* material (Chapter 16). It implements the formats and protocols we
can follow to a public specification, and is deliberately honest about the ones we
cannot yet verify byte-for-byte.

What's implemented here, to spec
--------------------------------
* **GUPPI raw** voltage files — the FITS-like 80-byte ASCII card header used by
  Green Bank / Breakthrough Listen, plus a minimal writer so the course can make
  its own example files. (:func:`read_guppi_header`, :func:`write_guppi`,
  :func:`iter_guppi_blocks`.)
* **SigMF** — the open Signal Metadata Format: a JSON ``.sigmf-meta`` sidecar plus
  a raw ``.sigmf-data`` file. (:func:`read_sigmf`, :func:`write_sigmf`.)
* **Radio-Sky Spectrograph (RSS) network protocol** — the TCP/IP feed documented
  in *"How to Talk to Radio-Sky Spectrograph"* and the ``myriadrf/RASDR`` socket
  commit: a ``F …|S …|O …|C …|`` handshake then 2-byte little-endian ("LoHi")
  spectra, highest channel first, each sweep ended by ``0xFE 0xFE``.
  (:class:`RSSClient`, :class:`MockRSSServer`.)
* **SPS** (Radio-Sky Spectrograph spectrogram file) and **SPD** (Radio-SkyPipe
  strip-chart file). The binary layout — a 156-byte little-endian header, a
  ``0xFF``-delimited notes block, then big-endian ``uint16`` sweeps (SPS) or
  ``int16``/``float64`` time samples (SPD) — is documented at
  ``radiosky.com/skypipehelp/V2/datastructure.html``. :func:`read_sps` is
  validated byte-for-byte against a real Radio JOVE recording (AJ4CO/Typinski via
  the MASER archive); :func:`read_spd` follows the same spec (round-trip tested).

What's deferred to mature libraries
-----------------------------------
* **Filterbank / HDF5 / Measurement Set / UVFITS** — handled by mature libraries
  (``blimpy``, ``pyuvdata``); :func:`read_filterbank` is a thin, optional wrapper.
"""

from __future__ import annotations

import json
import socket
import struct
import threading
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

__all__ = [
    "Spectrogram",
    "save_spectrogram",
    "load_spectrogram",
    "read_guppi_header",
    "write_guppi",
    "iter_guppi_blocks",
    "read_sigmf",
    "write_sigmf",
    "RSSClient",
    "MockRSSServer",
    "rss_handshake",
    "encode_rss_sweep",
    "decode_rss_sweep",
    "read_filterbank",
    "read_sps",
    "read_spd",
]


# --------------------------------------------------------------------------- #
# A small, transparent container the notebooks/tests pass around.
# --------------------------------------------------------------------------- #
@dataclass
class Spectrogram:
    """A simple dynamic spectrum: power over (time, frequency)."""

    times: np.ndarray  #: shape (n_time,), seconds
    freqs: np.ndarray  #: shape (n_chan,), Hz
    power: np.ndarray  #: shape (n_time, n_chan)
    meta: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.power = np.asarray(self.power)
        if self.power.shape != (len(self.times), len(self.freqs)):
            raise ValueError("power must have shape (len(times), len(freqs))")


def save_spectrogram(path: str | Path, spec: Spectrogram) -> Path:
    """Save a :class:`Spectrogram` to a transparent ``.npz`` container.

    This is the course's own portable format for passing spectrograms between
    notebooks; it is *not* one of the wire formats. For the real ones, see the
    GUPPI/SigMF/RSS functions in this module and ``docs/data-formats.md``.
    """
    path = Path(path)
    np.savez_compressed(
        path,
        times=spec.times,
        freqs=spec.freqs,
        power=spec.power,
        meta=json.dumps(spec.meta),
    )
    return path if path.suffix == ".npz" else path.with_suffix(".npz")


def load_spectrogram(path: str | Path) -> Spectrogram:
    """Load a :class:`Spectrogram` written by :func:`save_spectrogram`."""
    with np.load(Path(path), allow_pickle=False) as data:
        return Spectrogram(
            times=data["times"],
            freqs=data["freqs"],
            power=data["power"],
            meta=json.loads(str(data["meta"])),
        )


# --------------------------------------------------------------------------- #
# GUPPI raw  (Green Bank Ultimate Pulsar Processing Instrument; used by BL).
# Header = 80-byte ASCII cards "KEYWORD = value", string values single-quoted,
# terminated by an "END" card; then BLOCSIZE bytes of voltage data ordered
# [channel][time][polarization], complex 8-bit (int8 real, int8 imag).
# --------------------------------------------------------------------------- #
_CARD = 80


def _format_card(key: str, value) -> bytes:
    if isinstance(value, str):
        valstr = f"'{value}'"
    elif isinstance(value, float):
        valstr = repr(value)
    else:
        valstr = str(value)
    card = f"{key:<8}= {valstr}"
    return card.encode("ascii")[:_CARD].ljust(_CARD)


def _parse_value(raw: str):
    raw = raw.strip()
    if raw.startswith("'"):
        return raw.strip("'").strip()
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw


def read_guppi_header(path: str | Path) -> dict:
    """Parse the ASCII card header of a GUPPI raw file into a dict.

    Reads only the header of the first block (cheap); does not touch the
    voltages. Keys such as ``BLOCSIZE``, ``OBSNCHAN``, ``NPOL``, ``NBITS``,
    ``OBSFREQ``, ``OBSBW``, ``TBIN`` follow the Breakthrough Listen usage.
    """
    header: dict = {}
    with open(path, "rb") as fh:
        while True:
            card = fh.read(_CARD)
            if len(card) < _CARD:
                raise ValueError("truncated GUPPI header (no END card)")
            text = card.decode("ascii", errors="replace")
            key = text[:8].strip()
            if key == "END":
                break
            if "=" in text:
                _, _, rest = text.partition("=")
                header[key] = _parse_value(rest)
    return header


def write_guppi(
    path: str | Path,
    data: np.ndarray,
    header: dict | None = None,
) -> Path:
    """Write a minimal, valid single-block GUPPI raw file.

    Parameters
    ----------
    path
        Output path (``.0000.raw`` by convention).
    data
        Complex voltages, shape ``(nchan, ntime, npol)``. Stored as interleaved
        int8 real/imag (the only quantisation GUPPI raw supports here).
    header
        Extra/overriding header cards. ``BLOCSIZE``, ``OBSNCHAN``, ``NPOL`` and
        ``NBITS`` are filled in from ``data`` if absent.
    """
    data = np.asarray(data)
    if data.ndim != 3:
        raise ValueError("data must be (nchan, ntime, npol)")
    nchan, _, npol = data.shape
    # int8 real/imag interleaved, in [channel][time][pol] order.
    iq = np.empty(data.shape + (2,), dtype=np.int8)
    iq[..., 0] = np.clip(np.round(data.real), -128, 127)
    iq[..., 1] = np.clip(np.round(data.imag), -128, 127)
    payload = iq.tobytes()

    cards = {
        "BLOCSIZE": len(payload),
        "OBSNCHAN": nchan,
        "NPOL": npol,
        "NBITS": 8,
        "DIRECTIO": 0,
    }
    if header:
        cards.update(header)

    path = Path(path)
    with open(path, "wb") as fh:
        for key, value in cards.items():
            fh.write(_format_card(key, value))
        fh.write(_format_card("END", "")[:3].ljust(_CARD))
        fh.write(payload)
    return path


def iter_guppi_blocks(path: str | Path):
    """Yield ``(header, voltages)`` for each block in a GUPPI raw file.

    ``voltages`` is a complex ``(nchan, ntime, npol)`` array reconstructed from
    the interleaved int8 samples. Reads lazily, one block at a time.
    """
    with open(path, "rb") as fh:
        while True:
            header: dict = {}
            start = fh.tell()
            chunk = fh.read(_CARD)
            if not chunk:
                return
            # rewind and parse cards until END
            fh.seek(start)
            while True:
                card = fh.read(_CARD)
                if len(card) < _CARD:
                    return
                text = card.decode("ascii", errors="replace")
                key = text[:8].strip()
                if key == "END":
                    break
                if "=" in text:
                    _, _, rest = text.partition("=")
                    header[key] = _parse_value(rest)
            nchan = int(header["OBSNCHAN"])
            npol = int(header["NPOL"])
            blocsize = int(header["BLOCSIZE"])
            raw = fh.read(blocsize)
            if len(raw) < blocsize:
                return
            iq = np.frombuffer(raw, dtype=np.int8).reshape(nchan, -1, npol, 2)
            volts = iq[..., 0].astype(np.float32) + 1j * iq[..., 1].astype(np.float32)
            yield header, volts


# --------------------------------------------------------------------------- #
# SigMF — open Signal Metadata Format (https://sigmf.org).
# Two files: <base>.sigmf-meta (JSON) and <base>.sigmf-data (raw samples).
# --------------------------------------------------------------------------- #
_SIGMF_DTYPES: dict[str, np.dtype] = {
    "cf32_le": np.dtype("<c8"),
    "cf64_le": np.dtype("<c16"),
    "ci16_le": np.dtype("<i2"),  # interleaved I/Q handled below
    "ci8": np.dtype("i1"),
    "rf32_le": np.dtype("<f4"),
}


def write_sigmf(
    basepath: str | Path,
    samples: np.ndarray,
    sample_rate: float,
    *,
    datatype: str = "cf32_le",
    center_freq: float | None = None,
    extra_global: dict | None = None,
) -> tuple[Path, Path]:
    """Write a SigMF recording (``.sigmf-meta`` + ``.sigmf-data``).

    Supports the common complex-float case (``cf32_le``); for other datatypes the
    caller is responsible for passing an already-correctly-typed array.
    """
    base = Path(basepath)
    data_path = base.with_suffix(".sigmf-data")
    meta_path = base.with_suffix(".sigmf-meta")

    if datatype == "cf32_le":
        np.asarray(samples, dtype="<c8").tofile(data_path)
    else:
        np.asarray(samples).tofile(data_path)

    glob = {
        "core:datatype": datatype,
        "core:sample_rate": float(sample_rate),
        "core:version": "1.0.0",
        "core:num_channels": 1,
    }
    if extra_global:
        glob.update(extra_global)
    capture: dict[str, float] = {"core:sample_start": 0}
    if center_freq is not None:
        capture["core:frequency"] = float(center_freq)
    meta = {"global": glob, "captures": [capture], "annotations": []}
    meta_path.write_text(json.dumps(meta, indent=2))
    return meta_path, data_path


def read_sigmf(basepath: str | Path) -> tuple[np.ndarray, dict]:
    """Read a SigMF recording, returning ``(samples, metadata)``."""
    base = Path(basepath)
    meta = json.loads(base.with_suffix(".sigmf-meta").read_text())
    datatype = str(meta["global"]["core:datatype"])
    dtype: np.dtype = _SIGMF_DTYPES.get(datatype, np.dtype("<c8"))
    samples = np.fromfile(base.with_suffix(".sigmf-data"), dtype=dtype)
    return samples, meta


# --------------------------------------------------------------------------- #
# Radio-Sky Spectrograph (RSS) network protocol.
# Documented in "How to Talk to Radio-Sky Spectrograph" (cygnusa) and the
# myriadrf/RASDR socket commit. RSS listens on 127.0.0.1:8888. On connect the
# client sends an ASCII config: "F <Hz>|S <Hz>|O <Hz>|C <nchan>|". Each sweep is
# nchan little-endian ("LoHi") uint16 samples (12-bit data), highest channel
# first, followed by the terminator bytes 0xFE 0xFE. No timestamps, no acks.
# --------------------------------------------------------------------------- #
RSS_DEFAULT_PORT = 8888
RSS_TERMINATOR = b"\xfe\xfe"
RSS_MAX_VALUE = 0x0FFF  # 12-bit


def rss_handshake(center_hz: int, bandwidth_hz: int, n_channels: int, offset_hz: int = 0) -> bytes:
    """Build the RSS connect/config string, e.g. ``F 21000000|S 5000000|O 0|C 500|``."""
    if not (100 <= n_channels <= 512):
        raise ValueError("RSS supports 100–512 channels")
    return (
        f"F {int(center_hz)}|S {int(bandwidth_hz)}|O {int(offset_hz)}|C {int(n_channels)}|"
    ).encode("ascii")


def encode_rss_sweep(power: np.ndarray, *, high_freq_first: bool = True) -> bytes:
    """Encode one spectrum as an RSS sweep (LoHi uint16, high channel first, 0xFE 0xFE).

    ``power`` is clipped to the 12-bit range. If ``high_freq_first`` and the input
    is ordered low→high, it is reversed to match the RSS convention.
    """
    vals = np.clip(np.rint(np.asarray(power)), 0, RSS_MAX_VALUE).astype("<u2")
    if high_freq_first:
        vals = vals[::-1]
    return vals.tobytes() + RSS_TERMINATOR


def decode_rss_sweep(blob: bytes, *, high_freq_first: bool = True) -> np.ndarray:
    """Inverse of :func:`encode_rss_sweep` (terminator optional in ``blob``)."""
    if blob.endswith(RSS_TERMINATOR):
        blob = blob[: -len(RSS_TERMINATOR)]
    vals = np.frombuffer(blob, dtype="<u2").astype(int)
    return vals[::-1] if high_freq_first else vals


class RSSClient:
    """A minimal client that streams spectra to Radio-Sky Spectrograph over TCP.

    Use as a context manager::

        with RSSClient(center_hz=21_000_000, bandwidth_hz=5_000_000,
                       n_channels=256, host="127.0.0.1") as rss:
            for sweep in spectra:        # each: array of n_channels powers
                rss.send_sweep(sweep)
    """

    def __init__(
        self,
        center_hz: int,
        bandwidth_hz: int,
        n_channels: int,
        *,
        host: str = "127.0.0.1",
        port: int = RSS_DEFAULT_PORT,
        offset_hz: int = 0,
    ) -> None:
        self.center_hz = center_hz
        self.bandwidth_hz = bandwidth_hz
        self.n_channels = n_channels
        self.offset_hz = offset_hz
        self.host = host
        self.port = port
        self._sock: socket.socket | None = None

    def connect(self) -> None:
        self._sock = socket.create_connection((self.host, self.port))
        self._sock.sendall(
            rss_handshake(self.center_hz, self.bandwidth_hz, self.n_channels, self.offset_hz)
        )

    def send_sweep(self, power: np.ndarray) -> None:
        if self._sock is None:
            raise RuntimeError("call connect() first")
        if len(power) != self.n_channels:
            raise ValueError(f"expected {self.n_channels} channels, got {len(power)}")
        self._sock.sendall(encode_rss_sweep(power))

    def close(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def __enter__(self) -> RSSClient:
        self.connect()
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class MockRSSServer:
    """An in-process stand-in for Radio-Sky Spectrograph, for tests and notebooks.

    Accepts one :class:`RSSClient` connection, parses the handshake and the
    ``0xFE 0xFE``-delimited sweeps, and exposes them via :attr:`config` and
    :attr:`sweeps` once the client disconnects. Runs entirely offline.

    Example::

        server = MockRSSServer(); server.start()
        with RSSClient(..., host="127.0.0.1", port=server.port) as rss:
            rss.send_sweep(sweep)
        server.join()
        assert server.config["C"] == n_channels
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0) -> None:
        self._srv = socket.create_server((host, port))
        self.host, self.port = self._srv.getsockname()
        self.config: dict = {}
        self.sweeps: list[np.ndarray] = []
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _serve(self) -> None:
        conn, _ = self._srv.accept()
        with conn:
            buf = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                buf += chunk
        self._srv.close()
        # The handshake "F …|S …|O …|C <n>|" precedes the binary sweeps.
        text_end = buf.find(b"|C ")
        bar = buf.find(b"|", text_end + 3)
        config_bytes, rest = buf[: bar + 1], buf[bar + 1 :]
        for token in config_bytes.decode("ascii").split("|"):
            token = token.strip()
            if token:
                key, _, val = token.partition(" ")
                self.config[key] = int(val)
        for raw in rest.split(RSS_TERMINATOR):
            if raw:
                self.sweeps.append(decode_rss_sweep(raw))

    def join(self, timeout: float = 5.0) -> None:
        self._thread.join(timeout)


# --------------------------------------------------------------------------- #
# Optional / deferred readers.
# --------------------------------------------------------------------------- #
def read_filterbank(path: str | Path):
    """Read a SIGPROC filterbank / HDF5 file via ``blimpy`` (optional dependency).

    Install with ``uv sync --extra seti``. Kept as a thin wrapper so the rest of
    ``jansky`` has no hard dependency on the Breakthrough Listen stack.
    """
    try:
        from blimpy import Waterfall
    except ImportError as exc:  # pragma: no cover - optional path
        raise ImportError("read_filterbank needs blimpy: `uv sync --extra seti`") from exc
    return Waterfall(str(path))


# --------------------------------------------------------------------------- #
# Radio-Sky Spectrograph (.sps) and Radio-SkyPipe (.spd) files.
#
# Shared layout (radiosky.com/skypipehelp/V2/datastructure.html), validated
# against a real Radio JOVE .sps recording:
#   * 156-byte little-endian primary header (struct _SPX_HDR_FMT);
#   * a `note_length`-byte notes block: free text, then key/value pairs bracketed
#     by `*[[*` ... `*]]*` and delimited by 0xFF (no key/value separator);
#   * the data records (big-endian uint16 sweeps for SPS; int16/float64 time
#     samples for SPD).
# Times in the header are decimal days since 1899-12-30 00:00; add 2415018.5 for
# the Julian Date. NB: the header is little-endian but SPS *sample* data is
# big-endian -- the non-obvious detail that makes validating on real bytes vital.
# --------------------------------------------------------------------------- #

_SPX_HDR_FMT = "<10s6d1h10s20s20s40s1h1i"
_SPX_HDR_LEN = 156
_SPX_EPOCH_JD = 2415018.5  # JD of 1899-12-30 00:00
_SPX_SYNC = 0xFEFE  # trailing sweep delimiter in SPS records


def _spx_header(raw: bytes) -> dict:
    """Decode the 156-byte SPS/SPD primary header."""
    if len(raw) < _SPX_HDR_LEN:
        raise ValueError("file is shorter than the 156-byte SPS/SPD header")
    v = struct.unpack(_SPX_HDR_FMT, raw[:_SPX_HDR_LEN])

    def _s(b: bytes) -> str:
        return b.decode("latin1").strip("\x00").strip()

    return {
        "software": _s(v[0]),
        "start_jd": v[1] + _SPX_EPOCH_JD,
        "stop_jd": v[2] + _SPX_EPOCH_JD,
        "latitude": v[3],
        "longitude": v[4],
        "chartmax": v[5],
        "chartmin": v[6],
        "timezone": v[7],
        "source": _s(v[8]),
        "author": _s(v[9]),
        "obsname": _s(v[10]),
        "obsloc": _s(v[11]),
        "nchannels": v[12],
        "note_length": v[13],
    }


def _spx_notes(raw_notes: bytes) -> tuple[str, list[str]]:
    """Split a notes block into (free_text, [key/value items]).

    Items live between ``*[[*`` and ``*]]*`` and are separated by ``0xFF``.
    """
    start = raw_notes.find(b"*[[*")
    stop = raw_notes.find(b"*]]*")
    if start < 0 or stop < 0:
        return raw_notes.decode("latin1", "replace"), []
    free_text = raw_notes[:start].decode("latin1", "replace")
    items = [it.decode("latin1") for it in raw_notes[start + 4 : stop].split(b"\xff")]
    return free_text, items


def _spx_note(items: list[str], key: str) -> str | None:
    """Value of the first note item starting with ``key`` (or ``None``)."""
    for it in items:
        if it.startswith(key):
            return it[len(key) :]
    return None


def _sps_feed_names(items: list[str], nfeed: int) -> list[str]:
    """Polarisation labels for the feeds, read from the BANNER notes when present."""
    if nfeed == 1:
        return ["S"]
    names = []
    for i in range(nfeed):
        banner = (_spx_note(items, f"BANNER{i}") or "").upper()
        names.append("RR" if "RCP" in banner else "LL" if "LCP" in banner else f"CH{i}")
    return names


def read_sps(path: str | Path) -> Spectrogram:
    """Read a Radio-Sky Spectrograph ``.sps`` spectrogram file.

    Returns a :class:`Spectrogram` whose ``power`` is the first feed's dynamic
    spectrum ``(n_sweep, n_channel)``. For a dual-polarisation file, both feeds
    are in ``meta["feeds"]`` (keyed by ``"RR"``/``"LL"``/``"S"``). ``freqs`` runs
    from the high to the low band edge (Hz); ``times`` is seconds since the start.
    ``meta`` carries the full header and the parsed notes.

    Validated byte-for-byte against a real Radio JOVE recording (AJ4CO/Typinski).
    """
    raw = Path(path).read_bytes()
    hdr = _spx_header(raw)
    note_len = hdr["note_length"]
    free_text, items = _spx_notes(raw[_SPX_HDR_LEN : _SPX_HDR_LEN + note_len])

    nfreq = hdr["nchannels"]
    nfeed = 2 if (_spx_note(items, "DUALSPECFILE") or "").strip() == "True" else 1
    lowf = float(_spx_note(items, "LOWF") or "nan")
    hif = float(_spx_note(items, "HIF") or "nan")

    bytes_per_step = (nfreq * nfeed + 1) * 2  # +1 = trailing 0xFEFE sync sample
    body = raw[_SPX_HDR_LEN + note_len :]
    nstep = len(body) // bytes_per_step
    if nstep == 0:
        raise ValueError("no complete SPS sweeps found after the header/notes")

    sweeps = np.frombuffer(body[: nstep * bytes_per_step], dtype=">u2").reshape(
        nstep, nfreq * nfeed + 1
    )
    # Samples are ordered (channel, feed); the last column is the sync delimiter.
    samples = sweeps[:, : nfreq * nfeed].reshape(nstep, nfreq, nfeed).astype(float)

    freqs = np.linspace(hif, lowf, nfreq)  # Hz, high edge first
    duration_s = (hdr["stop_jd"] - hdr["start_jd"]) * 86400.0
    times = np.linspace(0.0, duration_s, nstep, endpoint=False) if nstep > 1 else np.zeros(1)

    feed_names = _sps_feed_names(items, nfeed)
    feeds = {name: samples[:, :, i] for i, name in enumerate(feed_names)}

    meta = {
        **hdr,
        "file_type": "SPS",
        "nfeed": nfeed,
        "dual": nfeed == 2,
        "fmin_hz": lowf,
        "fmax_hz": hif,
        "feed_names": feed_names,
        "feeds": feeds,
        "free_text": free_text,
        "note_items": items,
        "sync_ok": bool(np.all(sweeps[:, -1] == _SPX_SYNC)),
    }
    return Spectrogram(times=times, freqs=freqs, power=feeds[feed_names[0]], meta=meta)


def read_spd(path: str | Path) -> Spectrogram:
    """Read a Radio-SkyPipe ``.spd`` strip-chart (time-series) file.

    SPD files hold ``nchannels`` strip-chart traces, all at a single frequency
    (20.1 MHz for Radio JOVE), rather than a spectrum. The returned
    :class:`Spectrogram` therefore uses the channel axis as ``freqs`` (all set to
    20.1 MHz; channel labels in ``meta["channel_labels"]``) and ``power`` has
    shape ``(n_step, n_channel)``. Samples are ``int16`` when the file was saved
    with *Integer Save*, else ``float64``; each record optionally carries an
    8-byte ``float64`` timestamp unless saved with *No Time Stamps*.

    Implemented to the documented layout and round-trip tested; the format shares
    its header/notes structure with :func:`read_sps`, which is validated against
    real bytes.
    """
    raw = Path(path).read_bytes()
    hdr = _spx_header(raw)
    note_len = hdr["note_length"]
    free_text, items = _spx_notes(raw[_SPX_HDR_LEN : _SPX_HDR_LEN + note_len])

    integer_save = any(it.strip() == "Integer Save" for it in items)
    no_timestamps = any(it.strip() == "No Time Stamps" for it in items)
    nfeed = hdr["nchannels"]

    sample_dt = np.dtype("<i2") if integer_save else np.dtype("<f8")
    ts_bytes = 0 if no_timestamps else 8
    bytes_per_step = nfeed * sample_dt.itemsize + ts_bytes
    body = raw[_SPX_HDR_LEN + note_len :]
    nstep = len(body) // bytes_per_step
    if nstep == 0:
        raise ValueError("no complete SPD records found after the header/notes")

    power = np.empty((nstep, nfeed), dtype=float)
    times_jd = np.empty(nstep, dtype=float)
    for k in range(nstep):
        rec = body[k * bytes_per_step : (k + 1) * bytes_per_step]
        if no_timestamps:
            samples = rec
        else:
            times_jd[k] = struct.unpack("<d", rec[:8])[0] + _SPX_EPOCH_JD
            samples = rec[8:]
        power[k] = np.frombuffer(samples[: nfeed * sample_dt.itemsize], dtype=sample_dt)

    if no_timestamps:
        times_jd = np.linspace(hdr["start_jd"], hdr["stop_jd"], nstep, endpoint=False)
    times = (times_jd - times_jd[0]) * 86400.0 if nstep > 1 else np.zeros(1)

    channel_labels = [(_spx_note(items, f"CHL{i}") or f"CH{i}") for i in range(nfeed)]
    freqs = np.full(nfeed, 20.1e6)  # SPD is a single-frequency strip chart

    meta = {
        **hdr,
        "file_type": "SPD",
        "nfeed": nfeed,
        "integer_save": integer_save,
        "no_timestamps": no_timestamps,
        "channel_labels": channel_labels,
        "free_text": free_text,
        "note_items": items,
        "frequency_hz": 20.1e6,
    }
    return Spectrogram(times=times, freqs=freqs, power=power, meta=meta)
