# Plan 12 — Machine learning in radio astronomy chapter ✅ Delivered

> Flagged by **research-currency (#4)**. Scope: medium.
>
> **Delivered:**
> - **New chapter** `notebooks/38_machine_learning.ipynb` (Part IV) — frames the ML task types on
>   radio data, then a fully-offline worked example: classify dispersed FRB pulses vs RFI/noise
>   confusers (pure noise, narrowband RFI, zero-DM broadband) in synthetic dynamic spectra built
>   from `jansky.transients.disperse_pulse`. Trains a scikit-learn MLP and compares it to the
>   classical **matched-filter / DM-search baseline** (`dedisperse` + `boxcar_snr`): the learned
>   model (test AUC 1.00) beats the classical detector (AUC 0.858) specifically on the zero-DM
>   confuser it cannot distinguish on DM-search score alone. Confusion matrices + ROC; honest
>   caveats (simulator-as-ground-truth, data hunger, domain shift, why matched filtering is still
>   the production workhorse). Cites Eatough et al. (2009), Zackay & Ofek (2017), Agarwal et al.
>   (2020, FETCH). Authored by `notebook-author`; reviewed by `science-reviewer`.
> - **Dependency** — new `ml` optional extra (`scikit-learn`) in `pyproject.toml`; an optional
>   torch CNN is guarded behind `try/except` and stays reader-installed (the base path runs on
>   sklearn only). `--extra ml` added to the weekly `notebooks.yml` run.
> - **Docs** — glossary (CNN, confusion matrix, machine learning, ROC/AUC, train/validation/test
>   split), nav entry, and `docs/learning-paths.md` integration (map node + pulsars-&-transients
>   route + Maths-Lab B service row).
>
> Verification: 107 unit tests pass, nbmake on Ch 38 passes (~20 s on the `ml` extra), ruff +
> mypy + mkdocs --strict green.

## Context

The course has no coverage of machine learning, now standard practice in the field — FRB/RFI
classification, source-finding, RM/DM estimation, and real-time deep-learning detection pipelines
(multiple 2025 papers; foundation models emerging). It slots naturally onto the course's existing
FRB (Ch 18) and RFI (Maths Lab C) scaffolding rather than starting from scratch.

## Deliverables

- **New chapter** (Part IV), e.g. `notebooks/38_machine_learning.ipynb`:
  - frame the tasks (classification, detection, regression) on radio data;
  - a worked, small **CNN that separates FRBs from RFI on dynamic spectra**, reusing
    `jansky.transients.disperse_pulse` (FRB class) and `jansky.seti`/RFI sims (RFI/noise class) to
    generate a labelled training set entirely offline;
  - train/validate, show a confusion matrix and ROC, and connect to the matched-filter baseline
    from Maths Lab B (classical vs learned detectors);
  - honest caveats: data hunger, label bias, generalisation, why classical methods still matter.
- **Dependency** — a `ml` optional extra (`scikit-learn`, and a lightweight NN via `torch` *or*
  keep it `scikit-learn`/`numpy`-only to avoid heavy deps — prefer the latter for the base course,
  with torch behind the extra). Guard imports so the chapter degrades to the sklearn path offline.
- Glossary entries (CNN, training/validation, confusion matrix, ROC in this context); nav entry.

## Verification

- Runs offline on simulated labelled data; the classifier beats chance with a sensible confusion
  matrix; `nbmake` + `mkdocs --strict` green. No heavy dep required for the base path.
