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
