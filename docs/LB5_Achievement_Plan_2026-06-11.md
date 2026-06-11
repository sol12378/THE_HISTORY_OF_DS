# LB 5台達成計画書 — 客観的根拠に基づく詳細計画

作成: 2026-06-11 / 前提: sp45-fleongg fork (推定LB ~7.4-7.5) 提出中 / 目標: **LB 5台（1位 SaintLouis 5.986 超え）**

---

## 1. 現状認識（全て出典付き）

### 1.1 LB状況
- 1位 SaintLouis **5.986** / 2位 6.228 / 3位 6.487（`docs/LB1_Roadmap_from_7.5_2026-06-10.md` L4）
- 公開手法の天井 ~**7.4-7.57**（fleongg fle3n-v4 = 7.572、`ROGII_kaggle_obsidian/05_Experiments/exp_audit_public_notebooks_2026-06-10.md`）
- LB 5台の手法は**非公開**。loop#4外部偵察で公開notebook最高は9.25級（`docs/loop_log.md` L61, L76-78）
- 我々の確定best: exp072 LB **8.280**（top ~3%、`ROGII_kaggle_obsidian/09_Submissions/LB_Tracking.md`）

### 1.2 ギャップの構造
- 7.5 → 5.986 = **約1.5 ft**。公開8 notebook監査の結論: 7.4系は全て同一系譜（lik-PF 128seed×500粒子 multi-scale{3,5,8,12} + GBM stack + projection deg4 β0.75 + selector）で、**offsetの壁を誰も解いていない**（exp_audit_public_notebooks_2026-06-10.md）。
- fleongg著者自身が「これ以上は decorrelated 3rd source が必要」と明言し7.572で停止（`docs/LB1_Strategy_2026-06-10.md` L44）。
- test=3 wells。exp022のper-well実測では3 test相当wellで 3.99 / 4.44 / 6.52 ft（平均4.98、`experiments/exp022_particle_filter/per_well.csv`）。**LB 1ftの差 ≈ 3本中1本の構造解釈の成否**。5台とは「3本中1〜2本でほぼ正解の構造追跡に到達した状態」である。

### 1.3 offsetの壁（10回の実証 — 投資禁止領域の確定）
per-well offset（地層枝選択）は leak-free 信号で直接予測不能であることを以下で確認済み（`docs/loop_log.md` L32-45, Decision_Log）:

