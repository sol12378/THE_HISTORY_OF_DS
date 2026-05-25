# Schema and Contracts

## File-Level Contracts

Each horizontal well file must satisfy:

- has `MD`, `X`, `Y`, `Z`, `GR`, `TVT_input`
- train additionally has `TVT`
- `MD` is monotonic increasing
- `row_idx` is the original zero-based CSV row index
- `TVT_input` missing region should be a contiguous tail

Each typewell file must satisfy:

- has `TVT`
- has `GR`
- train may have `Geology`
- `TVT` should be sorted or sortable

## Identifier Contracts

Canonical IDs:

```text
well_id = filename before "__"
row_idx = original integer row position within horizontal CSV
submission_id = f"{well_id}_{row_idx}"
```

Never drop `well_id` or `row_idx` from processed data.

## Naming Contracts

Use uppercase raw column names as-is:

```text
MD, X, Y, Z, GR, TVT, TVT_input
```

Use snake_case for engineered columns:

```text
well_id
row_idx
ps_idx
last_known_TVT
delta_MD_from_PS
is_target
```

Do not rename raw columns differently in separate scripts.

## Target Contract

Training target rows:

```text
is_target = TVT_input.isna()
```

Evaluation must use only `is_target=True` rows.

## Feature Parity Contract

Any feature used by a model must be computable for both train and test without seeing test target `TVT`.

Train-only columns:

- `TVT`
- `ANCC`
- `ASTNU`
- `ASTNL`
- `EGFDU`
- `EGFDL`
- `BUDA`
- train typewell `Geology`

Use train-only columns for analysis or auxiliary targets only after explicitly documenting leakage risk.

## Base Schema v001

The first stable base schema is `v001`.

Required well-row columns:

```text
split
well_id
row_idx
source_path
MD
X
Y
Z
GR
TVT_input
TVT                  # train only, absent or null in test
id                   # test submission id, optional/null in train
is_target
is_known_tvt
is_gr_missing
ps_idx
n_rows_in_well
known_length
hidden_length
last_known_TVT
last_known_MD
last_known_X
last_known_Y
last_known_Z
delta_MD_from_PS
delta_X_from_PS
delta_Y_from_PS
delta_Z_from_PS
post_ps_step
row_frac
```

Optional analysis-only columns:

```text
ANCC
ASTNU
ASTNL
EGFDU
EGFDL
BUDA
```

If included in a base table, these must be prefixed or flagged as analysis-only and excluded from default model feature lists.

## Validation Gates

No processed table should be considered valid unless:

- all required columns exist
- row count matches raw source row count
- `well_id`, `row_idx` is unique within split
- `ps_idx` is not null for every well
- `hidden_length > 0`
- train `TVT` is non-null
- test `id` exists for all target rows
- sample submission target IDs match test target IDs exactly
