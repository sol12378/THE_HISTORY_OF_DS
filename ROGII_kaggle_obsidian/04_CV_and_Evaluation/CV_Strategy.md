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
