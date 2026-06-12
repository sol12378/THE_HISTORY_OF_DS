# exp084 Phase A2 — fork(7.625) + exp026(PF×geom) 直交blend

## 目的
新best base = sp45-fleongg fork (LB 7.625) に、誤差が部分直交(corr 0.611)な
自前 exp026 (PF×geom, LB 8.672) を注入し、LB 7.0-7.2 を狙う。

## blend設計
- `final = 0.70 * fork + 0.30 * exp026` (id単位)
- subprocess分離: fork → exp026 を順に走らせ、各 /kaggle/working/submission.csv を
  直後に fork_submission.csv / exp026_submission.csv へ copy してから blend。
  → 同名出力の上書き衝突を回避（rogii_phaseA2.py run_subprocess L96-106）。
- 最終 blend を /kaggle/working/submission.csv に書く＝スコア対象。

## blend重みの理論裏付け (2026-06-12)
2モデル最適混合: w1* = (σ2² - ρσ1σ2)/(σ1²+σ2²-2ρσ1σ2)
fork σ1≈7.6, exp026 σ2≈8.67, ρ=0.611 → w_fork*=0.667 / w_exp026*=0.333。
設定 0.70/0.30 はほぼ理論最適。

## ローカル検証結果 (2026-06-12)
local_verify.py を実行。**fork はローカル実行不可**（`from koolbox import Trainer`
= Kaggle dataset `koolbox-offline` 依存）。よって full-blend のローカル検証は構造的に不可能。
検証できたのは exp026 半分のみ:
- exp026 subprocess: rc=0, 175s, 14,151 rows, NaN=0
- 3 test well の anchor近接: 000d7d20 -2.9ft / 00bbac68 -1.5ft / 00e12e8b +1.8ft（全て<5ft, 健全）

## 修正履歴 (2026-06-12)
- 依存パス修正: `exp072_proj/_decoded_exp026_b64.py`（build中断で未生成・不在）
  → 実体 `kaggle_notebooks/exp026_pf_geom_blend/rogii_exp026_pf_geom_blend.py` に差し替え
  （rogii_phaseA2.py と local_verify.py の両方）。

## 検証ステータス
- exp026半分: PASS（ローカル）
- fork半分 + blend: Kaggle上でのみ検証可能（koolbox依存）。kernelロジックは精査済みで健全。

## 次アクション
1. **Kaggle kernel submit が必要**（ユーザー許可待ち）。ローカルでは fork を回せないため、
   blend全体の最終確認は Kaggle 実行が唯一の手段。
2. submit後: LB着地を確認し、7.625 から改善したか / CV-LB gap を較正。
3. 改善時: 採用済み gated PF smoother (exp081, -0.19) を次にこの base へ統合 (Phase B)。
4. 重み感度: 7.625 base が動いた場合 0.25/0.35 の微調整も候補。
