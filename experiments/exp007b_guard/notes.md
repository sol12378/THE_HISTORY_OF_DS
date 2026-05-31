# exp007b_guard

## 目的

exp007 の後処理として、双方向 anchor guard を適用して catastrophic 予測を抑制する。

## 発見と仮説

- exp007 fold4: best_iteration=600 (n_estimators 上限) → underfitting
- `|mean_pred_delta7| > 30` の wells で RMSE 38-48 の catastrophic 予測が発生
- exp006 は `mean_pred_delta > 30` の正方向のみガード → 負方向ガード漏れ

## 変更内容

- **n_estimators**: 600 → 1500 (early_stopping=50 は同じ)
- **ガードルール** (exp007b 独自):
  - `|mean_pred_delta| > 30.0` または `hidden_length > 8000.0` → alpha=0 (full anchor)
  - それ以外 → alpha=1.0 (LGB そのまま)

## 結果

| metric | value |
|---|---|
| LGB raw CV RMSE | 13.853360 |
| Blended CV RMSE | 13.985993 |
| exp007 CV RMSE | 13.867054 |
| 改善幅 vs exp007 | -0.118939 |
| LGB raw 改善幅 | -0.132632 |

## Fold別RMSE

| fold | rmse | best_iteration |
| --- | --- | --- |
| 0 | 13.061989 | 458 |
| 1 | 13.98059 | 270 |
| 2 | 13.618236 | 180 |
| 3 | 14.228974 | 514 |
| 4 | 14.339238 | 872 |

## Guard Rule 分布 (train)

| guard_rule | n_wells |
| --- | --- |
| no_guard | 756 |
| full_anchor | 17 |

## Top 20 Feature Importance (gain)

| feature | importance_gain |
| --- | --- |
| dZ_dMD_from_ps | 797540842 |
| last_known_Y | 367250289 |
| known_length | 354764559 |
| pre_ps_dZ_dMD | 344650199 |
| pre_ps_tvt_curvature | 338060751 |
| Y | 304884151 |
| X | 300018304 |
| pre_ps_tvt_slope_last20 | 282196481 |
| delta_X_from_PS | 257124030 |
| delta_Z_from_PS | 253112178 |
| pre_ps_tvt_slope_last5 | 243817259 |
| n_rows_in_well | 229283098 |
| pre_ps_horiz_dMD | 199809850 |
| Z | 197519320 |
| last_known_MD | 197289901 |
| last_known_TVT | 191538132 |
| last_known_X | 165322687 |
| pre_ps_dY_dMD | 150206442 |
| pre_ps_dX_dMD | 146850020 |
| last_known_Z | 146453371 |

## 考察: guard が逆効果だった理由

| 指標 | 値 |
|---|---|
| full_anchor 17 wells の LGB RMSE | 15.09 |
| full_anchor 17 wells の anchor RMSE | 18.03 |
| full_anchor 17 wells の blended RMSE | 18.03 (alpha=0 なので anchor と同値) |

- `|mean_pred_delta| > 30` の17 wells では、LGB (15.09) が anchor (18.03) より明らかに優秀。
- alpha=0 にすることで LGB の良い予測を捨て、より悪い anchor を使うことになった。
- **解釈**: n_estimators=1500 で fold4 の underfitting が改善され、exp007 では catastrophic だった wells の予測も修正されていた可能性が高い。
- 結論: **n_estimators=1500 の LGB raw (CV=13.853360) が本実験の best。guard は不要。**

## 次の改善案

1. **guard 閾値の見直し**: `|mean_pred_delta| > 30` を `|mean_pred_delta| > 50` 等に上げて guard を絞る、またはガード完全無効で submit
2. **n_estimators=1500 のみ submit**: LGB raw (13.853360) を submission として使う
3. **fold4 の per-well 分析**: fold4 で RMSE が高い well を特定し、Group D 特徴量を検討

## リーク懸念

- `mean_pred_delta` は LGB 予測からのみ計算 (OOF/test prediction)。train target には触れない。リーク低。
- `hidden_length` は base table に存在し test でも同じ定義。リーク低。
- guard の alpha は 0 or 1 の固定値 (grid search なし) → OOF 過学習なし。
