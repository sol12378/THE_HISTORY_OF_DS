# exp021_beam_track — Beam Search GR-typewell トラッカー

## 手法
参照ノートの beam_search を忠実移植(DTW型)。typewell index を1行±2ステップ動かし
cost=GR誤差²/es + 移動コスト の累積最小経路を bs本ビームで探索。14 config平均。
GRは well全体を補間してから使用。**完全leak-free**(hidden TVT不使用)。

## 結果(773-well pooled CV)
| 手法 | CV RMSE |
|---|---|
| anchor | 15.909853 |
| **beam (faithful)** | **15.697192** |
| beam (+offset較正) | 15.752609 |
| 参考: exp014 geom | 13.525189 |
| 参考: best blend(exp020) | 13.320964 |

beam が anchor に勝つ well: 432/773

## 3 test well (beam vs train真値, 参照の"4.71 ft"主張と照合)
| well | RMSE |
|---|---|
| 000d7d20 | 8.3779 |
| 00bbac68 | 14.7780 |
| 00e12e8b | 8.4932 |

## 解釈
- **Beamはanchor(15.91)とほぼ同等(15.70)で実質失敗**。offset較正版も15.75で改善せず。
- 原因: typewell index を1行±2ステップに制限する運動モデルが粗く、長距離hiddenで累積誤差・迷子。
  GR誤差コストだけでは多価性を解ききれず、決定論的ビームは一度ずれると復帰しにくい。
- 3 test well: 8.38/14.78/8.49 → 2/3でanchorに負け。
- 対照的に Particle Filter(exp022)は同じGR-typewell情報で CV 11.02・3test平均≈5.0 と大きく勝つ。
  違い=PFは(1)連続値状態 pos=TVT+Z でZ既知分を分離、(2)滑らかなrate運動+雑音、
  (3)128 seed尤度加重アンサンブルで曖昧性を確率的に統合。**ハードビームより確率的トラッカーが優位**。

## リンク
[[exp022_particle_filter]] [[exp023_leak_lookup]] [[exp014_geom_extrap]]
