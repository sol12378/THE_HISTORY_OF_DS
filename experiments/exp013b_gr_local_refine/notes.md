# exp013b_gr_local_refine (Track 2 Phase 1 追試 / GO-NOGO確定)

## 目的

exp013 で素朴なGR照合(±110窓)が全滅。残る問い:
**狭窓 + 幾何prior中心**なら、GRは予測を局所微修正できるか?
center ∈ {anchor, exp008予測} の ±w窓(w=10/20/30)でGR照合し、
center に最も近い解を採用。blend も評価。完全leak-free。

## 結果（全target行 RMSE、抜粋）

| method | RMSE | vs exp008 |
|---|---:|---:|
| **exp008 (参照)** | **13.808621** | — (BEST) |
| blend_exp008_w10_bw0.3 | 13.825925 | +0.017 |
| matchE_exp008_w10_smooth | 13.905225 | +0.097 |
| blend_exp008_w10_bw0.5 | 13.916275 | +0.108 |
| matchA_exp008_w10 (純match) | 14.407844 | +0.599 |
| anchor | 15.909853 | +2.101 |
| matchA_anchor_w10 | 16.414182 | +2.606 |
| matchA_anchor_w30 | 18.771290 | +4.963 |

## 判定: **NO-GO（GR-typewell 直接照合）**

- **どのGR変種も exp008 を超えない。** 最善でも +0.017 悪化（しかもほぼexp008そのもの bw=0.3）。
- 純GR照合(bw=1.0)は ±10窓でも +0.6〜+2.6 悪化。窓を広げるほど悪化。
- center を anchor にすると全て anchor 以下（GRが anchor すら改善しない）。
- center を exp008 にしても、GR照合へ動かすほど悪化 → **GRは強prior上で一切上乗せ情報を持たない**。

### なぜ効かないか

1. GR↔TVT が多価。±10 TVT という極狭窓でも同一GRを与える点が複数あり逆変換が不安定。
2. exp008 の Group D（GR rolling統計を LGBM特徴量化）が、この表現で取り出せるGR信号を
   既に取り切っている。明示的な点照合は冗長かつノイズ追加。
3. anchor / 幾何予測が既に強く（hidden TVTの中央値deltaは0.84）、点照合の誤差がそれを上回る。

## Tier 2 投資判断への含意

「GR-typewellアライメント = 本丸（LB6.8への梃子）」仮説は、
**pointwise/windowed matching の範囲では棄却**。
exp009(特徴量化)・exp013(直接照合・広窓)・exp013b(局所微修正)が全て失敗で一貫。
→ Tier 2 で GRアライメントへ大きく投資すべきではない。投資は別軸へ振り替える。

唯一未検証の残路: hidden GR系列全体 vs typewell GR系列の**DTW系列アライメント**
（形状ベース、点ではなくパターン照合）。ただし本結果の一貫した負信号を踏まえると高リスク。
