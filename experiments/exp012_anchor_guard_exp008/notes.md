# exp012_anchor_guard_exp008 (Track 1)

## 目的

best model exp008 (CV=13.808621) に exp006 流の一方向 anchor guard を後処理適用し、
長尺・下降 well で anchor に救われる余地が強モデルでもまだ残るかを検証する。
exp007b では双方向guardが逆効果だったため、本実験は閾値も exp008 OOF 上で再 sweep する。

## 手法

- guard 特徴量: `hidden_length`, `final_delta_z`(=delta_Z_from_PS最終行), `mean_pred_delta`
  （いずれも test で計算可能、leak-free）
- ルール: full_anchor / delta_extreme / strong_guard / mild_guard / no_guard
- `pred = α·exp008 + (1-α)·anchor`
- 閾値とαを OOF 上で粗グリッド sweep（full_hidden×delta_extreme×α_strong×α_mild）

## 結果

| metric | 値 |
|---|---|
| exp008 OOF RMSE | 13.808621 |
| anchor OOF RMSE | 15.909853 |
| **blended CV RMSE** | **13.754461** |
| improvement vs exp008 | **+0.054160** |

best config: full_anchor=無効, delta_extreme_thr=50, α_strong=0.85, α_mild=0.5

### per-rule 内訳

| rule | wells | α | blend | lgb | anchor |
|---|---:|---:|---:|---:|---:|
| strong_guard | 239 | 0.85 | 13.5228 | 13.6420 | 15.6579 |
| mild_guard | 15 | 0.50 | 25.6838 | 26.0677 | 26.3726 |
| no_guard | 519 | 1.00 | 13.3495 | 13.3495 | 15.6166 |

- strong_guard (final_delta_z<-100 & hidden>4000) で anchor を15%混ぜると改善。
  下降長尺 well で exp008 が僅かに overshoot するのを anchor が補正。
- full_anchor は exp008 では無効化が最適（強モデルは長尺でも anchor より良い）。
- anchor が勝つ well: 495/773（うち+5以上 166）だが、多くは僅差で blend は控えめ。

## test への影響

test 3 wells は全て no_guard（hidden<4000 かつ delta穏当）→ **公開LB変わらず**。
本改善は CV(773 wells)/private 向けの底上げ。

## リーク懸念・注意

- guard 条件は base table の test 計算可能特徴量のみ。leak-free。
- ただし閾値+αを OOF 上で sweep（864通り）して best を選んでいるため、
  +0.054 は OOF への軽い過学習を含む可能性。fold std=0.47 に対し小さい改善。
  → 本命の天井上げではなく「安価な保険」と位置づける。
