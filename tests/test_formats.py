"""Tests for jansky.formats -- data formats and the RSS network protocol.

All tests run offline with no optional dependencies: GUPPI raw and SigMF are
written and read back, and the RSS client is exercised against the in-process
mock server.
"""

from __future__ import annotations

import struct

import numpy as np
import pytest

from jansky import formats


def test_spectrogram_roundtrip_npz(tmp_path):
    rng = np.random.default_rng(0)
    spec = formats.Spectrogram(
        times=np.arange(5.0),
        freqs=np.linspace(20e6, 21e6, 8),
        power=rng.normal(size=(5, 8)),
        meta={"source": "test", "telescope": "jansky"},
    )
    path = formats.save_spectrogram(tmp_path / "s.npz", spec)
    back = formats.load_spectrogram(path)
    assert np.allclose(back.power, spec.power)
    assert back.meta["source"] == "test"


def test_guppi_roundtrip(tmp_path):
    rng = np.random.default_rng(1)
    nchan, ntime, npol = 4, 16, 2
    volts = rng.integers(-20, 20, (nchan, ntime, npol)) + 1j * rng.integers(
        -20, 20, (nchan, ntime, npol)
    )
    path = formats.write_guppi(
        tmp_path / "x.0000.raw",
        volts,
        header={"OBSFREQ": 1420.0, "TBIN": 1e-6, "SRC_NAME": "TESTSRC"},
    )

    header = formats.read_guppi_header(path)
    assert header["OBSNCHAN"] == nchan
    assert header["NPOL"] == npol
    assert header["NBITS"] == 8
    assert header["SRC_NAME"] == "TESTSRC"
    assert header["OBSFREQ"] == 1420.0

    blocks = list(formats.iter_guppi_blocks(path))
    assert len(blocks) == 1
    _, recovered = blocks[0]
    assert recovered.shape == (nchan, ntime, npol)
    # int8 round-trip is exact for these small integer voltages.
    assert np.allclose(recovered.real, volts.real)
    assert np.allclose(recovered.imag, volts.imag)


def test_sigmf_roundtrip(tmp_path):
    rng = np.random.default_rng(2)
    samples = (rng.normal(size=1000) + 1j * rng.normal(size=1000)).astype("complex64")
    formats.write_sigmf(
        tmp_path / "rec",
        samples,
        sample_rate=2.4e6,
        center_freq=1.42e9,
    )
    back, meta = formats.read_sigmf(tmp_path / "rec")
    assert meta["global"]["core:datatype"] == "cf32_le"
    assert meta["global"]["core:sample_rate"] == 2.4e6
    assert meta["captures"][0]["core:frequency"] == 1.42e9
    assert np.allclose(back, samples)


def test_rss_handshake_and_sweep_encoding():
    hs = formats.rss_handshake(21_000_000, 5_000_000, 500)
    assert hs == b"F 21000000|S 5000000|O 0|C 500|"
    # 12-bit clip + LoHi + high-channel-first + terminator
    sweep = formats.encode_rss_sweep(np.array([0, 4095, 9000]))
    assert sweep.endswith(formats.RSS_TERMINATOR)
    decoded = formats.decode_rss_sweep(sweep)
    assert list(decoded) == [0, 4095, 4095]  # 9000 clipped to 12-bit max


def test_rss_handshake_rejects_bad_channel_count():
    import pytest

    with pytest.raises(ValueError):
        formats.rss_handshake(21_000_000, 5_000_000, 50)  # < 100


def test_rss_client_streams_to_mock_server():
    server = formats.MockRSSServer()
    server.start()
    n_chan = 256
    rng = np.random.default_rng(3)
    sent = [rng.integers(0, 4096, n_chan) for _ in range(4)]
    with formats.RSSClient(
        center_hz=21_000_000,
        bandwidth_hz=5_000_000,
        n_channels=n_chan,
        host=server.host,
        port=server.port,
    ) as rss:
        for sweep in sent:
            rss.send_sweep(sweep)
    server.join()

    assert server.config["F"] == 21_000_000
    assert server.config["C"] == n_chan
    assert len(server.sweeps) == len(sent)
    for original, received in zip(sent, server.sweeps, strict=True):
        assert np.array_equal(received, original)


_HDR_FMT = "<10s6d1h10s20s20s40s1h1i"
_EPOCH = 2415018.5


def _spx_header(nchannels, note_length, *, start_jd, stop_jd, author=b"Tester", obsname=b"TestObs"):
    return struct.pack(
        _HDR_FMT,
        b"00002080",  # software id (10s)
        start_jd - _EPOCH,
        stop_jd - _EPOCH,
        29.0,  # lat
        -82.0,  # lon
        100.0,  # chartmax
        0.0,  # chartmin
        -5,  # timezone
        b"src",
        author,
        obsname,
        b"Somewhere, FL",
        nchannels,
        note_length,
    )


def _make_notes(items: list[bytes], free=b"") -> bytes:
    return free + b"*[[*" + b"\xff".join(items) + b"*]]*"


