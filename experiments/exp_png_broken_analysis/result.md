# PF 破損 Well PNG 目視分析結果

## 実験目的

PF (Particle Filter exp022) で pf_rmse > 20 となった TOP 5 broken wells と、pf_rmse < 3 の成功 2 wells を PNG で目視し、失敗パターンを特定する。

---

## Broken 5 Wells (pf_rmse > 20) 観察

| well_id    | pf_rmse | 主観察項目 |
|------------|---------|-----------|
| 86454a6f   | 56.34   | 曲がった軌道 + ノイズ多い GR. 複数 formation crossing で tracking 不安定. TVT matching が破綻. |
| efe96181   | 55.46   | 激しい GR ノイズ + 複雑な軌道. sequence matching が失われ、層推定の連続性が破綻. |
| 1b1eba53   | 53.54   | **非常に高い偏向角** (ほぼ水平井戸). 測深値と垂直深度の対応がズレ、層推定が局所化. |
| 91b301ce   | 47.10   | 激しい GR スパイク + 複雑な軌道. 層推跡が多点で失敗、target層で grossly misaligned. |
| 708caea9   | 44.84   | 高周波 GR ノイズ + formation crossing 多数. 観測尤度の低下で粒子収束失敗. |

---

## 成功 2 Wells (pf_rmse < 3) との比較

| well_id  | pf_rmse | 特徴 |
|----------|---------|------|
| 42c538a1 | 0.584   | クリーン GR + 中程度偏向. formation lines が明確に分離. TVT matching が tight に成立. |
| ed6436d6 | 0.670   | シャープな GR profile + 均等な formation 分布. 層間対応が uniform で robust. |

### 成功/失敗の差異分析

- **GR quality**: 成功例は ノイズ少なく明確なピーク. 失敗例は 高周波ノイズ or スパイク.
- **Well deviation**: 成功例は 中程度偏向 (formation lines が平均的に分布). 失敗例は 高偏向角 or 複雑な軌道.
- **Formation crossing**: 成功例は 明確で分離. 失敗例は 多数 + 密集で層推跡困難.
- **TVT matching**: 成功例は 赤/黒が tight. 失敗例は ズレ or段状 misalignment.

---

## PF が失敗する共通パターン (地質学的仮説)

### 1. GR ノイズ + 偏向による観測不確実性

Broken wells に共通: 高周波 GR ノイズ or スパイク. 特に高偏向角の井戸では formation crossing が密集し、観測尤度が低下. PF粒子が正しいモードに収束できず、likelihoods が均等化して粒子退化.

### 2. 測深値-垂直深度マップの歪み

非常に高い偏向角 (>60°) では、測深値 (MD) と垂直深度 (TVD) の対応が複雑になり、formation boundary の timing が大きくズレる. PF の時系列予測モデルがこのズレを追跡できず、systematic bias 蓄積.

### 3. Formation Crossing の多さ

Broken well (e.g., efe96181, 708caea9) では formation lines が複数個所で交差/平行. これにより GR value が繰り返され、層の unique signature が失われ、matching ambiguity が増加.

---

## 改善提案

1. **Pre-filter**: GR スパイク検出 + ノイズ除去 (median filter or wavelet denoising)
2. **Deviation-aware likelihood**: 高偏向井戸では GR matching weight を低下させ、MD-TVD calibration を強化
3. **Ensemble layers**: 単一 GR sequence matching ではなく、formation geometry constraints を加える

---

## 出力ファイル

- `per_well_observations.csv`: well_id, pf_rmse, category, observation
- `result.md`: 本レポート
