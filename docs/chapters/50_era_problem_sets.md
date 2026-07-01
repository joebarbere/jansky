# Chapter 50 — Essential Radio Astronomy: Worked Problem Sets (2018)

**Notebook:** [50_era_problem_sets.ipynb](../notebooks/50_era_problem_sets.ipynb)

**Level:** Intermediate–Advanced · **Time:** ~90 min

**Prerequisites:** Ch 2 (Physics of Radio Emission), Ch 43 (Synchrotron), Ch 44 (Free-free & HII)  
**Maths Lab:** [Lab 31 — Fourier & Convolution](../notebooks/31_mathslab_fourier_convolution.ipynb)

---

## What this chapter covers

Chapter 50 is the **problem-solving capstone** for the Part I fundamentals. It works through all
twelve problem sets from the 2018 NRAO *Essential Radio Astronomy* course — the practical companion
to the ERA textbook (Condon & Ransom 2016) — solving each problem with prose, LaTeX derivation, and
a code cell that prints the answer in physical units using the same `jansky` helpers used throughout
the course.

**Textbook:** Condon, J. J. & Ransom, S. M. (2016), *Essential Radio Astronomy*, Princeton
University Press.  
ADS: [2016era..book.....C](https://ui.adsabs.harvard.edu/abs/2016era..book.....C)  
Online course & problem sets: <https://science.nrao.edu/opportunities/courses/era>

---

## Learning goals

After working through this chapter you will be able to:

- Apply the Rayleigh–Jeans law, Planck function, and brightness-temperature formalism to real
  sources (Mars, CMB, planetary nebulae, HII regions).
- Derive and use key antenna-theory results: the parabola equal-path property, the Ruze efficiency
  formula, and Fourier similarity and modulation theorems.
- Compute radiometer-equation sensitivities for the GBT and VLA, and reason about configuration
  versus brightness-temperature noise.
- Work through pulsar timing: dispersion measure, Shklovskii secular derivative, and a
  phase-connected TOA fit.
- Reproduce the thermal-wind spectral index (+0.6) for ionised stellar winds and the FIR/radio
  calorimeter model at high redshift.
- Calculate molecular critical densities for CO and HCN using the $\mu^2\nu^3$ scaling.

---

## Problem sets covered

| PS | Topic | Key results |
|----|-------|-------------|
| **1** | Brightness, CMB, Mars | SED slopes; T_b ~213 K; d-independence |
| **2** | Stellar emission, QM, Thomson | Habitable zone; Larmor collapse ~1.6e−11 s; σ_T ~6.65e−25 cm² |
| **3** | Fourier theorems, 2-D FFT | Similarity & modulation; phase carries structure |
| **4** | Parabola, polarisation, dipole | Equal-path property; dipole+λ/4 reflector beam ~120° HPBW |
| **5** | GBT efficiency & sensitivity | Ruze η≈0.60; HPBW ~16″ at 45 GHz |
| **6** | VLA sensitivity, planetary nebula | σ_T scaling with configuration; PN brightness temperature |
| **7** | Interferometry basics | EW fringe rate; VLA integration time |
| **8** | Rigel ionised wind | N₀ ~2e10 cm⁻³; spectral index α = +0.6 |
| **9** | Compact sources, VLBI | T_B limit; VLBI baseline ~1.5e4 km; γ ~1e4 |
| **10** | FIR/radio calorimeter | B_CMB; f_sync at high z; ULIRG B_min ~mG |
| **11** | Pulsar DM, Shklovskii, TOA fit | DM; Shklovskii effect on MSPs; phase-connected timing |
| **12** | HII recombination, molecules | He+/H+ ~0.09; HCN vs CO critical density |

---

## Key references

- Condon, J. J. & Ransom, S. M. (2016), *Essential Radio Astronomy*, Princeton University Press.
  [ADS](https://ui.adsabs.harvard.edu/abs/2016era..book.....C)
- Luisi, M. et al. (2016), ApJ 824, 125 — NGC 7538 recombination lines.
  [DOI](https://doi.org/10.3847/0004-637X/824/2/125)
- Carilli, C. L. & Walter, F. (2013), ARA&A 51, 105 — Molecular gas in high-z galaxies.
  [ADS](https://ui.adsabs.harvard.edu/abs/2013ARA%26A..51..105C)
- Gao, Y. & Solomon, P. M. (2004), ApJ 606, 271 — HCN as a dense-gas tracer.
  [ADS](https://ui.adsabs.harvard.edu/abs/2004ApJ...606..271G)
- Panagia, N. & Felli, M. (1975), A&A 39, 1 — Thermal wind spectrum.
  [ADS](https://ui.adsabs.harvard.edu/abs/1975A%26A....39....1P)
- Wright, A. E. & Barlow, M. J. (1975), MNRAS 170, 41 — Stellar wind spectral index.
  [ADS](https://ui.adsabs.harvard.edu/abs/1975MNRAS.170...41W)
- Miley, G. (1980), ARA&A 18, 165 — Radiative age of synchrotron sources.
  [ADS](https://ui.adsabs.harvard.edu/abs/1980ARA%26A..18..165M)
- Shklovskii, I. S. (1970), Sov. Astron. 13, 562 — Secular period derivative.

---

## Related chapters

- **[Ch 2 — Physics of Radio Emission](../notebooks/02_physics_of_radio_emission.ipynb):** the
  emission mechanisms this chapter exercises.
- **[Ch 43 — Synchrotron Radiation](../notebooks/43_synchrotron_radiation.ipynb):** spectral index,
  Lorentz factor, and synchrotron lifetime (PS9, PS10).
- **[Ch 44 — Free-Free & HII Regions](../notebooks/44_free_free_and_hii.ipynb):** free-free opacity
  and the Rigel wind problem (PS8, PS12).
- **[Lab 31 — Fourier & Convolution](../notebooks/31_mathslab_fourier_convolution.ipynb):** the FT
  theorems behind PS3 and the 2-D FFT image processing.
- **[Ch 13 — Pulsars](../notebooks/13_pulsars.ipynb):** DM, timing, and the P–Ṗ diagram (PS11).
