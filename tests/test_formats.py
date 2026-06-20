"""Tests for jansky.formats -- data formats and the RSS network protocol.

All tests run offline with no optional dependencies: GUPPI raw and SigMF are
written and read back, and the RSS client is exercised against the in-process
mock server.
"""

from __future__ import annotations

import numpy as np

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


def test_deferred_readers_raise():
    import pytest

    with pytest.raises(NotImplementedError):
        formats.read_sps("nope.sps")
    with pytest.raises(NotImplementedError):
        formats.read_spd("nope.spd")
