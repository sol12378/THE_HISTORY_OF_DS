# exp006_anchor_guard

## 目的

exp003 LightGBM の後処理として、ルールベースの anchor guard を適用し、
「anchor が強いのに LightGBM が崩すwells」での大崩れを防ぐ。

## ガードルール

| rule | 条件 | alpha (LGB weight) |
|---|---|---|
| full_anchor | hidden_length > 8000 | 0.0 |
| delta_extreme | mean_pred_delta > 30.0 | 0.0 |
| strong_guard | final_delta_z < -100.0 AND hidden_length > 4000 | 0.7 |
| mild_guard | final_delta_z < -50.0 AND hidden_length > 4000 (strong_guard非対象) | 1.0 |
| no_guard | otherwise | 1.0 |

`pred = alpha * lgbm + (1 - alpha) * anchor`

## 結果

| metric | 値 |
|---|---|
| LightGBM CV RMSE | 15.054865 |
| Anchor CV RMSE | 15.909853 |
| Blended CV RMSE | 14.724541 |
| improvement vs LightGBM | +0.330323 |
| improvement vs Anchor | +1.185311 |

## train guard rule 分布

guard_rule
no_guard         512
strong_guard     228
mild_guard        15
full_anchor       14
delta_extreme      4

## test guard rule 分布

guard_rule
no_guard    3

## リーク懸念

guard 条件に使う `hidden_length` と `delta_Z_from_PS` は base table に存在し、
train/test 両方で同じ定義で計算できる。
alpha は train OOF 上でチューニングしているが、候補値が粗いため過学習懸念は低い。