| # | 手法 | 結果 |
|---|---|---|
| 1 | GR直接照合 (exp013/013b) | 43.08 / +0.017悪化、NO-GO |
| 2 | MHT尤度枝選択 (loop#2) | CV 22.73 vs single 17.98（-4.7ft悪化） |
| 3 | 空間surface offset (loop#3) | corr **-0.135**（逆相関） |
| 4 | self-calibration oracle | corr -0.028 |
| 5 | 空間TVT補間 | hidden RMSE 149-186（疎すぎ） |
| 6 | NN回帰6種 (exp019/020/039/046/053/075) | 全て10.7〜16.5でPF未満 |
| 7 | 外部GBM stack OOF (exp073) | CV改善でもLB悪化（負の転移） |
| 8 | 学習的per-well再重み付け (loop#5) | 10.80 vs 固定10.05（過学習） |
| 9 | GR特徴量化 leak-safe (exp017) | -0.067悪化 |
| 10 | oracle診断 | 1-offset/well理想でも8.21（PF 11.02に対する天井） |

**含意**: 「offsetを当てる」直接アプローチは全形態で死亡。残された道は (i) 直交ソースのblend、(ii) **系列照合・大域最適化・学習型尤度による間接的な構造追跡改善** のみ。

### 1.4 我々の固有資産
- **exp026 PF×geom**: CV 10.06 / LB 8.672。公開stackとの誤差相関 **0.611** = 部分直交（exp073実測）。公開勢が持たない decorrelated 3rd source。
- favorable CV-LB transfer 実績: exp072 gap +0.81、exp022系 +1.39。**ただし借り物OOFで破壊される**（exp073: CV 8.79→LB 8.630、imputer非再構築による膨張。LB_Tracking.md）。
- GPU (RTX 2080 SUPER): TCN 5-fold 2.9分の実績（exp075）。学習型emissionの実機学習が可能。

### 1.5 per-well誤差構造（攻撃対象の特定）
exp022 per_well.csv の層別（loop_log.md L92-95）:
- good帯 (<8ft): 566 wells — PF追跡成功（最良 0.584 ft）
- bad帯 (8-20ft): 188 wells — **部分ドリフト群 = 最大誤差源**
- broken (>20ft): 47 wells — wrong-branch lock（±18-43ftのbias）、全て長尺+大Z_span
- per-well oracle min(blend,pf,geom) = **7.094 ft** — 現有成分の選択だけで-1.6ftの未回収余地があるが、leak-free選択信号は disagreement の spearman +0.25 が最強で回収不能（loop#1/5で実証）

**結論**: bad帯188本の「部分ドリフト」と broken 47本の「branch lock」は、**逐次フィルタ（PF）の構造的弱点**（一度迷子になると戻れない）に起因する。これが攻撃対象。

---

## 2. 技術的根拠（外部文献調査 2026-06-11 実施）

### 2.1 大域最適化（smoother / Viterbi / DTW）は逐次フィルタに優る
- 一般SMC理論: forward-backward particle smoother は filter の particle degeneracy を後退再帰で補正（Klaas et al. ICML 2006 "Fast Particle Smoothing"）。**事後一括予測タスク（本コンペはまさにこれ — test区間末端までGR観測あり）では全データを使う smoother/Viterbi が filter より理論的に優位**が標準的理解。
- geosteering直接適用: Alyaev et al. 2021 (Applied Computing and Geosciences) — 確率的解釈+DPの自動アルゴリズムが**29人中28人の専門家を上回る**。SPE Journal 2025 "Geosteering Robot" は PF多重解釈+RL を ROGII Geosteering World Cup 類似環境で実証。
- DTW for log correlation: Lineman+ 1987 (SPWLA) 以来の古典。Wheeler & Hale 2014 (SEG) は多坑井同時相関で大域最適性を主張。Sylvester 2023 (Basin Research, 査読誌) がRGT多坑井相関の近年代表。
- 制約付き vs 無制約: Sakoe-Chiba帯の系統検証（Geler+ 2016/2019）で適切な帯幅は無制約より精度向上、ただし**帯幅依存性が大きい**（チューニング必須）。Ratanamahatana & Keogh (SDM 2004) は学習制約が固定帯に優ると報告。
- **exp052 DTW失敗（CV 23.3）との整合**: exp052は「無制約・未較正・素朴シーケンス照合」（Decision_Log L48）。文献が有効性を示すのは「制約+較正+大域DP」の形態であり、未踏。

### 2.2 学習型emission（最も強い外部根拠）
- **DHGC (JMSE/MDPI 2025末, 査読誌)**: 1D CNN を 177,026 triplet（ノルウェー北海8坑井の**GR**）で学習 → スコアリングNN + DP整列。**未見89ペアで相関 0.35→0.91、成功率98.9%、素のDTW比8.2倍高速**。本コンペとほぼ同一設定（GR系列の坑井間照合）で「学習コスト+DP ≫ 生信号DTW」の定量的実証。
- ASDNet (AI in Geosciences 2023)、CMT-Hiformer (Processes 2025)、Le+ 2019 (Petrophysics, CNN depth matching) が補強。
- 注意: 「ガウシアン尤度 vs 学習スコア」の直接A/B論文は無し。DHGCの 0.35→0.91 が最近接の代替証拠。

### 2.3 リスクの根拠
- Group E封印（exp011: typewell GR特徴量化leak）は「**点単位特徴量化**」のleak。学習emissionは「系列整列コスト」という別形態だが、**fold内train wellsのみで学習する規律**が必須（exp022の成功 = well単位系列照合が点単位の盲点だった、という過去の教訓と同型）。
- exp073教訓: 採点時に我々が推論経路を管理できない成分は favorable transfer を破壊する。全ての新成分は**kernel内で自己完結計算**できる形で設計する。

---

## 3. 達成計画（Phase別、Go/No-Go ゲート付き）

### 数値ターゲットの逆算
CV-LB転移則: LB ≈ CV − 0.8〜1.4（exp072: +0.81, exp022系: +1.39、自前成分のみで成立）。
**LB 5.9 を取るには 自前管理パイプラインで pooled CV ≈ 6.7〜7.3 が必要**（現best CV: exp073 nested 8.69 ただし汚染、クリーンは exp072系 9.09）。
つまり **クリーンCVをあと約2ft削る**のが課題の定量的定義。

### Phase A（即時〜2日）: 7.5 base 確保 + PF直交注入【防衛線】
- A1: sp45 fork の LB確認（提出中）。基準: LB ≤ 7.6。
- A2: exp026 PF（corr 0.611）を fork kernel 内で自己完結計算し nested OOF で重み決定して注入。
- 期待: 7.4 → **7.0-7.2**（corr 0.61・同等強度blendの理論値 -0.2〜0.4）。
- **ゲートA**: CV-LB gap が +0.5以上の favorable を維持していること。崩れたら成分を巻き戻す。

### Phase B（2-4日）: forward-backward PF smoothing【低コスト先行実験】
- 根拠: §2.1。現PFはfiltering限定で、bad帯188本の「途中ドリフト」を将来観測で修正できない。test区間も末端までGRがあるため smoothing は完全に leak-free。
- 実装: exp022 PF に backward pass（two-filter smoother または FFBSi簡易版）を追加。粒子・seedは既存資産を再利用。
- **定量ゲートB**: pooled CV 10.06 → **9.5以下**、かつ bad帯188本の median 改善 ≥ 1.0 ft、broken 47本の悪化なし。per-well軌跡プロットでドリフト消失を目視確認。
- 未達なら: 「大域化に効果なし」の証拠として Phase C の期待値を下方修正（ただしDTWは別機構なので中止はしない）。

### Phase C（4-8日）: 制約付きDTW / Viterbi 大域アライメント【本命1】
- 根拠: §2.1 + exp052失敗の原因分析（無制約・未較正が死因であり機構自体の否定ではない）。
- 設計（exp052との差分を明示）:
  1. 状態空間 = (MD, typewellオフセット)、exp022と同じ pos=TVT+Z 分離を維持（exp052の素朴照合に戻らない）
  2. 遷移コスト = dip rate物理制約（傾斜変化上限、層厚単調性）
  3. 観測コスト = **affine較正済み**GR残差（iaztec監査の a,b 較正を前段に）
  4. 帯制約 = **PF posterior を Sakoe-Chiba帯として使用**（既存資産との合成。固定帯の帯幅依存問題を回避）
- **定量ゲートC**: pooled CV ≤ 9.0、3 test相当wellで悪化ゼロ、broken 47本のうち ≥ 10本が <20ft に回復。
- 期待: blend後 CV 8.5前後 → LB 6.8-7.2圏。

### Phase D（5-10日、Cと並行可）: 学習型emission【本命2・GPU】
- 根拠: §2.2 DHGC（本コンペ同一設定で 0.35→0.91 の実証）。
- 設計:
  1. 教師データ: train wellsの正解TVTから (lateral窓, typewell窓) の正対応/負対応ペアを生成、triplet/contrastive学習（DHGC方式、fold内trainのみ — leak規律）
  2. モデル: 小型1D CNN（GPU 5-fold 数分、exp075実績から実行可能性確認済み）
  3. 統合: 学習スコアを (a) PF/smootherのemissionに置換、(b) Phase C のDTW観測コストに使用 — **C×Dの合成が最終形**
- **定量ゲートD**: 学習スコア単体の対応判定 AUC ≥ 0.85（DHGCは0.997だが多坑井大データ。保守的に設定）、emission置換後 PF CV が 10.06→9.5以下。
- リスク: NN単体の弱さは6回実証済み（§1.3 #6）。ただしそれは「TVT直接回帰」であり、本Phaseは「対応判定の2値学習」= 別タスク。回帰でなく照合学習である点が過去の失敗と決定的に異なる。

### Phase E（継続）: 統合 + Private防衛
- B/C/D生存成分 + Phase A blend を nested NNLS統合。fold一貫性・重み安定ゲート。
- 最終2提出: 安全板（Phase A、7.x確実）+ 攻撃版（C×D統合、5-6台狙い）。
- guarded override等のPublic限定leak不採用（exp044で採点時死にコード確定済み）。

### 撤退基準・やらないこと
- offset直接予測（回帰/分類/尤度選択/空間補間）には**一切投資しない**（§1.3、10回の壁）。
- blend重み・selector・projectionの追加チューニングは Phase A 完了をもって打ち止め（期待値合計 -0.3未満、5台に構造的に届かない）。
- 借り物外部OOFのblend禁止（exp073）。全成分はkernel内自己完結計算。
- B/C/D全てが各ゲート未達の場合: 5台は現知見では到達不能と判定し、6.8圏防衛（Phase A+部分成分）+ PNG画像CNN（exp055再挑戦、最後の未踏領域）に切替。

---

## 4. マイルストン表

| Phase | 内容 | 期待LB | 根拠の強さ | 期間 |
|---|---|---:|---|---|
| A | 7.5 base + PF直交注入 | 7.0-7.2 | 高（corr 0.611実測 + 著者明言） | 〜2日 |
| B | PF smoothing | (CV -0.5の検証) | 中（SMC理論、geosteering直接比較は無し） | 2-4日 |
| C | 制約付きDTW/Viterbi | 6.8-7.2 | 中（文献多数、ただしexp052失敗歴あり） | 4-8日 |
| D | 学習型emission | C×D合成で 5.8-6.5 | 中-高（DHGC: 同一設定で大幅改善の査読済実証） | 5-10日 |
| E | 統合+防衛 | 最終 | — | 継続 |

**正直な評価**: Phase A で 7.0圏（上位10位前後）は高確度。**5台は C×D の成否に懸かっており、成功確率は主観で 30-50%**。ただしこれは (i) 1位との1.5ftギャップが公開技術に存在しない、(ii) 残された未踏領域が系列大域化+学習照合のみ、(iii) その両方に査読済みの肯定的外部実証がある、という消去法と文献の両面から導かれる**現時点で最も期待値の高い経路**である。

---

## 5. 実験規律（既存鉄則の再掲 + 本計画固有）
1. 借り物OOF禁止、全成分kernel内自己完結（exp073）
2. per-well hard routing/学習reweight禁止（loop#1/5）
3. offset直接予測禁止（10回の壁）
4. 学習emissionは fold内train wellsのみで学習（Group E再発防止）
5. 各Phaseは数値ゲートで Go/No-Go、pooled CVだけでなく **per-well軌跡プロット**（bad帯/brokenの回復本数）で判定
6. CV-LB gap毎提出監視、gap +0.5未満に縮んだら成分巻き戻し
7. 1実験1目的、experiments/expXXX/ に result.json / oof / notes 保存、EXP_SUMMARY.md 更新
