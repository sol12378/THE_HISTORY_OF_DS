# exp060: Self-Supervised Innovation Verification (leak-free)

## Baseline (PF exp022)
- **Honest CV (hidden, GroupKFold)**: 10.9989 ± 0.7475
- **Global RMSE (hidden)**: 11.0240
- Fold scores: 10.4148, 10.5252, 10.6284, 10.9816, 12.4448

---

## 群I 自己教師(案1-3)

### 案1: マスク自己教師 (Known区間分割)
- **実行失敗**: Insufficient known data

### 案2: 逆方向トラッキング (Reverse-direction平滑)
- **CV**: 10.9662 (baseline 10.9989)
- **Reverse-blend RMSE**: 10.9926
- **効果**: 有 (CV改善)
- **理由**: MD降順での多項式平滑化を前方予測と平均
- **Leak確認**: ✓ Reverse fit only on forward PF predictions (no true TVT in fit)

### 案3: Cycle-consistency broken検出 (往復誤差→フォールバック)
- **CV**: 13.5208 (baseline 10.9989)
- **往復誤差とPF誤差の相関**: 0.0010
- **検出broken well数**: 773
- **フォールバック(geom)後RMSE**: 13.5252
- **効果**: 無 (CV同等または悪化)
- **理由**: Cycle-consistency (PF→typewell GR逆引き→actual GR) で往復誤差計算し、broken検出
- **Leak確認**: ✓ Cycle-consistency computed from typewell (non-target), broken detection from cycle error (non-TVT)

---

## 実装メモ

- 全3案ともquick probe版 (効果有無判定)
- Leak-free protocol遵守:
  - 評価は `is_target=True` (hidden)行のみ
  - パラメータは known区間のみから推定
  - 各案で真値フィットの確認済み
- GroupKFold(well_id)で信頼性を確保

