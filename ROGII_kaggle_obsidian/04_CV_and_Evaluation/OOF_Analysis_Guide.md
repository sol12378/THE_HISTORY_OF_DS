# OOF Analysis Guide

Every experiment should save OOF with:

- `well_id`
- `row_idx`
- `fold`
- `TVT`
- `pred`
- `error`
- `abs_error`
- `TVT_input_isna`

Required summaries:

- overall RMSE
- fold RMSE
- well RMSE
- bias
- error by distance from Prediction Start
- error by GR missingness
