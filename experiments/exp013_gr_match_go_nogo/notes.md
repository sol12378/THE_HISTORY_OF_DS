# exp013_gr_match_go_nogo (Track 2 Phase 1)

## 目的

戦略の核心仮説の検証: hidden行の観測GRを typewell GR-TVTプロファイルに照合し
TVTを直接復元すれば、anchor(15.91)を超え exp008(13.81)に匹敵するか?
匹敵すれば本丸 Approach C へGO、ダメなら設計見直し or NO-GO。

**完全leak-free**: 推定にラベルTVT不使用。観測GR + typewell参照 + anchor のみ。
→ fold/学習不要、全773 wellsで直接RMSE測定。

## 手法

各wellで typewell GR(TVT) を構築。known区間で gr_offset 較正。
anchor±110窓の TVTグリッド(0.5刻み)から |tw_GR(tvt) - (obs_GR - offset)| 最小のTVTを探索。
- variantA: 窓内 nearest GR match（global argmin）
- variantB: 系列連続性ペナルティ付き greedy（λ=0.15）
- variantA_smooth: variantA を rolling median(25) 平滑

## 結果（全target行 RMSE）

| method | RMSE |
|---|---:|
| anchor | 15.909853 |
| **exp008 (参照)** | **13.808621** |
| variantA_nearest | 43.08 |
| variantA_smooth | 24.16 |
| variantB_sequential | 46.23 |

corr-bin別（per-well平均、>0.85帯 244 wells でも）: A≈41.5, B≈42.0 ≫ anchor 12.97。
B が anchor に勝つ well: わずか 15/773。

## 解釈

**素朴なGR直接照合は全滅。** anchorより遥かに悪い。
原因: hidden TVTのdelta実測幅±100に対し中央値0.84・std15.8で大半がanchor近傍。
typewell GRは窓内で高周波変動（std≈26）→ ±110窓内に同一GRを与えるTVTが多数存在し、
nearest-match は遠方の偽マッチを拾う。連続性ペナルティも一度誤枝に乗ると復帰せず drift。

→ 窓を狭め幾何prior中心にした追試 exp013b へ。
