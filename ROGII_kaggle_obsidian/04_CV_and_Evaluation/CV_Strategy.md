# CV Strategy

Primary validation:

```text
GroupKFold by well_id
```

Evaluation rows:

```text
TVT_input is NaN
```

Reason:

- Adjacent rows in the same well are highly correlated.
- Row-random CV leaks local continuity.
- The test task predicts future missing tails, so local CV should mimic held-out wells.

Secondary checks:

- spatial holdout
- typewell similarity holdout
- GR missingness slices
- hidden-length slices

## Recommended v001 Fold

Use a well-level split that balances target-row counts:

```text
data/folds/folds_group_well_v001.csv
columns: split, well_id, fold
```

Implementation idea:

- Build row-level records only for target rows.
- Run `GroupKFold(n_splits=5)` with `groups=well_id`.
- Collapse the resulting fold assignment back to one row per `well_id`.
- Join folds to training rows by `well_id`.

This keeps all rows from a well in one fold while balancing the number of evaluated target rows per fold.

## Why Not Row Random

Row-random split is invalid because:

- adjacent rows share nearly identical `MD`, `X`, `Y`, `Z`, `GR`
- target `TVT` is smooth within many wells
- train rows would be immediate neighbors of validation rows
- the resulting score would measure interpolation, not unseen-well generalization

## Why Not Simple KFold by Well Count Only

Randomly splitting wells into equal counts is acceptable as a baseline, but fold target-row counts can drift because wells have different hidden lengths.

For ROGII, target rows per well range widely, so balancing evaluation rows is preferred.

## Evaluation Contract

Every CV report should include:

- fold RMSE on target rows
- number of wells per fold
- number of target rows per fold
- weighted overall RMSE over all OOF target rows
- unweighted mean of well-level RMSE
- bias: `mean(pred - TVT)`
