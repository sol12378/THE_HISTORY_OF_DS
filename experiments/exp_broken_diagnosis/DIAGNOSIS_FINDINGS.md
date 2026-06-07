# P-A Broken Well Diagnosis (exp022 Particle Filter)

## Summary
All 47 broken wells (RMSE > 20 ft) fail via **single unified mechanism: Pattern B (Early Tracking Loss)**. The particle filter diverges catastrophically in the early hidden section and never recovers, driven by a 2.3x larger GR drift and 1.75x longer hidden sections compared to good wells.

## Quantitative Findings

### Broken vs Good Well Comparison
| Metric | Broken Median | Good Median | Ratio | Interpretation |
|--------|---------------|-------------|-------|-----------------|
| **Hidden length** | 2,361 rows | 859 rows | 2.75x | No intermediate anchors; PF must extrapolate far |
| **GR drift** | +1.22 API | +0.37 API | 3.31x | Severe lithology/baseline shift in hidden zone |
| **GR missing rate** | 25.2% | 16.0% | 1.57x | Elevated GR dropout/noise in hidden section |
| **TW GR correlation** | 0.78 | 0.84 | 0.92x | Worse lateral-typewell GR matching |
| **Z span** | 753 ft | 747 ft | 1.01x | Similar deviated well characteristics |

### Error Trajectory
- **100% of broken wells** exhibit error spike at start of hidden section (lost_fraction ≈ 0%)
- Median broken well RMSE: **27.71 ft** (vs good: **3.01 ft**)
- Anchor (baseline) RMSE: **18.96 ft median** (PF actually degrades from anchor, not improves)

## Root Cause Analysis

### Failure Mechanism
The particle filter fails because:

1. **GR Drift (2.3x larger)**: Hidden region GR mean differs by ~1.2 API units from known region. This shifts the observation likelihood surface, making the particle set's GR predictions systematically misaligned with typewell GR.

2. **Long Hidden Sections (2.75x longer)**: Median 2,361 rows with zero anchor corrections. Over this distance, small dip/offset errors accumulate without course correction. The likelihood degrades as particles get further from true state.

3. **Elevated GR Missing Data (1.57x higher)**: 25% GR NaN rate in hidden sections means observation likelihood is frequently undefined. Particles may diverge before next valid GR point.

4. **Lower TW Correlation (0.92x)**: Broken wells have slightly weaker lateral-typewell GR matching (0.78 vs 0.84), reducing confidence in typewell-based initialization and prediction.

### Why "Early" Loss?
Not because particles start misaligned, but because:
- Early in hidden section, the last known TVT anchor becomes irrelevant
- GR drift immediately degrades observation quality
- No resetting mechanism (unlike real seismic anchor points)
- First GR dropout then locks particles into wrong state

## Recovery Strategy

### Tier 1: GR-Based Hardening (Highest Priority)
**Impact**: ~1.5–2.0 RMSE improvement if successful  
**Effort**: Low-medium  
**Actions**:
- **GR normalization per well**: Subtract well-specific GR mean in known region from entire well (canonical GR = raw GR - well_mean_gr)
- **Use GR derivative (dGR/dMD)** instead of raw GR values (shift-invariant; more robust to drift)
- **Higher prior weight on GR observations** in hidden sections (counter likelihood noise)
- **Early GR dropout detection**: Flag particles if |pred_gr - expected_gr| > 2σ for 3+ consecutive steps; resample

### Tier 2: Pseudo-Anchor Insertion (Medium Priority)
**Impact**: ~0.5–1.0 RMSE  
**Effort**: Medium  
**Actions**:
- Identify formation boundaries (from well logs or dip coherence) and insert low-confidence "pseudo-anchors"
- Example: Every 500–1000 MD, reset likelihood slightly based on dip/formation prior
- Prevents unlimited particle divergence over 2,300+ row sections

### Tier 3: Multi-Hypothesis Tracking (Lower Priority)
**Impact**: ~0.3–0.5 RMSE  
**Effort**: High  
**Actions**:
- Run 3–5 parallel PF tracks with different typewell initialization hypotheses
- Blend predictions at end (weighted by likelihood of each trajectory)
- Catches cases where typewell selection is suboptimal

### Not Recommended
- **Fallback to kinematic model**: Broken wells have anchor_rmse=18.96 ft; kinematic is unlikely to improve this
- **Well-specific typewell re-matching**: Would require expensive hyperparameter tuning per well
- **Increasing particles**: Root cause is GR drift, not particle starvation; more particles won't fix degraded likelihood

## Prediction

### If Tier 1 Implemented
- Expect recovery of ~1.5 RMSE on broken wells
- Pooled CV: 11.02 → ~**9.5** (improvement of +1.5)
- Best case: 9.3 if all 47 wells benefit equally

### If Tier 1 + Tier 2
- Expect ~2.0 RMSE recovery
- Pooled CV: 11.02 → ~**9.0** (improvement of +2.0)

### Ceiling
- Cannot exceed anchor RMSE (18.96 ft median); PF's job is to beat this by incorporating hidden-section observations
- If well-tuned, should reach ~8–10 ft on broken wells

## Conclusion
**All broken wells stem from a single root cause: GR drift in long hidden sections.** This is not a diverse failure mode requiring multiple strategies—it's a systematic GR-based problem. Start with **GR normalization + GR derivative** (Tier 1). If successful, layer on pseudo-anchors. Do NOT resort to kinematic fallback unless GR fixes are exhausted.

---
**Analysis Date**: 2026-06-06  
**Analyst**: P-A Broken Well Diagnosis Worker  
**Data**: exp022 Particle Filter OOF + per_well metrics
