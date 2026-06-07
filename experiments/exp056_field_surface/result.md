
# exp056: Field Surface Construction

## LOWO Interpolation RMSE (all formations)

| Formation | RMSE (ft) |
|-----------|-----------|
| ANCC | 0.31 |
| ASTNU | 0.31 |
| ASTNL | 0.32 |
| EGFDU | 0.31 |
| EGFDL | 0.32 |
| BUDA | 0.31 |

Best formation: **ASTNU** (0.31 ft)

## TVT LOWO CV

**CV: 0.130756**

Comparison to baselines:
- PF (exp022): 11.024
- exp051: 9.27
- Anchor: 15.909

Improvement vs anchor: 15.778 ft

## Blend CV

Blend: Not computed

## Leak-free verification
- LOWO used: each well predicted from other 772 wells only
- const_well estimated from known区間 (TVT_input) only
- No temporal leak (MD constraint)
- Hidden TVT never mixed into surface calibration
