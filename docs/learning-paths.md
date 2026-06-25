# Learning paths

The course is **41 chapters** plus a six-part **Maths Lab**. You don't have to read them in
order — most chapters need only a couple of earlier ones. This page shows the whole map, the
prerequisites, and a few **themed routes** so you can chart a path that fits your goal and your
hardware.

New here? The quickest start is still **Part I in order** (Chapters 1 → 2 → 3); everything else
branches off that foundation.

## The whole course at a glance

Arrows mean *"builds on"*. Dashed arrows point to the **Maths Lab** appendix that does the worked
maths behind a chapter.

```mermaid
flowchart TD
  %% ---- Part I: Foundations ----
  C1[1 · What is radio astronomy]
  C2[2 · Radio emission]
  C3[3 · Noise & radiometer]
  C43[43 · Synchrotron radiation]
  C44[44 · Free-free & HII regions]
  C1 --> C2 --> C3
  C2 --> C43
  C2 --> C44

  %% ---- Part II: Instrumentation & hardware ----
  C4[4 · Antennas & receivers]
  C5[5 · SDR basics]
  C6[6 · Hydrogen line]
  C26[26 · Meteor scatter]
  C27[27 · VLF & ionosphere]
  C28[28 · GNU Radio]
  C29[29 · No-hardware HI: VIRGO/PICTOR]
  C30[30 · RASDR & Radio-Sky]
  C40[40 · Lightning & sferics]
  C3 --> C4 --> C5 --> C6
  C5 --> C28 --> C30
  C5 --> C26
  C5 --> C27 --> C40
  C6 --> C29

  %% ---- Part III: Interferometry & imaging ----
  C7[7 · Why interferometry]
  C8[8 · Aperture synthesis]
  C9[9 · Deconvolution & CLEAN]
  C41[41 · Practical calibration]
  C17[17 · Coherent interferometry · KrakenSDR]
  C19[19 · EHT & VLBI]
  C25[25 · Intensity interferometry · HBT]
  C37[37 · Polarisation & Faraday rotation]
  C3 --> C7 --> C8 --> C9
  C9 --> C41
  C8 --> C17
  C9 --> C19
  C7 --> C25
  C8 --> C37
  C2 --> C37

  %% ---- Part IV: Real data & research ----
  C10[10 · Open archives]
  C11[11 · HI rotation curve]
  C12[12 · VLA imaging]
  C13[13 · Pulsars]
  C14[14 · Multi-wavelength]
  C16[16 · Data formats]
  C18[18 · Fast radio bursts]
  C47[47 · Long-period radio transients]
  C20[20 · Pulsar timing arrays]
  C21[21 · SETI]
  C22[22 · CMB]
  C23[23 · Solar & Jupiter]
  C24[24 · Molecular & masers]
  C38[38 · Machine learning]
  C39[39 · RFI mitigation]
  C42[42 · Cosmic dawn & EoR]
  C45[45 · Radio galaxies & source counts]
  C46[46 · The art of radio images]
  C15[15 · Capstone]
  C9 --> C10 --> C11
  C10 --> C12
  C10 --> C13
  C10 --> C14
  C13 --> C18
  C13 --> C20
  C13 --> C47
  C18 --> C47
  C18 --> C38
  C3 --> C38
  C3 --> C39
  C3 --> C21
  C2 --> C22
  C2 --> C23
  C2 --> C24
  C6 --> C42
  C22 --> C42
  C10 --> C45
  C43 --> C45
  C11 --> C15
  C12 --> C15
  C12 --> C46
  C13 --> C15
  C14 --> C15

  %% ---- Maths Lab (appendix) ----
  LA([Lab A · Fourier & convolution])
  LB([Lab B · Matched filtering])
  LC([Lab C · Noise & RFI])
  LD([Lab D · Coordinates & time])
  LE([Lab E · Calibration])
  LF([Lab F · Special functions])
  C8 -.-> LA
  C37 -.-> LA
  C18 -.-> LB
  C38 -.-> LB
  C3 -.-> LC
  C39 -.-> LC
  C10 -.-> LD
  C9 -.-> LE
  C4 -.-> LF
```

## Themed routes

Pick the track that matches your goal. Each is an **ordered** list — follow it top to bottom.

### 🛋️ Laptop-only (no hardware, fully offline)

Every chapter runs on synthetic or archival data, so this is the complete course minus the
capture steps. **1 → 2 → 3 → 4 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 18 → 20 → 22 → 24 → 15.**
The Maths Lab (A–F) supports any of these whenever the maths gets dense.

### 📡 I have an RTL-SDR (hands-on hardware)

Build up to capturing real signals, then branch into the amateur projects. **1 → 2 → 3 → 4 → 5 →
6 → 29 → 28 → 30 → 26 → 27.** (Chapters 5–6 are the capture core; 26–30 are the project chapters.)

### 🛰️ Interferometry & imaging

The aperture-synthesis spine and where it leads. **3 → 7 → 8 → 9 → 17 → 19 → 25 → 37 → 12.**
Pair with **Lab A** (Fourier) and **Lab E** (calibration). Chapter 37 (polarisation &
Faraday rotation) reuses the same Fourier machinery in $\lambda^2$ space.

### ⏱️ Pulsars, transients & the nanohertz sky

Time-domain radio astronomy end to end. **3 → 10 → 13 → 18 → 20 → 38.** Pair with **Lab B**
(matched filtering / detection) and **Lab D** (coordinates & time). Chapter 38 pits a learned
classifier against the Lab B matched filter on the FRBs from Chapter 18.

### 🔭 Just the physics & maths

Skip the instruments; concentrate on the science and the derivations. **1 → 2 → 3 → 22 → 24 → 21**,
threaded with the whole **Maths Lab** (A → B → C → D → E → F).

## Maths Lab — which lab serves which chapter

The six appendices are the worked maths behind the course. Reach for one when a chapter leans on a
technique you'd like to see derived from scratch.

| Maths Lab | Worked technique | Most useful for |
|---|---|---|
| **[A · Fourier & convolution](notebooks/31_mathslab_fourier_convolution.ipynb)** | FT pairs, convolution theorem, sampling | Ch 8 (uv-plane), Ch 9 (CLEAN), Ch 37 (RM synthesis), Ch 42 (21 cm power spectrum), Ch 3 |
| **[B · Matched filtering](notebooks/32_mathslab_matched_filtering.ipynb)** | Detection theory, the matched filter | Ch 18 (FRBs), Ch 13 (pulsars), Ch 38 (ML baseline), Ch 3 |
| **[C · Noise & RFI](notebooks/33_mathslab_noise_rfi.ipynb)** | Noise statistics, robust RFI excision | Ch 3 (radiometer), Ch 39 (RFI flagging), Ch 5 (SDR) |
| **[D · Coordinates & time](notebooks/34_mathslab_coordinates_time.ipynb)** | Sky coordinates, time systems | Ch 10 (archives), Ch 11, Ch 13 |
| **[E · Calibration](notebooks/35_mathslab_calibration.ipynb)** | Linear algebra for gain/closure | Ch 41 (practical calibration), Ch 9 (CLEAN), Ch 12 (VLA imaging) |
| **[F · Special functions & beams](notebooks/36_mathslab_special_functions.ipynb)** | Bessel/sinc, beam patterns | Ch 4 (antennas), Ch 8 |

---

Prefer pictures? The **[Visual Tour](visual-tour.md)** walks the same material as diagrams, plots,
photographs, and videos. When you're ready, head to **[Setup](setup.md)** and open Chapter 1.
