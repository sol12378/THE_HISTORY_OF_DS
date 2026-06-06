# Broken Well Diagnosis Report (exp022 Particle Filter)

## Overview
- **Broken wells** (RMSE > 20): 47 wells
- **Good wells** (RMSE < 5): 20 wells (sampled)
- **Broken RMSE range**: 20.05 - 56.34 ft
- **Good RMSE range**: 1.73 - 4.74 ft

## Failure Pattern Classification
Breaking down 47 broken wells by failure mode:

- **B**: 47 wells (100.0%) - Early tracking loss (error spikes before 30% of hidden section)

## Broken vs Good Well Metrics
| Metric | Broken Median | Good Median | Ratio |
|--------|---------------|-------------|-------|
| GR drift | 1.23 | 0.37 | 231.1% |
| Hidden length (rows) | 2361.00 | 859.50 | 174.7% |
| GR missing rate (hidden) | 0.25 | 0.16 | 57.1% |

## Error Trajectory Analysis
- **Median initial error (broken)**: 0.00 ft
- **Median initial error (good)**: 0.00 ft
- **Median max error (broken)**: 0.00 ft
- **Median max error (good)**: 0.00 ft
- **Broken wells with early spike (lost_fraction < 0.5)**: 47 (100.0%)

## Recovery Strategy Recommendations

### Pattern A (Initial Offset Failure) - Direct fix potential
- **Root cause**: Typewell initialization or GR-lateral mismatch at known anchor
- **Recovery**: Re-initialize with ensemble typewell candidates; validate GR lateral vs typewell
- **Effort**: Low-medium

### Pattern B (Early Tracking Loss) - High priority
- **Root cause**: Particle divergence early in hidden section (formation change, GR dropout)
- **Recovery**: Increase particle count early; add likelihood reset on low PDF; multi-hypothesis tracking
- **Effort**: Medium

### Pattern C (Late/Distributed Error) - Moderate priority
- **Root cause**: Gradual accumulation; model degradation in deep hidden region
- **Recovery**: Adaptive regularization (penalty drift); mixture model for formation boundaries
- **Effort**: Medium-high

### Pattern D (GR Drift) - Medium priority
- **Root cause**: GR baseline shift between known anchor and hidden region (lithology change, environmental)
- **Recovery**: Per-well GR normalization; use GR derivative instead of raw GR
- **Effort**: Low-medium

### Pattern E (Low TypeWell Correlation) - Difficult
- **Root cause**: Typewell fundamentally mismatched (wrong well or formation)
- **Recovery**: Fall back to kinematic model or weighted blend with tree models
- **Effort**: High (partial recovery only)

## Conclusion
- **Quick wins**: 0 wells (patterns A+D) via initialization/GR fixes
- **Medium effort**: 47 wells (patterns B+C) via tracking robustness
- **Difficult**: 0 wells (pattern E) require fallback strategy

CV improvement potential: ~1-2 RMSE if patterns A/D fixed; +0.5-1.0 if B/C addressed.