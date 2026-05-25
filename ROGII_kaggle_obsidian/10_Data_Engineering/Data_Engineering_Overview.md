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

## Freeze Decisions

These decisions should remain stable throughout the competition unless there is a documented migration:

1. `well_id` and `row_idx` are the canonical row keys.
2. Model training rows are horizontal-well rows where `is_target=True`.
3. Local evaluation uses `TVT` RMSE on `is_target=True` rows only.
4. Folds are generated once and versioned in `data/folds/`.
5. Base tables are feature-light and stable; experiment-specific features live in feature tables or feature functions.
6. Every processed table has a version, creation timestamp, source raw-data fingerprint, and schema contract.
7. Feature families are additive and can be ablated independently.
8. Raw train-only geological marker columns are analysis-only unless an experiment explicitly documents how test parity is achieved.

## Recommended Data Architecture

Use a layered "bronze / silver / gold" mental model:

```text
Bronze:
  data/raw/
  Exact Kaggle files. Immutable.

Silver:
  data/interim/
  Parsed normalized tables with stable row IDs, source paths, and basic validation.

Gold:
  data/processed/
  Model-ready base tables, fold files, and feature tables.
```

The gold layer should be the only default input for experiments.

## Table Granularity

Use three canonical granularities:

```text
well-row:
  one row per horizontal well point
  key = split, well_id, row_idx

typewell-row:
  one row per typewell TVT point
  key = split, well_id, typewell_row_idx

well-level:
  one row per well
  key = split, well_id
```

Do not mix these granularities without an explicit join rule.

## Metadata Requirements

Every generated dataset should have a sidecar metadata file:

```text
data/processed/train_base_v001.parquet
data/processed/train_base_v001.meta.json
```

Metadata should include:

- dataset name
- version
- created_at
- source file counts
- source raw fingerprint
- row counts
- column list
- null summary
- script name
- git commit if available
- leakage assumptions
- validation checks passed

## Change Policy

If a base schema must change:

1. Create a new version such as `train_base_v002.parquet`.
2. Keep old versions until dependent experiments are archived.
3. Write the migration reason in `Decision_Log.md`.
4. Update `Schema_and_Contracts.md`.
5. Never silently overwrite a base table used by previous experiments.
