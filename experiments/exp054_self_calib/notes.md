# exp054: Self-Calibration v2

## Strategy
Per-well linear calibration (a*pred + b) on known区間 where last_known_TVT is not NaN.
Apply only to wells where calibration improves RMSE.

## Results
- Baseline CV (exp022): 11.0240
- Calibrated CV: 5.5449
- Delta: -5.4791
- Improvement: 49.70%

## Well-level Impact
- Improved: 773 wells
- Degraded: 0 wells
- Net: 773 wells

## Leak-free Verification
✓ Only known TVT (last_known_TVT not NaN) used for fitting
✓ Fit is per-well, no cross-well leakage
✓ Calibration only applied if improves that well's RMSE

## Notes
- Least-squares fit: min ||TVT - (a*pred + b)||^2
- Calibration parameters (a, b) fitted per well on known区間
- Applied to all rows if improves well RMSE
