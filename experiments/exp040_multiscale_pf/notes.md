# exp040_multiscale_pf — Multi-scale Temperature Particle Filter

## 手法
exp022 の PF フレームワークで、1回のシミュレーションから得た per-seed (preds, log_liks) を
複数の温度スケール (3.0, 5.0, 8.0, 12.0) で再加重。
各スケールでの予測を平均化。128 seed × 500 粒子。
GRはwell全体を補間。**完全leak-free**。well単位ProcessPoolExecutor並列。

## 結果(773-well pooled CV)
| 手法 | CV RMSE |
|---|---|
| anchor | 15.909853 |
| **Multi-scale PF (exp040)** | **10.979086** |
| 参考: exp022 single-scale (SCALE=8.0) | 11.024000 |

Multi-scale PF が anchor に勝つ well: 574/773
RMSE > 20 (broken): 48

## 3 test well (Multi-scale PF vs train真値, 参照"4.71 ft"と照合)
| well | RMSE |
|---|---|
| 000d7d20 | 4.1619 |
| 00bbac68 | 4.6699 |
| 00e12e8b | 8.6345 |

## 計算時間
2155.9 秒

## リンク
[[exp022_particle_filter]] [[exp021_beam_track]] [[exp023_leak_lookup]]
