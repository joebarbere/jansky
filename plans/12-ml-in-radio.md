# Plan 12 — Machine learning in radio astronomy chapter 📋 Proposed

> Flagged by **research-currency (#4)**. Scope: medium.

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
