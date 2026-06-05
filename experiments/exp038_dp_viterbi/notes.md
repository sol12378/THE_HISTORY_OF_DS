# exp038_dp_viterbi — DP/Viterbi TVT トラッカー

## 手法
離散状態空間の動的計画法(Viterbi)。状態 = TVT_bin(50個の離散化状態, TVT ±50ft from anchor)。
- **遷移コスト**: dTVT の先験(tail-30から推定)からのガウス偏差ペナルティ(sigma=1.0ft)
- **観測コスト**: 各(TVT_bin, MD step)でのGR尤度 vs typewell GR補間値
- **最適経路**: Viterbi アルゴリズムで全探索→グローバル最適

PF(exp022)との相補性: PF=確率的局所探索, Viterbi=離散全探索。低相関ならblend価値あり。

## 結果(773-well pooled CV)
| 手法 | CV RMSE |
|---|---|
| anchor | 15.909853 |
| **Viterbi** | **16.615025** |
| 参考: exp022 PF | 11.02 |
| 参考: exp014 geom | 13.525189 |

Viterbi が anchor に勝つ well: 394/773
Broken wells (RMSE>20): 141

## 3 test well (Viterbi vs train真値)
| well | RMSE |
|---|---|
| 000d7d20 | 7.4006 |
| 00bbac68 | 22.3933 |
| 00e12e8b | 15.2403 |

## リンク
[[exp022_particle_filter]] [[exp014_geom_extrap]]
