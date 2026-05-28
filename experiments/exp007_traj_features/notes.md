# exp007_traj_features

## 目的

exp003 (LightGBM baseline, CV=15.054865) に Groups A+B+C 特徴量を追加し、TVT予測精度を改善する。

## 変更内容

- **Group A (Pre-PS TVT momentum)**: pre_ps_tvt_slope_last20, pre_ps_tvt_slope_last5, pre_ps_tvt_curvature, pre_ps_tvt_delta_last20
- **Group B pre-PS**: pre_ps_dZ_dMD, pre_ps_dX_dMD, pre_ps_dY_dMD, pre_ps_horiz_dMD, pre_ps_azimuth
- **Group B per-row**: dZ_dMD_from_ps, dX_dMD_from_ps, dY_dMD_from_ps, horiz_disp_from_ps, azimuth_from_ps
- **Group C**: kh_ratio (known/hidden), hidden_frac (hidden/total rows)
- LightGBMハイパーパラメータは exp003 と同一

## 結果

| metric | value |
|---|---|
| overall CV RMSE | 13.867054 |
| exp003 baseline | 15.054865 |
| 改善幅 | +1.187811 |
| fold mean | 13.859021 |
| fold std | 0.478188 |

## Fold別RMSE

| fold | rmse | best_iteration |
| --- | --- | --- |
| 0 | 13.061989 | 458 |
| 1 | 13.98059 | 270 |
| 2 | 13.618236 | 180 |
| 3 | 14.228974 | 514 |
| 4 | 14.405314 | 600 |

## Top 20 Feature Importance (gain)

| feature | importance_gain |
| --- | --- |
| dZ_dMD_from_ps | 796716151 |
| last_known_Y | 367127851 |
| known_length | 354416335 |
| pre_ps_dZ_dMD | 344378576 |
| pre_ps_tvt_curvature | 337736128 |
| Y | 304283556 |
| X | 299494122 |
| pre_ps_tvt_slope_last20 | 281918352 |
| delta_X_from_PS | 256582884 |
| delta_Z_from_PS | 252505507 |
| pre_ps_tvt_slope_last5 | 243708722 |
| n_rows_in_well | 228969567 |
| pre_ps_horiz_dMD | 199528048 |
| last_known_MD | 197121827 |
| Z | 196779133 |
| last_known_TVT | 191309651 |
| last_known_X | 165234151 |
| pre_ps_dY_dMD | 150081257 |
| pre_ps_dX_dMD | 146672099 |
| last_known_Z | 146349771 |

## リーク懸念

- Group A は is_known_tvt 行の TVT_input を使う。train/testで観測済みデータ（PSより前）のみ使用。リーク低。
- Group B pre-PS は is_known_tvt 行のX/Y/Z座標から方向を計算。PSより前のデータのみ。リーク低。
- Group B per-row は delta_*_from_PS 列から計算。既存列と同等リスク（低〜中）。
- Group C は既存の known_length/hidden_length から計算。リーク低。
