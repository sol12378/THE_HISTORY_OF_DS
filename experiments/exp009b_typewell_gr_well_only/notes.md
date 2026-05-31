# exp009b_typewell_gr_well_only

## 目的

exp009 (CV=13.922291) の失敗原因を修正: per-row GR 補正特徴量を全削除し、
per-well Typewell GR 特徴量のみを残す。

## 変更点（exp009 との差分）

| 削除した特徴量 | 削除理由 |
|---|---|
| gr_dev_from_tw_anchor | ノイズの入力値 (importance: 0.6M) |
| tw_tvt_correction | -gr_dev/slope → ノイズ増幅 σ≈80 TVT (0.5M) |
| tw_tvt_correction_reliable | 同上のマスク版 (0.8M) |
| tw_gr_extrap_range | 不要な補助特徴量 |

## 残した Group E 特徴量

| 特徴量 | grain | 定義 |
|---|---|---|
| tw_known_gr_corr | per-well | known区間 GR と typewell GR の相関 |
| tw_gr_offset | per-well | GR の系統的ずれ |
| tw_gr_scale | per-well | GR スケール差 |
| tw_gr_last20_diff | per-well | PS近傍の GR-typewell 乖離 |
| tw_gr_slope_at_anchor | per-well | dGR/dTVT at last_known_TVT |
| tw_gr_abs_slope_at_anchor | per-well | ｜dGR/dTVT｜ |
| tw_gr_at_anchor | per-row定数 | typewell GR at last_known_TVT |

## 結果

| metric | 値 |
|---|---|
| **exp009b CV RMSE** | **13.932155** |
| exp008 baseline | 13.808621 |
| exp009 (failed) | 13.922291 |
| vs exp008 | -0.123534 |
| vs exp009 | -0.009864 |

## Fold 別 RMSE

| fold | rmse | best_iter |
|---|---:|---:|
| 0 | 13.139644 | 631 |
| 1 | 13.968885 | 269 |
| 2 | 13.971968 | 408 |
| 3 | 13.940404 | 735 |
| 4 | 14.602585 | 1284 |

## Top 15 Feature Importance (gain)

| feature | importance_gain |
|---|---:|
| dZ_dMD_from_ps | 706,361,572 |
| last_known_Y | 326,698,811 |
| pre_ps_dZ_dMD | 292,053,652 |
| pre_ps_tvt_curvature | 258,652,540 |
| delta_X_from_PS | 256,154,447 |
| delta_Z_from_PS | 245,718,737 |
| known_length | 241,817,520 |
| Y | 241,816,030 |
| X | 237,926,107 |
| pre_ps_tvt_slope_last20 | 229,791,683 |
| pre_ps_tvt_slope_last5 | 191,599,199 |
| tw_gr_scale | 180,731,778 |
| tw_gr_offset | 160,852,558 |
| tw_gr_last20_diff | 160,129,411 |
| n_rows_in_well | 158,092,003 |

## Group E 特徴量の重要度

| feature | importance_gain |
|---|---:|
| tw_gr_scale | 180,731,778 |
| tw_gr_offset | 160,852,558 |
| tw_gr_last20_diff | 160,129,411 |
| tw_gr_abs_slope_at_anchor | 123,991,003 |
| tw_known_gr_corr | 118,179,233 |
| tw_gr_slope_at_anchor | 107,808,636 |
| tw_gr_at_anchor | 106,184,916 |

## リーク防止確認

- キャリブレーション: is_known_tvt==True 行のみ ✅
- typewell は参照曲線（別物理井戸）、ラベルではない ✅
- target GR は観測可能な物理計測値 ✅
- tw_gr_at_anchor は per-row 定数（全 row に同一値） ✅
- test: typewell_test_base_v001.parquet を使用 ✅
- per-row 補正ロジックは完全削除 ✅
