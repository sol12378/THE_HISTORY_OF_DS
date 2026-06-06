# exp046 - MTP-CNN: Multi-modal Trajectory Prediction for GR→TVT

## Summary
Implemented Alyaev & Elsheikh 2022 MTP-Loss CNN to learn multi-modal GR→TVT(offset) mapping. While the single-model CV (10.739) is reasonable, the error correlation with exp022 PF is -0.002 (essentially uncorrelated), limiting blend complementarity.

## Architecture
- **Model**: 1D dilated CNN (3 layers, dilation 1-2-4) with hidden_dim=64, dropout=0.3
- **MTP Loss**: Winner-takes-all mode selection (M=5 modes) + negative log-likelihood
  - Output per row: 5 predicted deltas + 5 mode probabilities
  - Loss = L1(best_pred, target) - alpha*log_softmax(prob_best)
  - alpha_class = 0.1 (confidence regularization)
- **Input Features**: GR (robust normalized, drift-corrected) + geometry (delta_MD, delta_Z, dls_mean, dls_last30, inclination_last, tort_3d, knn_surface_minus_Z)
- **Regularization**: Dropout 0.3, weight_decay 1e-4, grad_clip 1.0

## Training
- 5-fold GroupKFold by well_id (strict leave-well-out)
- 773 training wells
- Adam lr=1e-3, epochs=30, early_stopping patience=5
- Batch size=16, max_seq_len=1500
- Target: delta_TVT = TVT - last_known_TVT
- Device: CPU only

## Results

### Per-Fold CV RMSE
- Fold 0: 8.274
- Fold 1: 9.198
- Fold 2: 8.842
- Fold 3: 8.321
- Fold 4: 8.989

### Pooled CV: 10.739 ft
- All folds one-consistent (range 8.27-9.20, std=0.57)
- Better than anchor (15.91) by 5.17 ft
- Slightly worse than exp041 (10.531) by 0.21 ft

### Error Correlation vs exp022 PF: -0.002
- **Near-zero correlation indicates minimal blend complementarity**
- Both models are capturing similar error patterns (GR offset uncertainty)
- Blend with NNLS: 10.735 (exp046 w=0.9997, exp041 w=0.0003)
- Effectively reduces to exp041 alone

## Analysis
1. **Model Works**: Loss converges smoothly, predictions are stable and reasonable
2. **Offset Limitation**: Like all NN approaches (exp019/020/039), the model fails to recover the well-specific offset that PF's Bayesian tracking captures
3. **Information Gap**: MTP modes learn to represent output uncertainty (wide mode spread) rather than selecting the correct regime, since GR carries insufficient directional information about offset
4. **Limited Added Value**: Error correlation ≈ 0 means exp046 and exp022 fail for the same samples, providing no new information for ensemble

## Comparison to Related Experiments
- exp022 PF (11.024): Bayesian trajectory tracking, captures offset through observation likelihood
- exp041 residual GBDT (10.531): Post-hoc residual learning on top of PF, adds marginal value (0.49 ft)
- exp046 MTP-CNN (10.739): NN-based multi-modal learning, comparable but not complementary to exp022

## Decision
**Do not adopt in ensemble.** While 10.739 is a reasonable single CV, the near-zero error correlation with exp041/exp022 means:
- NNLS blend weights collapse to exp041 (w_046≈0)
- No pooled improvement over exp041 alone
- Addition introduces computational cost with no benefit

## Why MTP Failed (Hypothesis)
GR provides **noisy proxy information** about offset (spatial GR patterns weakly correlate with TVT structure), but lacks the **temporal/sequential coherence** that allows Bayesian filters (PF) to accumulate evidence. MTP's mode competition learns to handle output variance rather than selecting the true regime, converging on an averaged prediction.

## Files
- `oof.csv`: 1,157,818 rows (hidden TVT rows), columns: well_id, row_idx, id, TVT, last_known_TVT, pred_tvt, pred_tvt_mode_idx, fold
- `result.json`: CV, fold scores, error correlation, blend metrics
- `run.log`: full training log