def _make_sps(tmp_path, nfreq=4, nfeed=2, nstep=3, lowf=16_000_000, hif=32_000_000):
    items = [
        f"SWEEPS{nstep}".encode(),
        f"LOWF{lowf}".encode(),
        f"HIF{hif}".encode(),
        f"STEPS{nfreq}".encode(),
        b"DUALSPECFILE" + (b"True" if nfeed == 2 else b"False"),
    ]
    if nfeed == 2:
        items += [b"BANNER0 RCP feed", b"BANNER1 LCP feed"]
    notes = _make_notes(items)
    header = _spx_header(nfreq, len(notes), start_jd=2_457_732.5, stop_jd=2_457_732.6)
    # Sweep samples laid out (channel, feed): value encodes 100*feed + channel.
    rows = []
    for _ in range(nstep):
        flat = [100 * f + c for c in range(nfreq) for f in range(nfeed)]
        flat.append(0xFEFE)  # trailing sync delimiter
        rows.append(struct.pack(f">{nfreq * nfeed + 1}H", *flat))
    path = tmp_path / "synth.sps"
    path.write_bytes(header + notes + b"".join(rows))
    return path


def test_read_sps_roundtrip_dual_feed(tmp_path):
    sg = formats.read_sps(_make_sps(tmp_path, nfreq=4, nfeed=2, nstep=3))
    assert sg.power.shape == (3, 4)
    assert sg.meta["nfeed"] == 2 and sg.meta["dual"]
    assert sg.meta["feed_names"] == ["RR", "LL"]
    assert sg.meta["sync_ok"] is True
    # freqs run from the high edge (32 MHz) to the low edge (16 MHz).
    assert np.isclose(sg.freqs[0], 32e6) and np.isclose(sg.freqs[-1], 16e6)
    # Column ordering (channel, feed): feed 0 = channel value, feed 1 = 100 + channel.
    assert np.array_equal(sg.meta["feeds"]["RR"][0], [0, 1, 2, 3])
    assert np.array_equal(sg.meta["feeds"]["LL"][0], [100, 101, 102, 103])


def test_read_sps_single_feed(tmp_path):
    sg = formats.read_sps(_make_sps(tmp_path, nfreq=8, nfeed=1, nstep=2))
    assert sg.power.shape == (2, 8)
    assert sg.meta["nfeed"] == 1 and sg.meta["feed_names"] == ["S"]


def _make_spd(tmp_path, nfeed=2, nstep=3, integer_save=True, no_timestamps=False):
    items = [b"CHL0Ch-A", b"CHL1Ch-B"][:nfeed]
    if integer_save:
        items.append(b"Integer Save")
    if no_timestamps:
        items.append(b"No Time Stamps")
    notes = _make_notes(items)
    header = _spx_header(nfeed, len(notes), start_jd=2_457_000.5, stop_jd=2_457_000.6)
    sample_fmt = f"<{nfeed}h" if integer_save else f"<{nfeed}d"
    records = []
    for k in range(nstep):
        rec = b""
        if not no_timestamps:
            rec += struct.pack("<d", (2_457_000.5 - _EPOCH) + k * 0.01)
        vals = [10 * k + i for i in range(nfeed)]
        rec += struct.pack(sample_fmt, *vals)
        records.append(rec)
    path = tmp_path / "synth.spd"
    path.write_bytes(header + notes + b"".join(records))
    return path


def test_read_spd_roundtrip_integer_timestamps(tmp_path):
    sg = formats.read_spd(_make_spd(tmp_path, nfeed=2, nstep=3, integer_save=True))
    assert sg.power.shape == (3, 2)
    assert sg.meta["integer_save"] and not sg.meta["no_timestamps"]
    assert sg.meta["channel_labels"] == ["Ch-A", "Ch-B"]
    assert np.allclose(sg.freqs, 20.1e6)
    assert np.array_equal(sg.power[1], [10, 11])  # step 1 samples


def test_read_spd_float_no_timestamps(tmp_path):
    sg = formats.read_spd(
        _make_spd(tmp_path, nfeed=3, nstep=4, integer_save=False, no_timestamps=True)
    )
    assert sg.power.shape == (4, 3)
    assert not sg.meta["integer_save"] and sg.meta["no_timestamps"]
    assert np.array_equal(sg.power[2], [20, 21, 22])


def _online() -> bool:
    import urllib.request

    try:
        urllib.request.urlopen("https://maser.obspm.fr", timeout=5)
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _online(), reason="no network")
def test_read_sps_real_radiojove_sample(tmp_path, monkeypatch):
    """read_sps parses the real Radio JOVE recording (network-gated)."""
    from jansky import data

    monkeypatch.setenv("JANSKY_DATA_DIR", str(tmp_path))
    # The host may answer the reachability probe yet still time out on the data file
    # itself; a network-gated test should skip on that, not fail CI.
    try:
        sps_path = data.fetch("radiojove-sps")
    except RuntimeError as exc:
        pytest.skip(f"radiojove-sps download unavailable: {exc}")
    sg = formats.read_sps(sps_path)
    assert sg.meta["author"] == "Dave Typinski"
    assert sg.meta["nchannels"] == 300 and sg.meta["dual"]
    assert np.isclose(sg.meta["fmax_hz"], 32e6) and np.isclose(sg.meta["fmin_hz"], 16e6)
    assert sg.meta["sync_ok"] is True
    # nstep recovered from the byte layout matches the SWEEPS metadata note.
    assert sg.power.shape[0] == int(formats._spx_note(sg.meta["note_items"], "SWEEPS"))
