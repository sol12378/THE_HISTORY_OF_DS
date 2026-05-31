# exp009_typewell_gr_alignment

## 結果

| metric | 値 |
|---|---|
| **exp009 CV RMSE** | **13.922291** |
| exp008 baseline | 13.808621 |
| vs exp008 | **-0.113670 (悪化)** |
| vs exp007 | -0.055237 (悪化) |

### Fold 別 RMSE

| fold | rmse | best_iter |
|---|---:|---:|
| 0 | 13.219689 | 960 |
| 1 | 13.846692 | 261 |
| 2 | 13.953974 | 568 |
| 3 | 14.075130 | 580 |
| 4 | 14.486926 | 789 |

## 分析：なぜ悪化したか

### Group E_well 特徴量（per-well）は有効

| feature | rank | gain |
|---|---:|---:|
| tw_gr_scale | #11 | 193M |
| tw_gr_offset | #13 | 168M |
| tw_gr_last20_diff | #17 | 148M |
| tw_known_gr_corr | #20 | 130M |
| tw_gr_abs_slope_at_anchor | #21 | 121M |
| tw_gr_slope_at_anchor | #32 | 102M |

合計 gain = 862M → per-well typewell 特徴量は地質コンテキストとして機能している。

### Group E_row 特徴量（per-row）がノイズ

| feature | rank | gain |
|---|---:|---:|
| tw_gr_at_anchor | #33 | 102M （per-well定数なので実質per-well） |
| tw_tvt_correction | #51 | 0.5M ← **ほぼゼロ** |
| tw_tvt_correction_reliable | #49 | 0.8M |
| gr_dev_from_tw_anchor | #50 | 0.6M |

### tw_tvt_correction が失敗した根本的理由

```
target TVT 変化量（median）: 26 TVT units
GR 標準偏差（typical）: 20 API units

tw_tvt_correction = -gr_dev / slope

slope が小さいとき（例: -0.25 GR/TVT）:
  correction = GR_dev / 0.25 → GR ノイズを 4× 増幅！

実際の範囲:
  000d7d20: correction ∈ [-26, +10] vs true_delta ∈ [-12.5, +2.7]
  727a3a10: correction ∈ [-128, +170] vs true_delta ∈ [-18.5, +0.0] ← 大暴走！

correction と true_delta の相関:
  000d7d20: 0.35（唯一の有望ケース）
  0390d174: 0.07
  727a3a10: 0.08
```

**結論**: target TVT 変化 (~26 TVT units) << GR ノイズを slope で割った誤差 (~80 TVT units)。
点単位での GR→TVT 補正は成立しない。

### tw_known_gr_corr 別の改善/悪化

| corr_bin | n | avg_r8 | avg_r9 | avg_d | pct_better |
|---|---:|---:|---:|---:|---:|
| <0.6 | 34 | 11.34 | 12.03 | +0.70 | 38% |
| 0.6-0.75 | 153 | 11.55 | 11.92 | +0.38 | 42% |
| 0.75-0.85 | 343 | 10.88 | 10.90 | +0.02 | 48% |
| **>0.85** | **243** | **11.19** | **11.10** | **-0.09** | **54%** |

→ 高相関 well (>0.85) では typewell 特徴量は有効！低相関 well で足を引っ張っている。

## 実験系列の進捗

```
exp007:  13.867054  (trajectory A+B+C)
exp008:  13.808621  (+ GR rolling D)
exp009:  13.922291  (+ typewell E)  ← 悪化
```

## 根本的な設計上の誤り

今回の `tw_tvt_correction` は「点単位の GR 値」から TVT を推定しようとした。
しかし正しいアプローチは「GR の系列パターン」を typewell と比較すること。

**正しい方向（次の実験）:**
1. per-well E features のみ残す → exp009b（即効性あり）
2. 系列ベースの GR alignment（cross-correlation） → exp010
   - known区間の GR 系列と typewell GR 系列の cross-correlation で shift を求める
   - target 区間でこの shift を TVT 補正に適用
   - これが本来の well-to-well GR 相関手法

## 次アクション

1. **exp009b**: per-row E features を除去し per-well E features のみで再学習
   - 期待: exp008 以上、悪化なし
2. **exp009c (または exp010)**: GR 系列 cross-correlation でシフト量を計算
   - 既知区間 GR × typewell GR の 1D cross-correlation → shift_tvt per well
   - 期待: +0.3〜+1.0 RMSE 改善
