# Data Quality Checks

## Raw Inventory Checks

- train horizontal count equals train typewell count
- every train well has a PNG
- test horizontal count equals test typewell count
- sample submission IDs map to test wells and row indices

## Horizontal Checks

- required columns exist
- `MD` monotonic increasing
- no duplicate `row_idx`
- `TVT_input` missing tail is contiguous
- train `TVT_input` equals `TVT` before PS
- target rows are non-empty
- GR missingness is recorded

## Typewell Checks

- required columns exist
- `TVT` and `GR` are non-null
- `TVT` range overlaps relevant horizontal well TVT range
- duplicate TVT values are handled

## Train/Test Parity Checks

- model feature columns must exist in both splits
- no target column in test matrix
- submission IDs exactly match `test_base[is_target]`

## Experiment Artifact Checks

Before trusting an experiment:

- OOF row count equals training target row count
- fold column has expected folds
- no validation well appears in training within same fold
- submission row count equals sample submission row count
- submission IDs exactly match sample submission
