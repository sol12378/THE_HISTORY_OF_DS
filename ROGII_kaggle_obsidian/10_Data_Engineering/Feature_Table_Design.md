# Feature Table Design

## Design

Use additive feature families with stable keys:

```text
key: split, well_id, row_idx
```

Each feature family should be independently buildable:

```text
anchor_features
trajectory_features
gr_features
typewell_features
alignment_features
```

This enables ablation:

```text
basic
basic + anchor
basic + anchor + trajectory
basic + anchor + trajectory + GR
basic + anchor + trajectory + GR + typewell
```

## Anchor Features

Computed per well using only rows before Prediction Start:

- last known TVT
- last known MD/X/Y/Z
- delta from PS
- local TVT slope before PS
- local TVT curvature before PS

## Trajectory Features

Computed from current and neighboring positions:

- local direction
- displacement from PS
- horizontal distance
- dZ/dMD
- azimuth proxy
- inclination proxy
- curvature

## GR Features

Computed within a well:

- raw GR
- missing flag
- interpolated value
- rolling mean/std
- rolling diff/slope
- GR percentile
- missing run length

## Typewell Features

Computed from the paired typewell:

- GR stats over full typewell
- GR at last known TVT
- GR at baseline predicted TVT
- local rolling stats around candidate TVT

## Alignment Features

Computed by comparing horizontal GR windows to typewell GR windows:

- best correlation score
- best matching TVT
- shift from baseline TVT
- DTW-like distance
- confidence from GR coverage

## Storage

Prefer parquet:

- faster load
- preserves dtypes
- compact
- stable for repeated experiments

## Feature Registry

Maintain a lightweight feature registry:

```text
data/processed/feature_registry_v001.json
```

For each feature family, record:

- feature table path
- version
- keys
- columns
- dependencies
- leakage assumptions
- train/test availability
- generating script/function

## Feature Stability Rule

Once a feature table is used by an experiment, do not mutate it in place.

Instead:

```text
features_gr_v001.parquet
features_gr_v002.parquet
```

Experiments should reference exact feature versions in config.

## Matrix Assembly

Training matrices should be assembled from:

```text
base table
+ selected feature family versions
+ fold file
+ target transform
```

The resulting matrix can be cached as:

```text
data/cache/matrix_exp003_lgb_anchor_trajectory.parquet
```

Cache files are disposable. Base tables and versioned feature tables are not.

## Target Transform Contract

Supported target modes should be explicit:

```text
direct:
  y = TVT

delta_from_anchor:
  y = TVT - last_known_TVT

slope_from_anchor:
  y = (TVT - last_known_TVT) / max(delta_MD_from_PS, eps)
```

Evaluation always converts back to absolute `TVT` and computes RMSE.

## Train/Test Feature Parity

Before training, assert:

```text
set(train_features) == set(test_features)
```

Exceptions must be documented and handled in code, not silently ignored.
