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
