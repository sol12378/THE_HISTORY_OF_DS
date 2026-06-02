# exp014_geom_extrap

## 目的
exp008 (CV=13.808621) に Group F（幾何外挿）を追加。hidden区間でX/Y/Z/MDは既知なので、
known区間で較正した構造傾斜(dTVT/dMD, dTVT/dZ)を既知hidden幾何へ投影しTVT deltaを外挿する。

## 結果
| metric | 値 |
|---|---|
| **exp014 CV RMSE** | **13.525189** |
| exp008 baseline | 13.808621 |
| vs exp008 | +0.283432 |

## Fold 別
| fold | rmse | best_iter |
|---|---:|---:|
| 0 | 12.675700 | 700 |
| 1 | 13.578982 | 158 |
| 2 | 13.711679 | 329 |
| 3 | 13.655823 | 629 |
| 4 | 13.969219 | 872 |

## Top 15 importance
| feature | gain |
|---|---:|
| dZ_dMD_from_ps | 716,977,503 |
| last_known_Y | 312,080,585 |
| pre_ps_dZ_dMD | 300,712,947 |
| known_length | 248,165,118 |
| Y | 226,057,773 |
| X | 220,820,193 |
| f_dtvt_dz_pre | 214,776,194 |
| f_extrap_quad_dMD | 212,172,619 |
| f_dtvt_dz_r2 | 211,323,996 |
| pre_ps_tvt_curvature | 189,756,611 |
| f_extrap_slope5_dMD | 188,331,648 |
| delta_X_from_PS | 185,502,053 |
| pre_ps_tvt_slope_last20 | 175,325,117 |
| pre_ps_gr_mean | 172,250,460 |
| pre_ps_tvt_slope_last5 | 164,550,411 |

## Group F のランク
| feature | gain | 全体順位 |
|---|---:|---:|
| f_dtvt_dz_pre | 214,776,194 | #7 |
| f_extrap_quad_dMD | 212,172,619 | #8 |
| f_dtvt_dz_r2 | 211,323,996 | #9 |
| f_extrap_slope5_dMD | 188,331,648 | #11 |
| f_extrap_slope20_dMD | 106,542,903 | #30 |
| f_extrap_disagree | 98,193,165 | #32 |
| f_extrap_z | 98,051,136 | #34 |
| f_dtvt_dmd_l50 | 74,591,472 | #38 |

## リーク防止
- 構造傾斜の較正は is_known_tvt==True 行のみ ✅
- hidden の X/Y/Z/MD は観測量（予測対象はTVTのみ） ✅
- hidden の TVT は一切使わない ✅
- fold は exp008 と同一（folds_group_well_v001.csv） ✅
