# exp008_gr_rolling

## 目的

exp007b (CV=13.853360) に Group D (GR rolling 特徴量) を追加し、
GRの文脈情報が TVT 予測に貢献するかを検証する。

## 追加特徴量

### Group D_well（per-well、既知区間から算出）

| 特徴量 | 定義 |
|---|---|
| pre_ps_gr_mean | known行 GR 平均 |
| pre_ps_gr_std | known行 GR 標準偏差 |
| pre_ps_gr_last20_mean | known末尾20行 GR 平均 |
| pre_ps_gr_trend | known行全体の GR 変化率 |
| pre_ps_gr_available_frac | known行の GR 有効割合 |

### Group D_row（per-row、因果ローリング）

| 特徴量 | 定義 |
|---|---|
| gr_vs_pre_ps_mean | GR - pre_ps_gr_mean |
| gr_z_score | (GR - mean) / std |
| gr_rolling_mean_w20 | 後ろ向き rolling mean (w=20) |
| gr_rolling_mean_w50 | 後ろ向き rolling mean (w=50) |
| gr_rolling_std_w20 | 後ろ向き rolling std (w=20) |

## リーク防止

- pre-PS 統計は is_known_tvt==True 行のみから計算
- rolling は center=False（後ろ向きのみ）
- 欠損補完: pre_ps_gr_mean → GLOBAL_GR_MEAN=87.7524（train のみから計算した定数）
- TVT・TVT_input は一切使用しない

## 結果

| metric | 値 |
|---|---|
| exp008 CV RMSE | **13.808621** |
| exp007b baseline | 13.853360 |
| vs exp007b | +0.044739 |
| vs exp007 | +0.058433 |

## Fold 別 RMSE

| fold | rmse | best_iter |
|---|---:|---:|
| 0 | 13.039683 | 286 |
| 1 | 14.041555 | 241 |
| 2 | 13.534087 | 255 |
| 3 | 13.962596 | 286 |
| 4 | 14.425618 | 839 |

## Top 10 Feature Importance (gain)

| feature | importance_gain |
|---|---:|
| dZ_dMD_from_ps | 765,916,056 |
| last_known_Y | 364,712,991 |
| pre_ps_dZ_dMD | 334,666,616 |
| pre_ps_tvt_curvature | 287,669,985 |
| known_length | 280,436,828 |
| Y | 263,719,054 |
| X | 258,325,314 |
| delta_X_from_PS | 248,273,183 |
| delta_Z_from_PS | 229,807,018 |
| pre_ps_tvt_slope_last20 | 229,689,877 |
