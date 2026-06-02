# exp022_particle_filter — Particle Filter GR-typewell トラッカー

## 手法
参照の run_particle_filter を忠実移植。状態 pos=TVT+Z をMD沿いに滑らか伝播、
観測GR vs typewell GR(pos-Z) の尤度で粒子再重み付け。128 seed × 500 粒子, 尤度加重(scale=8.0)。
GRは well全体を補間。**完全leak-free**。well単位ProcessPoolExecutor並列。

## 結果(773-well pooled CV)
| 手法 | CV RMSE |
|---|---|
| anchor | 15.909853 |
| **PF** | **11.024014** |
| 参考: exp014 geom | 13.525189 |
| 参考: best blend(exp020) | 13.320964 |

PF が anchor に勝つ well: 587/773。per-well RMSE 中央値5.66/平均7.97。47 well壊れ(>20)。

## 3 test well (PF vs train真値, 参照"4.71 ft"と照合)
| well | RMSE |
|---|---|
| 000d7d20 | 3.9871 |
| 00bbac68 | 4.4426 |
| 00e12e8b | 6.5151 |

3 well平均≈5.0 → **参照の"local 4.71 ft"を再現**。参照のLB 6.8は(リークではなく)このPFトラッキング由来と判明。

## 解釈（重要・並行作業の結論を覆す）
- **PF pooled CV 11.02 は全手法の最良**（geom 13.53 / blend 13.32 / anchor 15.91 を凌駕）。完全leak-free。
- 並行作業(exp017 GR特徴量/exp019 系列NN/exp020 微分可能DTW)は GR照合を「全形態NO-GO・CV~5到達不可」と
  結論したが、それらは**学習的/ソフト/グローバル**モデル。PFは**well単位の確率的ハードトラッカー**で、
  各wellが自分のtypewellを直接利用するため根本的に強い。→「到達不可」は誤り、未検証の形態が勝った。
- なぜPF>Beam: 連続状態 pos=TVT+Z(Z既知分を分離)、滑らかなrate運動+雑音、128 seed尤度加重で
  多価GRの曖昧性を確率的に統合。決定論ビームの±2制約より柔軟で迷子復帰も可能。

## ブレンド余地（次の本線）
- PFとgeom(exp014)の誤差相関0.426と低い → 強力ブレンド。
- **0.6·PF + 0.4·geom + well内mean平滑(w101) = CV 10.16**（前best 13.32から +3.16、全fold一貫 9.49〜11.07）。
- 残課題: 47壊れwellのreliabilityゲート(PF log-lik等)、tree/NN ensembleとの3way blend、PFパラメータ調整。

## リンク
[[exp021_beam_track]] [[exp023_leak_lookup]] [[exp014_geom_extrap]]
