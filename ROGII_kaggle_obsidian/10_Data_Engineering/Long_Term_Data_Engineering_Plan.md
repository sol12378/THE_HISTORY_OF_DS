# Long-Term Data Engineering Plan

## Purpose

This plan freezes the data engineering architecture before serious modeling begins. The goal is to avoid mid-competition schema churn and make every experiment reproducible.

## Architecture Summary

Use four stable layers:

```text
raw
  immutable Kaggle files

interim
  parsed normalized tables

processed
  versioned base tables and feature tables

experiment
  exact matrices, OOF, submissions, model artifacts
```

## Stable Artifacts

The following artifacts should be treated as stable contracts:

```text
data/processed/train_base_v001.parquet
data/processed/test_base_v001.parquet
data/processed/typewell_train_base_v001.parquet
data/processed/typewell_test_base_v001.parquet
data/folds/folds_group_well_v001.csv
```

Feature artifacts should be independently versioned:

```text
data/processed/features_anchor_v001.parquet
data/processed/features_trajectory_v001.parquet
data/processed/features_gr_v001.parquet
data/processed/features_typewell_basic_v001.parquet
data/processed/features_alignment_v001.parquet
```

## What Should Be Frozen

Freeze:

- canonical identifiers
- base schema
- target row definition
- fold file format
- submission mapping
- feature family boundaries
- artifact naming conventions
- leakage policy

Do not freeze:

- model type
- feature versions
- target transform choice
- blending strategy
- experiment configs

## Canonical Identifiers

Every row-level table must carry:

```text
split
well_id
row_idx
```

Test target rows also carry:

```text
id = f"{well_id}_{row_idx}"
```

These identifiers are the backbone for joins, OOF analysis, error slicing, and submission generation.

## Base Tables vs Feature Tables

Base tables should contain only stable, universally useful columns:

- raw observable fields
- row identity
- Prediction Start metadata
- anchor metadata
- target and mask columns

Feature tables should contain derived experiment-oriented columns:

- rolling GR
- trajectory curvature
- typewell joins
- alignment scores
- candidate TVT estimates

This separation reduces the cost of changing feature logic while preserving stable experiment inputs.

## Fold Strategy

The default fold contract:

```text
data/folds/folds_group_well_v001.csv
columns: split, well_id, fold
```

For row-level training, join folds by `well_id`.

Additional fold files can be created:

```text
folds_group_typewell_v001.csv
folds_spatial_cluster_v001.csv
folds_adversarial_public_v001.csv
```

Never overwrite a fold file after experiments depend on it.

## Quality Gates

Every ETL run should fail fast if:

- raw file counts do not match expectations
- sample submission IDs do not map to test target rows
- `TVT_input` missing section is not a contiguous tail
- row keys are duplicated
- train/test feature columns diverge
- any target-aware feature is generated before fold isolation
- any experiment tries to use analysis-only columns by default

## Recommended Implementation Modules

```text
src/rogii/data/raw_inventory.py
src/rogii/data/build_base.py
src/rogii/data/build_typewell.py
src/rogii/data/validate_schema.py
src/rogii/data/make_folds.py
src/rogii/features/build_anchor.py
src/rogii/features/build_trajectory.py
src/rogii/features/build_gr.py
src/rogii/features/build_typewell.py
src/rogii/features/build_alignment.py
src/rogii/training/build_matrix.py
```

## Recommended Scripts

```text
scripts/build_base_tables.py
scripts/build_feature_table.py
scripts/make_folds.py
scripts/validate_data.py
scripts/build_matrix.py
scripts/run_exp.py
```

## Public Repository Safety

Do not commit:

- `.env`
- `.kaggle/`
- raw Kaggle data
- processed parquet files
- OOF files
- model artifacts
- submissions
- Obsidian workspace files

Commit:

- ETL code
- schema docs
- small templates
- configs
- empty `.gitkeep` directories
- Obsidian Markdown notes

## Migration Policy

If a design change is required:

1. create a new artifact version
2. leave old artifacts untouched
3. document the reason in `Decision_Log.md`
4. update relevant schema docs
5. list impacted experiments
6. do not compare CV across incompatible data versions without noting it

## Final Principle

The base data layer should be boring, stable, and traceable. Innovation belongs in feature versions and experiments, not in silent changes to row identity, masks, folds, or target definitions.
