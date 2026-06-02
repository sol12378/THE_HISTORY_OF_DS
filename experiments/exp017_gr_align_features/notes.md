# exp017 — GR-typewell系列照合 特徴量化（Group H）最終GR実験

## 目的
ユーザー指示「GR typewellが鍵、CV<=5を達成せよ」を受け、GR-typewell照合を
**学習モデルに特徴量化して投入する最後の現実的形**で定量評価する。
評価は exp011 leak を避けるため **typewell-grouped fold** で実施。

## 前段の oracle 診断（scripts/diag_*.py, experiments/diag_gr_ceiling/）
| 指標 | RMSE | 意味 |
|---|---:|---|
| anchor | 15.91 | 基準 |
| geom (exp014) | 13.53 | 現行幾何prior |
| **glob_oracle** (1 offset/well, 真値選択) | **8.21** | geom形状+理想offsetの上限 |
| **seg_oracle** (4 offset/well, 真値選択) | **4.39** | 同, 区分offset |
| corr(GR選択offset, 真offset) | **+0.155** | GRのoffset信号は極めて弱い |

→ 「geom形状は正しく、残差は低周波offset。理想offsetを当てれば CV<=5 可能。
   だがGRはそのoffsetを当てられない」。

## 本実験 結果（typewell-grouped fold）
| feature set | CV |
|---|---:|
| base = exp014全特徴 | 13.762346 |
| base + Group H (GR alignment) | 13.829807 |
| **Group H 寄与** | **-0.067（悪化）** |

Group H importance 順位: h_cal_b #16, h_align_gain #22, h_cal_a #25, h_tw_corr #29,
h_align_offset #43, h_gr_resid_at_geom #55, h_local_offset #60（いずれも下位）。

### Fold別（base / base+H）
- f0 12.993 / 12.933, f1 13.635 / 13.348, f2 13.373 / 13.454,
  f3 13.968 / 14.142, f4 14.681 / 15.031
- f1で改善するがf3/f4で悪化。leak-safe foldでは正味マイナス＝overfit兆候。

## 結論
GR-typewell照合は、**oracleで上限まで定量化しても CV<=5 には届かず**
（geom形状+理想offsetの1param上限ですら 8.2）、かつ
**学習特徴量化しても leak-safe fold で悪化(-0.067)**。
exp009/011/013/013b に続き、GR照合は全形態でNO-GO。
→ **CV<=5 は GR を含む正規手段では到達不可能**。LB首位でも6.8。

## リーク防止
- typewell-grouped fold (folds_group_typewell_v001.csv) ✅
- Group H は 観測GR + typewell + 幾何center(last_known_TVT+f_extrap_quad_dMD) のみ。hidden TVT不使用 ✅
- 同fold上で base と base+H を学習しHの寄与を切り出し ✅

## 次アクション（現実的）
1. 現行best維持: exp015 (well-fold CV 13.520)。
2. 真の改善余地はモデル多様化(XGB/CatBoost blend) — Tier2優先A。期待 ~0.1-0.3。
3. geom形状が良い事実を活かす: known区間の自己ホールドアウトでoffset bias自己較正を検討（leak-free）。
