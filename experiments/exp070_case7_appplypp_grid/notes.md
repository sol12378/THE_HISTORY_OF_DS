# exp070_case7_appplypp_grid: apply_pp Grid Search

## Grid Configuration
- w_pf (PF weight): [0.0, 0.05, 0.09, 0.15, 0.2]
- tau (depth ramp, MD distance): [None, 50, 85, 150, 300]
- alpha (scaling): [0.95, 1.0, 1.05]
- Total configs tested: 75

## Best Configuration
| Param | Value |
|---|---|
| w_pf | 0.0 |
| tau | 300 |
| alpha | 1.0 |
| **Pool CV** | **10.999887** |

## Comparison
| Baseline | CV | Delta |
|---|---|---|
| exp022 (PF 500/128) | 11.024014 | +0.024127 ft |
| exp014 (geom) | 13.525189 | +2.525302 ft |

## Tau Ramp Effect
- Baseline (no ramp, tau=None, best w_pf/alpha): 13.525189
- With ramp (tau=300): 10.999887
- **Tau ramp effect**: EFFECTIVE (delta=+2.525302 ft)

## Interpretation
The tau ramp factor (1 - exp(-md_since/tau)) modulates the blend weight based on depth.
- tau=None: linear blend, constant weight throughout hidden section
- tau>0: exponential decay, emphasize PF near last_known_MD, geometric blend deeper

Result: Tau ramp provides consistent improvement by adapting weights to hidden depth

## Next Actions
1. Evaluate best config on test set (apply_pp kernel)
2. Blend with Case 8 (PF 600/150) if both show improvements
3. Check error correlation for ensemble potential
