# exp016_struct_plane

## 目的
exp014 (CV=13.525189) に Group G（3D構造平面外挿）を追加。
TVT≈傾斜地層の平面 → known区間で TVT~X,Y,Z を較正し、既知hidden座標へ適用。
Group F の縦成分(dTVT/dZ)を横方向dip込みに一般化。

## 結果
| metric | 値 |
|---|---|
| **exp016 CV RMSE** | **13.887794** |
| exp014 baseline | 13.525189 |
| vs exp014 | -0.362605 |
| vs exp008 | -0.079173 |

## Fold 別
| fold | rmse | best_iter |
|---|---:|---:|
| 0 | 13.354886 | 146 |
| 1 | 13.956245 | 143 |
| 2 | 13.939412 | 110 |
| 3 | 13.778537 | 864 |
| 4 | 14.390976 | 543 |

## Group G のランク
| feature | gain | 全体順位 |
|---|---:|---:|
| g_plane_local_delta | 210,023,515 | #5 |
| g_plane_choriz | 164,042,750 | #12 |
| g_plane_full_delta | 156,052,458 | #15 |
| g_plane_cz | 145,020,210 | #16 |
| g_plane_local_r2 | 119,394,061 | #21 |
| g_plane_full_r2 | 92,250,725 | #32 |
| g_plane_disagree | 62,482,222 | #43 |

## リーク防止
- 平面較正は is_known_tvt==True 行のみ ✅ / hidden X/Y/Z は観測量 ✅ / hidden TVT不使用 ✅
- fold は exp008/014 と同一 ✅ / delta は ±200 clip ✅
