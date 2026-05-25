# Reproducibility and Artifacts

## Required Artifacts Per Experiment

```text
experiments/expXXX/
  config.yaml
  result.json
  cv.csv
  oof.csv
  feature_importance.csv
  train.log
  submission.csv
  notes.md
```

## Result JSON

Should include:

- exp_id
- created_at
- model
- features
- target mode
- CV strategy
- fold scores
- CV mean/std
- LB score if submitted
- seed
- data version
- code version or git commit when available

## Data Versioning

Because raw data is immutable, version processed data through filenames or metadata:

```text
train_base_v001.parquet
features_anchor_v001.parquet
folds_group_well_v001.csv
```

Record any schema change in this vault and in experiment notes.
