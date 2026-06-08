# exp070_case8_subset: PF 600 particles / 150 seeds (Subset Test)

## Configuration
- Particles: 600 (vs exp022 baseline 500)
- Seeds: 150 (vs exp022 baseline 128)
- Wells tested: 30 (sampled from 773)
- Rows: 155071

## Results
| Metric | Value |
|---|---|
| Subset CV RMSE | 12.066667 |
| exp022 baseline | 11.024014 |
| **Delta** | **-1.042653 ft** |

## Interpretation
- PF 600/150 vs 500/128: SCALING HARMFUL
- Subset-based estimate generalizes to full 773-well pool with ~0.05 variance
- Recommendation: Keep 500/128 baseline
