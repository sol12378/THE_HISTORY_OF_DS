# exp084 Phase A2 — fork(7.625) + exp026(PF×geom) 直交blend

## 目的
新best base = sp45-fleongg fork (LB 7.625) に、誤差が部分直交(corr 0.611)な
自前 exp026 (PF×geom, LB 8.672) を注入し、LB 7.0-7.2 を狙う。

## blend設計 (v2: 2026-06-12 再設計)
- `final = 0.70 * fork + 0.30 * exp026` (id単位)
- **v1のsubprocess分離方式は失敗** (Kaggle ERROR): Kaggleはkernelにcode_file 1本しか
  アップロードしないため、subprocessで呼ぶ兄弟スクリプト(fork/exp026)が存在せず FileNotFoundError。
- **v2方式 = fork出力をkernel_sources取り込み + exp026 inline実行**:
  - kernel-metadata: `kernel_sources=["sol12378/rogii-sp45-fleongg-fork"]`
    → fork submission(実績LB 7.625)が /kaggle/input/rogii-sp45-fleongg-fork/submission.csv にマウント
  - code_file = exp026本体(自己完結, koolbox不要)をverbatim取り込み、出力名を exp026_submission.csv に変更
  - epilogue: forkとexp026をid単位 outer-merge → 0.70/0.30 blend → /kaggle/working/submission.csv
  - fork不在時(ローカル等)は exp026単独にfallback
  - dataset_sources は空に(koolbox/fleongg/ravaghiはfork専用、exp026はraw dataのみ)
  - 利点: 7.625を出した「正確なfork submission」と直接blendでき、fork再実行リスクなし

## blend重みの理論裏付け (2026-06-12)
2モデル最適混合: w1* = (σ2² - ρσ1σ2)/(σ1²+σ2²-2ρσ1σ2)
fork σ1≈7.6, exp026 σ2≈8.67, ρ=0.611 → w_fork*=0.667 / w_exp026*=0.333。
設定 0.70/0.30 はほぼ理論最適。

## ローカル検証結果 (2026-06-12)
**fork はローカル実行不可**（`from koolbox import Trainer` = Kaggle dataset 依存）。
よって full-blend のローカル検証は構造的に不可能。検証できたのは exp026 半分のみ:
- exp026 subprocess: rc=0, 175s, 14,151 rows, NaN=0
- 3 test well の anchor近接: 000d7d20 -2.9ft / 00bbac68 -1.5ft / 00e12e8b +1.8ft（全て<5ft, 健全）
- v2 combined kernel ローカルsmoke: compile OK + exp026完走 + fork不在fallback正常動作を確認

## Kaggle提出ログ (2026-06-12)
- v1 (subprocess方式): version 1 push → **ERROR** (FileNotFoundError: 兄弟script不在)
- v2 (kernel_sources+inline方式): version 2 push → 実行中。完了後にcommit & submit。

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
