"""Generate the Seaborn figures used in the course's Visual Tour.

Run from the repo root with::

    uv run python scripts/generate_figures.py

Every figure is built from the `jansky` helper package plus NumPy/SciPy, so the
plots stay consistent with the maths taught in the chapters. Output PNGs are
written to ``docs/assets/figures/`` and committed so the docs site renders
without a build-time compute step. Re-run this whenever the helpers change.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: no display needed

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit

from jansky import interferometry, signals, units

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# A consistent, legible Seaborn theme for the whole gallery.
sns.set_theme(context="notebook", style="whitegrid", palette="viridis")
ACCENT = "#7e57c2"  # matches the site's deep-purple accent


def _save(fig: plt.Figure, name: str) -> None:
    path = OUT / name
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT.parents[1])}")


def radiometer_heatmap() -> None:
    """Seaborn heatmap of radiometer sensitivity over bandwidth x integration time."""
    bandwidths = np.array([1e4, 1e5, 1e6, 1e7, 1e8])  # Hz
    times = np.array([0.1, 1, 10, 60, 600, 3600])  # s
    grid = np.array(
        [[signals.radiometer_sensitivity(50.0, b, t) for b in bandwidths] for t in times]
    )
    df = pd.DataFrame(
        grid,
        index=[f"{t:g}" for t in times],
        columns=["10 kHz", "100 kHz", "1 MHz", "10 MHz", "100 MHz"],
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        df,
        ax=ax,
        cmap="rocket_r",
        norm=matplotlib.colors.LogNorm(),
        annot=True,
        fmt=".2g",
        linewidths=0.5,
        cbar_kws={"label": r"$\Delta T$  (K)"},
    )
    ax.set_xlabel("Bandwidth  $B$")
    ax.set_ylabel("Integration time  $\\tau$  (s)")
    ax.set_title(
        "Radiometer sensitivity  $\\Delta T = T_{sys}/\\sqrt{B\\,\\tau}$  ($T_{sys}=50$ K)"
    )
    _save(fig, "radiometer_heatmap.png")


def signal_emerges() -> None:
    """Many noise integrations converging on a faint signal (Seaborn lineplot + CI band)."""
    true_signal = 0.05
    rows = []
    for trial in range(40):
        res = signals.integrate_noise(
            t_sys=30.0,
            bandwidth=1e6,
            total_time=100.0,
            signal=true_signal,
            n_samples=300,
            seed=trial,
        )
        for t, est in zip(res.times, res.estimate, strict=True):
            rows.append({"time": t, "estimate": est})
    df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=df, x="time", y="estimate", errorbar=("ci", 95), ax=ax, color=ACCENT)
    ax.axhline(true_signal, ls="--", color="crimson", label=f"true signal = {true_signal} K")
    ax.set_xlabel("Integration time  (s)")
    ax.set_ylabel("Running estimate  (K)")
    ax.set_title("Watch a signal climb out of the noise (40 trials, 95% band)")
    ax.legend()
    _save(fig, "signal_emerges.png")


def spectral_index() -> None:
    """Two-component radio spectrum on log-log axes with a recovered power-law fit."""
    freq = np.linspace(0.1, 10.0, 60)
    flux = signals.synthetic_spectrum(
        freq, thermal_amp=0.5, nonthermal_amp=10.0, spectral_index=-0.8, noise=0.15, seed=3
    )

    def model(nu, amp, alpha):
        return signals.power_law(nu, amp, alpha)

    nonthermal = flux - 0.5
    mask = nonthermal > 0
    popt, _ = curve_fit(model, freq[mask], nonthermal[mask], p0=[10.0, -1.0])

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=freq, y=flux, ax=ax, color=ACCENT, s=40, label="synthetic data")
    ax.plot(
        freq,
        0.5 + model(freq, *popt),
        color="crimson",
        label=rf"fit: $\alpha = {popt[1]:.2f}$ (true $-0.8$)",
    )
    ax.axhline(0.5, ls=":", color="gray", label="thermal floor")
    ax.set(xscale="log", yscale="log")
    ax.set_xlabel("Frequency  (GHz)")
    ax.set_ylabel("Flux density  (Jy)")
    ax.set_title("Spectral index: separating thermal from synchrotron emission")
    ax.legend()
    _save(fig, "spectral_index.png")


def beam_patterns() -> None:
    """Airy vs Gaussian beam power patterns in dB (Seaborn lineplot)."""
    theta = np.linspace(-np.radians(3), np.radians(3), 1200)
    diameter, wavelength = 25.0, 0.21  # 25 m dish at 21 cm
    airy = signals.airy_beam(theta, diameter, wavelength)
    fwhm = np.radians(0.6)
    gauss = signals.gaussian_beam(theta, fwhm)
    deg = np.degrees(theta)
    df = pd.concat(
        [
            pd.DataFrame(
                {
                    "angle": deg,
                    "power_dB": units.to_decibels(np.clip(airy, 1e-6, None)),
                    "pattern": "Airy (uniform dish)",
                }
            ),
            pd.DataFrame(
                {
                    "angle": deg,
                    "power_dB": units.to_decibels(np.clip(gauss, 1e-6, None)),
                    "pattern": "Gaussian (tapered)",
                }
            ),
        ]
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=df, x="angle", y="power_dB", hue="pattern", ax=ax)
    ax.set_ylim(-50, 2)
    ax.set_xlabel("Angle from boresight  (degrees)")
    ax.set_ylabel("Relative power  (dB)")
    ax.set_title("Antenna beam patterns: the main lobe and its sidelobes")
    _save(fig, "beam_patterns.png")


def brightness_temperature() -> None:
    """Heatmap of flux density (Jy) over brightness temperature x frequency."""
    temps = np.array([10, 30, 100, 300, 1000, 3000, 10000])  # K
    freqs = np.array([0.3, 0.6, 1.4, 5, 15, 45]) * u.GHz
    omega = 1e-6 * u.sr
    grid = np.array(
        [
            [units.brightness_temperature_to_flux(t * u.K, f, omega).to_value(u.Jy) for f in freqs]
            for t in temps
        ]
    )
    df = pd.DataFrame(
        grid, index=[f"{t:g}" for t in temps], columns=[f"{f.to_value(u.GHz):g}" for f in freqs]
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        df,
        ax=ax,
        cmap="mako",
        norm=matplotlib.colors.LogNorm(),
        annot=True,
        fmt=".1g",
        linewidths=0.5,
        cbar_kws={"label": "Flux density (Jy)"},
    )
    ax.set_xlabel("Frequency  (GHz)")
    ax.set_ylabel("Brightness temperature  (K)")
    ax.set_title(r"Rayleigh--Jeans: flux density over a $10^{-6}$ sr source")
    _save(fig, "brightness_temperature.png")


def uv_coverage() -> None:
    """Snapshot vs Earth-rotation uv-coverage for a toy array (Seaborn scatter with hue)."""
    rng = np.random.default_rng(7)
    antennas = rng.uniform(-60, 60, size=(8, 2))
    snap = interferometry.uv_coverage(antennas)
    track = interferometry.uv_coverage(antennas, hour_angles=np.linspace(-np.pi / 3, np.pi / 3, 80))
    df = pd.concat(
        [
            pd.DataFrame({"u": track[:, 0], "v": track[:, 1], "kind": "12 h Earth rotation"}),
            pd.DataFrame({"u": snap[:, 0], "v": snap[:, 1], "kind": "snapshot"}),
        ]
    )
    fig, ax = plt.subplots(figsize=(6.5, 6))
    sns.scatterplot(
        data=df,
        x="u",
        y="v",
        hue="kind",
        s=10,
        ax=ax,
        palette={"snapshot": "crimson", "12 h Earth rotation": ACCENT},
    )
    ax.set_aspect("equal")
    ax.set_xlabel("u  (m)")
    ax.set_ylabel("v  (m)")
    ax.set_title("Filling the uv-plane: Earth-rotation synthesis")
    _save(fig, "uv_coverage.png")


def pulsar_ppdot() -> None:
    """Illustrative pulsar P-Pdot diagram (Seaborn scatter with characteristic-age lines)."""
    rng = np.random.default_rng(42)
    # Two illustrative populations: normal and millisecond pulsars.
    p_normal = 10 ** rng.normal(-0.2, 0.35, 250)  # ~0.1-3 s
    pdot_normal = 10 ** rng.normal(-15, 1.0, 250)
    p_ms = 10 ** rng.normal(-2.4, 0.18, 40)  # ~3-6 ms
    pdot_ms = 10 ** rng.normal(-20, 0.6, 40)
    df = pd.DataFrame(
        {
            "P": np.concatenate([p_normal, p_ms]),
            "Pdot": np.concatenate([pdot_normal, pdot_ms]),
            "type": ["normal"] * len(p_normal) + ["millisecond"] * len(p_ms),
        }
    )
    fig, ax = plt.subplots(figsize=(7.5, 6))
    sns.scatterplot(
        data=df,
        x="P",
        y="Pdot",
        hue="type",
        style="type",
        ax=ax,
        palette={"normal": ACCENT, "millisecond": "crimson"},
        s=28,
        alpha=0.8,
    )
    p_line = np.array([1e-3, 20])
    for age_yr, label in [(1e3, "1 kyr"), (1e6, "1 Myr"), (1e9, "1 Gyr")]:
        # Characteristic age tau = P / (2 Pdot) -> Pdot = P / (2 tau).
        age_s = age_yr * 3.156e7
        ax.plot(p_line, p_line / (2 * age_s), ls="--", color="gray", lw=0.8)
        ax.text(
            p_line[-1],
            p_line[-1] / (2 * age_s),
            f"  {label}",
            color="gray",
            va="center",
            fontsize=8,
        )
    ax.set(xscale="log", yscale="log")
    ax.set_xlabel("Spin period  $P$  (s)")
    ax.set_ylabel("Period derivative  $\\dot{P}$  (s/s)")
    ax.set_title("The pulsar $P$–$\\dot{P}$ diagram (illustrative)")
    _save(fig, "pulsar_ppdot.png")


def resolution_infographic() -> None:
    """Angular resolution (1.22 lambda/D) across instruments -- an infographic bar chart."""
    rows = [
        ("Human eye\n(optical)", 5e-3, 0.55e-6),
        ("Backyard 1.2 m dish\n@ 1.4 GHz", 1.2, 0.21),
        ("Parkes 64 m\n@ 1.4 GHz", 64, 0.21),
        ("VLA (A-config 36 km)\n@ 1.4 GHz", 36e3, 0.21),
        ("VLBI / EHT (Earth)\n@ 230 GHz", 1.0e7, 1.3e-3),
    ]
    data = []
    for name, d, lam in rows:
        theta_rad = 1.22 * lam / d
        arcsec = np.degrees(theta_rad) * 3600
        data.append({"instrument": name, "resolution_arcsec": arcsec})
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(8.5, 5))
    sns.barplot(
        data=df,
        y="instrument",
        x="resolution_arcsec",
        ax=ax,
        hue="instrument",
        palette="viridis",
        legend=False,
    )
    ax.set_xscale("log")
    ax.set_xlabel("Angular resolution  $1.22\\,\\lambda/D$  (arcsec, smaller = sharper)")
    ax.set_ylabel("")
    ax.set_title("Why we build big arrays: angular resolution compared")
    for i, v in enumerate(df["resolution_arcsec"]):
        label = f"{v:.2g}″" if v >= 0.01 else f"{v * 1000:.2g} mas"
        ax.text(v, i, f"  {label}", va="center", fontsize=9)
    _save(fig, "resolution_infographic.png")


def main() -> None:
    radiometer_heatmap()
    signal_emerges()
    spectral_index()
    beam_patterns()
    brightness_temperature()
    uv_coverage()
    pulsar_ppdot()
    resolution_infographic()
    print(f"\nAll figures written to {OUT}")


if __name__ == "__main__":
    main()
