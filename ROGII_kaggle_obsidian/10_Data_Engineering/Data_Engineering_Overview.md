# Data Engineering Overview

## Goal

Build a repeatable, auditable data pipeline from raw Kaggle files to model-ready feature tables.

The pipeline must make it easy to:

- reproduce experiments
- avoid leakage
- generate consistent train/test features
- create reliable CV folds
- save OOF and submission artifacts
- inspect well-level failures

## Core Principle

Treat each well as a sequence first, and as tabular rows second.

Raw files are organized by well. Models will often train on rows, but feature construction must preserve well-level context:

- row order
- Prediction Start position
- pre-PS anchor state
- rolling windows within a well
- typewell reference curve

## Data Layers

Recommended layers:

```text
data/raw/
  Immutable Kaggle files.

data/interim/
  Parsed and lightly normalized per-well tables.

data/processed/
  Model-ready train/test base tables and feature tables.

data/folds/
  Fold assignment files.

outputs/
  Models, OOF, predictions, plots, diagnostics.

experiments/
  Per-experiment frozen configs and results.
```

## Pipeline Stages

1. Raw inventory
2. Schema validation
3. Horizontal well parsing
4. Typewell parsing
5. Prediction Start detection
6. Base table construction
7. Fold generation
8. Feature generation
9. Model dataset export
10. OOF/submission artifact validation

## Non-Negotiables

- Never modify `data/raw/`.
- Never use future `TVT` when constructing test-time features.
- Never row-random split.
- Always save row identifiers: `well_id`, `row_idx`, and submission `id` where applicable.
- Always keep enough metadata to trace any prediction back to a source CSV row.
