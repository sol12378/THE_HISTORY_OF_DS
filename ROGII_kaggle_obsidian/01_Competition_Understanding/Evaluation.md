# Evaluation

Official metric:

```text
RMSE = sqrt(mean((manualTVT - predictedTVT)^2))
```

Local validation rules:

- Evaluate only rows where `TVT_input` is missing.
- Split by well, not by row.
- Save OOF predictions for every experiment.
- Track CV-LB gap and leakage risk.
