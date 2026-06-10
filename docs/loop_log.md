# 自律実験ループ ログ (目標: LB Top 5 / LB 5台)

各行: ループ# | 手法 | CV | LB | 採否 | 次の一手

| # | 日付 | 手法(1変更) | CV | LB | 採否 | 次の一手 |
|---|---|---|---:|---:|---|---|
| 0 | 06-10 | exp073 公開資産統合blend (pf+geom+ravaghi+pilk_cat+proj) | 8.79 | 提出待ち(UI) | 提出中 | LB着地でgap較正 |
| 1 | 06-10 | Phase1 forensics + per-well routing予測可能性テスト | 8.69(分析) | - | 棄却(routing単純版8.36止まり) | Phase2: tracker改修(lik-PF+selector) |
| 2 | 06-10 | MHT multi-restart PF (offset{-40..40}尤度選択, subset207) | 22.73 vs single17.98 | - | **棄却(悪化-4.7, 悪化53本)** | LB着地待ち→較正後に枝選択の非尤度信号(空間prior/NN ranker)を検討 |

---

## Loop 1 詳細 (Phase 1 forensics + routing test)

### Plan (誤差分析→仮説)
exp073 blend OOF (8.69) のper-well誤差センサスで投資先を特定する。仮説: 既存3成分{blend,pf,geom}のper-well routingで大きな余地があるか?

### Do (1変更: 既存OOFのper-well分析、提出なし)
- forensics: 帯別人口とpooled²寄与を分解。
- routing test: leak-free per-well特徴(disagreement|pf-geom|, z_span等)が「どの成分を信頼すべきか」を予測できるか。

### Check (結果)
- **帯別寄与**: good<8=566well(22%), **bad 8-20=188well(45%, 最大)**, broken>20=19well(33%)。blendは既にPFのbroken 48→19に削減済み。**最大の誤差源はbad帯(8-20ft)= 部分ドリフトwell群**。
- broken 19本は全て大bias(±18-43ft)= wrong-branch lock。長尺・大z_span。
- **per-well oracle pick min(blend,pf,geom)=7.094**(blend 8.69から-1.6の余地)。
- pf<blend on 292well(38%), geom<blend on 153well(20%) → per-well最適混合は大きく変動。
- leak-free信号: disagreement(|pf-geom|) が誤差と spearman **+0.25**(最強)だが、単純なdisagreement-gated geom-routingは pooled 8.36止まり(oracle 7.09に遠い)。geom_better_rateは高disagree帯でも16-27%と低い。

### Act (採否と次)
- **単純routing/reweight = 採用見送り**。理由: 既存3成分は同じドリフトを共有するため、選択の予測可能ceilingが低い(過去のoffset予測不能の壁と整合)。
- **次の本命 = Phase 2 トラッカー改修**。bad+broken帯(78%の誤差)を減らすには「より良い追跡」が必要。最小変更の第一歩 = 公開のmulti-scale lik-PF(128seed×4scale尤度加重)+ 我々のexp071 selector(PF 10.91→10.47実績)を移植し、PF単体 11.0→10.3-10.5 を狙う。これがblend底上げの土台。
- CV-LB gap監視: exp073 LB着地後に較正(現状exp072 gap 0.806)。

### 提出メモ
- exp073 kernel (sol12378/rogii-exp073-blend) commit完走。**CSV直接提出は400(notebook-only comp)**。Kaggle UIで "Submit to Competition" が必要。

---

## Loop 2 詳細 (MHT multi-restart PF)

### Plan
broken 19本は全てwrong-branch lock(大bias)。現PF init_spread 4ftでは遠方の正枝に届かない。offset{-40,-20,0,+20,+40}から並走し、well毎に総尤度最大の枝を選択(4-offset oracle 4.39の実装形)。subset(rmse_blend>=8の207well)で48seed×5offsetで概念検証。

### Do
exp076_mht_pf.py。pf_singleにinit_off追加。restart毎にmax single-seed total loglikをスコアとして枝選択。

### Check
- single(off0) 17.98 → **MHT 22.73 (悪化 -4.7ft)**。rescue 3本のみ、悪化53本。
- 選択offset分布: 0.0=115, ±20=55, ±40=37 → 非ゼロを92本で選んだがその多くが誤り。
- CV-LB gap: 該当なし(subset診断、未提出)。

### Act
- **棄却**。GR尤度は枝をランクできない(多価性で偽ピーク選択)。「offset leak-free予測不能(corr<=0.155)」の8回目の確認。
- 含意: Phase2bのMHTが前提とした「累積尤度による枝選択」は死亡。枝選択には**非尤度信号**(空間formation prior / NN ranker / 幾何滑らかさ)が必須。
- 次: **まずexp073のLB着地(ref53533960 PENDING)を待ち、8.79の転移を較正**してから、非尤度の枝選択(Phase4空間prior)を検討。LB次第で方向確定。
