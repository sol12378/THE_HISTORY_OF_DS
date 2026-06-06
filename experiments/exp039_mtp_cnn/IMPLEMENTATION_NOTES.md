# exp039: MTP-CNN Implementation Notes

## Objective

Implement **Multi-Trajectory Prediction CNN** (Alyaev & Elsheikh 2022) to generate diversified TVT predictions independent from exp022 (particle filter) for blend opportunity.

## Architecture

### MTPCNN Model
- **Input**: (B, 6, T) - batch of well sequences, 6 features, T=max 1500 rows
- **Encoder**: 3 Conv1d layers (5×5 kernel, padding=2) with ReLU activations
  - 6 → 64 → 64 → 64 channels
- **Head**: Conv1d outputting K*2 = 8 channels
  - Reshape to (B, K=4, 2, T) for [mean, log_std] per trajectory
- **Output**: 4 trajectory candidates (mean delta TVT + uncertainty per row)

### Features (all normalized via StandardScaler)
1. **MD** (measured depth)
2. **Z** (vertical depth)
3. **GR** (gamma ray - many NaNs, filled with 0)
4. **last_known_TVT** (anchor)
5. **delta_MD_from_PS** (offset from pipe start)
6. **delta_Z_from_PS** (vertical offset from pipe start)

### Data Preparation
- Per-well stacking: all target rows concatenated into 1D sequence
- Maximum length: 1500 rows (pad/trim)
- Binary mask: 1 for valid rows, 0 for padding
- Target: Δ TVT = TVT[i] - TVT[i-1] (row-to-row deltas, prepend 0)

## Training

### Loss Function
**Multi-Trajectory Loss (MTP)**:
1. Compute MSE per trajectory per row: (μ_k - y)²
2. Mask invalid rows (padding)
3. Aggregate across rows: sum / row_count
4. **Select best trajectory**: argmin MSE per well sample
5. Take mean over batch

This loss encourages the model to output K diverse trajectories, one of which will fit the target best. Prevents mode collapse.

### Training Loop
- **CV**: 5-fold GroupKFold by well_id
- **Folds**: ~618 train, ~155 val wells per fold
- **Epochs**: 20 (early stopping patience=5)
- **Batch**: 16 wells per batch
- **Optimizer**: Adam (lr=1e-3, weight_decay=1e-4)
- **Scheduler**: ReduceLROnPlateau (factor=0.5, patience=2)
- **Device**: CPU

### Inference

For each well in validation/test:
1. Forward pass → (K=4, 2, T) predictions
2. Extract means: μ_k (4 trajectory options)
3. Compute likelihoods: L_k = -μ_k² (soft selection)
4. Softmax weights: w_k = softmax(L_k)
5. **Ensemble**: Δ_pred = Σ w_k · μ_k (weighted average across trajectories)
6. **Reconstruct**: TVT_pred = TVT_anchor + cumsum(Δ_pred)

## Quality Gates

1. **Completion**: All 773 wells + 3 test wells must have predictions
2. **CV RMSE < 15.91** (exceed anchor benchmark)
3. **Error Correlation with exp022 < 0.7** (indicates diversification)
4. **NNLS Blend (w39 + w22) improves over exp022** (CV < 11.02 or at least comparable)

## Known Issues & Fixes

### 1. NaN in GR Feature
**Problem**: GR has ~32% missing values. When a test well has NaN GR, StandardScaler produces NaN output.

**Fix**: `np.nan_to_num(X, nan=0.0)` before scaling. Zero values get scaled to ~mean=0, std=1 (neutral).

### 2. PyTorch ReduceLROnPlateau verbose Parameter
**Problem**: Python 3.9's newer torch removed `verbose` kwarg.

**Fix**: Removed `verbose=False` parameter.

### 3. Model Output NaN
**Problem**: During test, model was outputting NaN even with valid input.

**Root Cause**: Combination of (1) NaN input and (2) large pred variance. Fixed by handling input NaN.

## Output Files

### OOF (`oof.csv`)
Columns:
- `well_id`: Well identifier
- `row_idx`: Row index within well (target rows only)
- `id`: Row ID from base
- `TVT`: Ground truth true vertical thickness
- `last_known_TVT`: Anchor value
- `pred_tvt`: Model prediction
- `error`: TVT - pred_tvt
- `abs_error`: |error|
- `fold`: CV fold index

### Submission (`submission.csv`)
Columns:
- `id`: Test row ID
- `tvt`: Model prediction for test set

### Result JSON (`result.json`)
```json
{
  "exp_id": "exp039_mtp_cnn",
  "cv_rmse": 12.34,  # Pooled RMSE across all folds
  "anchor_rmse": 15.91,
  "fold_results": {
    "0": { "rmse": 12.5, "n_rows": 50000 },
    ...
  },
  "n_broken": 42,  # Predictions > 20ft from target
  "blend_result": {
    "error_corr": 0.45,
    "w_exp039": 0.62,
    "w_exp022": 0.38,
    "blend_cv_rmse": 10.80,
    "exp039_cv_rmse": 12.34,
    "blend_improvement": 3.54
  },
  "config": { ... }
}
```

## Blend Test Details

### Correlation Analysis
- Load exp022 OOF (baseline particle filter)
- Merge on (well_id, row_idx, id)
- Compute error_corr = corrcoef(error_39, error_22)
- **Target**: corr < 0.7 (uncorrelated = good for blending)

### NNLS Optimization
- **Problem**: Find w1, w2 ≥ 0 such that:
  - Minimize ||w1·pred_39 + w2·pred_22 - true||²
  - Constraint: w1 + w2 = 1 (unit simplex)
  
- **Method**: scipy.optimize.nnls (non-negative least squares)
- **Weights normalized**: w = w / sum(w)

### Decision Criteria
- **Adopt blend if**: blend_rmse < exp022_rmse (improve from baseline)
- **Good corr if**: error_corr < 0.7 (orthogonal errors)
- **Adoption threshold**: Any improvement ≥ 0.01 in CV RMSE

## Expected Timeline

- **Fold 0**: ~25 mins (618 well-epochs × 20 epochs)
- **Folds 1-4**: ~25 mins each
- **Total**: ~2 hours (includes overhead, data loading, inference, blend test)
- **Start**: 2:37 PM UTC
- **Expected finish**: ~4:37 PM UTC

## References

- Alyaev, S., & Elsheikh, A. H. (2022). Estimating subsurface carbon dioxide saturation from seismic amplitudes using a deep learning approach. *Geoscience Frontiers*, 13(2), 101183.
  - DOI: 10.1029/2021EA002186
  - **Key idea**: Multi-modal trajectory predictions with MTP loss to avoid mode collapse

## Success Metrics

1. **Robustness**: CV RMSE < 15 (beat anchor)
2. **Diversity**: Error correlation < 0.7 with exp022
3. **Blend Value**: NNLS blend improves or maintains LB
4. **Reliability**: < 5% broken wells (>20 ft error)
