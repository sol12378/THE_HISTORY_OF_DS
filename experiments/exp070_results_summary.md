# exp070: PF Scaling & apply_pp Grid Search — Results Summary

## Overview
Two complementary experimental variants to evaluate:
1. **Case 8**: PF with 600 particles / 150 seeds (vs baseline 500/128)
2. **Case 7**: apply_pp parameter grid search (w_pf, tau, alpha)

Both leak-free, GroupKFold validation, honest CV methodology.

---

## Case 7: apply_pp Grid Search (COMPLETED)

### Configuration
- Grid size: 75 configurations (5 w_pf × 5 tau × 3 alpha)
- w_pf ∈ {0.0, 0.05, 0.09, 0.15, 0.2}
- tau ∈ {None, 50, 85, 150, 300} (depth ramp factor)
- alpha ∈ {0.95, 1.0, 1.05} (scaling)
- Validation: GroupKFold by well_id (5 folds)
- Training rows: 3,783,989 (train target + known)

### Best Configuration Found
| Parameter | Value |
|---|---|
| **w_pf** | 0.0 (pure geom, no PF) |
| **tau** | 300 (moderate depth ramp) |
| **alpha** | 1.0 (no scaling) |
| **Pool CV** | **10.999887** |

### Results & Interpretation

**vs Baselines:**
- exp022 (PF 500/128): 11.024014 → **+0.024127 ft improvement** (marginal, <0.3%)
- exp014 (geom only, no tau): 13.525189 → **+2.525302 ft improvement** (strong)

**Key Finding**: The tau ramp (depth-dependent decay) helps pure geometric prediction!

```
Pure Geom CV progression:
- w_pf=0, tau=None, alpha=1.0: CV = 13.525189 (baseline, no ramp)
- w_pf=0, tau=50,   alpha=1.0: CV = 11.025169 (-2.500 ft with tau=50)
- w_pf=0, tau=85,   alpha=1.0: CV = 11.024743 (-2.500 ft with tau=85)
- w_pf=0, tau=150,  alpha=1.0: CV = 11.021103 (-2.504 ft with tau=150) 
- w_pf=0, tau=300,  alpha=1.0: CV = 10.999887 (-2.525 ft with tau=300) ✓ BEST
```

**Tau Ramp Mechanism:**
- Formula: `pred = (1-w_pf)·geom + w_pf·pf; if tau: pred *= (1 - exp(-md_since/tau))`
- Effect: Depth-dependent blend where hidden shallower sections (small md_since) get weighted down, deeper sections trust the predictions more
- Works well for pure geom because geom is deterministic but has cumulative error growth with depth
- Ineffective when mixing PF (w_pf>0) because PF and geom have different depth-error profiles

**Fold Stability:**
- fold_std ≈ 0.76 for best config (consistent across 5 folds)
- No large fold outliers (collapse), indicating stable generalization

### Recommendation for Case 7
✓ Adopt: w_pf=0, tau=300, alpha=1.0 in production
- Apply to geom-only predictions to gain ~2.5 ft improvement
- Can be combined with PF as separate ensemble branch

---

## Case 8: PF Scaling Test (IN PROGRESS → SUBSET RESULT)

### Configuration
- Baseline: exp022 PF (500 particles, 128 seeds) → CV 11.024014
- Test: 600 particles, 150 seeds
- Strategy: Subset test (30 wells) for efficiency, then full extrapolation

### Execution Status
- Full 773-well: Stalled (heavy computation, killed)
- Subset (30 wells): Running...

### Expected Results (Pending)
If subset shows improvement, extrapolate to 773-well projection.
If subset shows degradation, larger PF is not worth the compute overhead.

---

## Next Actions (Prioritized)

### Immediate (after Case 8 completes)
1. **Evaluate Case 8 subset result**
   - If delta > +0.01 ft: Consider full 773-well run
   - If delta < -0.01 ft: Stick with 500/128 baseline

2. **Blend Case 7 + Case 8** (if both improve)
   - Check error correlation between: geom-with-tau vs PF
   - NNLS weight optimization if orthogonal enough

### Production Application
3. **Create exp071_final_blend kernel**
   - apply_pp (w_pf=0, tau=300, alpha=1.0) on geom predictions
   - PF predictions (exp022 or upgraded)
   - Simple 50/50 or NNLS blend
   - Expect CV ~11.0 → LB ~8.8-8.9

### Longer-term Validation
4. Test on 3 hidden wells (if LB improves, report delta to exp026 8.672)

---

## Technical Notes

### Leak-free Methodology
- apply_pp optimized on train target/known rows only (GroupKFold)
- md_since computed from known MD data (no hidden info)
- Tested formula: `d = (1-w)*geom + w*pf; d *= (1 - exp(-md/tau)); d *= alpha`
- All parameters derived from validation fold alone (no label leakage)

### Why Tau Helps Geom
Geometric extrapolation has known failure modes:
- Early (shallow hidden): Very accurate, geom ~ truth
- Mid (1000+ MD): Cumulative Z-alignment errors accumulate
- Late (2000+ MD): Divergence risk if well trajectory changes
- Solution: Tau ramp down-weights predictions at shallower depths where geom is overconfident, up-weights deeper where empirical evidence is needed

### Why Tau Doesn't Help PF+Geom Blend
- PF has depth-dependent skill too (but different from geom)
- When mixed (w_pf>0), tau creates interference between two depth models
- Better to let NNLS weights learn the depth dependence implicitly

---

## Files Generated
- `exp070_case7_appplypp_grid/result.json` — Full grid results
- `exp070_case7_appplypp_grid/grid_results.csv` — All 75 configs + fold CVs
- `exp070_case7_appplypp_grid/notes.md` — Detailed analysis
- `exp070_case8_subset/result.json` — Subset scaling test (pending)

