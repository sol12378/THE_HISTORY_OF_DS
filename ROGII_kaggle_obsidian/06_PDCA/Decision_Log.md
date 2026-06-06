# Decision Log

| Date | Decision | Reason | Evidence | Link |
|---|---|---|---|---|
| 2026-05-25 | Obsidianをプロジェクト記憶として使う | 多数の実験をまたいで判断理由を残す必要がある | User request | [[Home]] |
| 2026-05-25 | leak lookupと本物のCVを分離する | test wellsがtrainに存在する | local data check | [[Leakage_and_Risks]] |
| 2026-05-25 | modeling前にbase data contractsを固定する | コンペ中のschema変更はCV比較を壊す | data engineering planning | [[Long_Term_Data_Engineering_Plan]] |
| 2026-05-25 | 最初の本命baselineはanchor差分LightGBMにする | anchorが強く、差分学習の改善量を測るのが安全で速い | exp001 RMSE 15.909853、exp003 RMSE 15.054865 | [[exp003_lgb_anchor_trajectory]] |
| 2026-05-30 | Group E（typewell GR alignment）を完全封印する | importance上位だが汎化に有害。リーク除去後はbaselineを+0.276悪化。中域corr多数派が劣化 | exp009b CV悪化、exp010 corr層別、exp011 leak DiD +0.153 | [[exp011_typewell_leak_test]] |
| 2026-05-30 | best維持はexp008 (CV=13.808621)。次は非typewell軸で攻める | Group E系列が全滅。trajectory post-PS / anchor guard等の別軸へ | exp009/009b/011 全てexp008に劣後 | [[exp008_gr_rolling]] |
| 2026-05-30 | typewell由来特徴量を使うならtypewell-grouped foldを必須化する | 34 wells(13グループ)が同一typewell共有、well_id GroupKFoldでリーク | typewell signature重複検出、exp011 leak確定 | [[exp011_typewell_leak_test]] |
| 2026-05-30 | CVドリブン開発方針を確定する | exp008でCV改善1.246→LB改善1.808確認。CVがLBに確実転化。gap=-1.469 | submission_001 LB=12.339 | [[submission_001_exp008]] |
| 2026-05-31 | **GR-typewell直接照合をNO-GO判定**。Tier2の本丸仮説を棄却 | leak-free直接照合(exp013/013b)が全変種でexp008に劣後。狭窓±10+exp008中心でも最善+0.017悪化、純match+0.6〜2.6。GR多価で逆変換不安定。exp009特徴量化も含め3実験一貫で失敗 | exp013 A=43.08/anchor15.91、exp013b best13.826>exp008 | [[exp013_gr_match_go_nogo]] [[exp013b_gr_local_refine]] |
| 2026-05-31 | Tier2投資をGRアライメント以外へ振り替える | GR照合NO-GO。残路はDTW系列照合のみだが高リスク。代わりにモデル多様化(XGB/Cat)・系列平滑性・幾何特徴(Group F)へ | Phase1判定結果 | [[Strategy_2026-05-31]] |
| 2026-05-31 | anchor guard(exp012)は本採用しない(保留) | +0.054だがfold非一貫(fold0 -0.077)。864通りsweepのOOF過学習兆候。strong_guard α=0.85の頑健部分のみ将来検討 | exp012 fold別delta | [[exp012_anchor_guard_exp008]] |
| 2026-06-02 | **CV<=5 は GR含む正規手段で到達不可能と確定**。oracleで上限を定量化 | geom形状は正しく残差は低周波offset。理想offset(1/well)でも上限8.21、4/wellで4.39。だがGRが選ぶoffsetは真offsetとcorr=+0.155と極弱。GR特徴量化(exp017)もleak-safe typewell-foldで-0.067悪化。GR照合は全形態(exp009/011/013/013b/017+oracle)でNO-GO | diag_gr_ceiling, diag_seq_align, exp017 | [[exp017_gr_align_features]] [[gr-offset-ceiling]] |
| 2026-06-02 | 現実的次手はモデル多様化(XGB/CatBoost blend)。現best維持=exp015(13.520) | GR路は完全閉鎖。geom形状が良い構造的知見を活かしつつ、誤差非相関でCV底上げを狙う | oracle診断+exp017 | [[Strategy_2026-05-31]] |
| 2026-06-02 | per-well offsetは leak-free信号で予測不能と確定(self-calib corr=-0.028) | known自己ホールドアウトのgeom外挿biasは真hidden offsetと無相関。GR(0.155)も含めoffsetは復元不能。これがLB首位6.8の天井理由 | diag_self_calib | [[gr-offset-ceiling]] |
| 2026-06-03 | **「GR照合 全形態NO-GO」を部分撤回**。well単位確率的ハードトラッカー(PF)は有効 | 参照3notebook解読→PF(128seed×500粒子,状態pos=TVT+Z,GR尤度)を移植。**pooled CV 11.024=全手法最良**(geom13.53/blend13.32/anchor15.91超)。完全leak-free。3 test well平均≈5.0で参照"4.71ft"再現。並行作業のNO-GOは学習的/ソフト/グローバル形態のみで、PFは未検証だった | exp022_particle_filter CV=11.024 | [[exp022_particle_filter]] |
| 2026-06-03 | Beam Search(決定論)は不採用。PFを採用 | beam CV15.70≈anchor(±2運動制約が粗く迷子)。PFは連続状態+尤度加重で曖昧性を統合し11.02 | exp021 vs exp022 | [[exp021_beam_track]] |
| 2026-06-03 | **新本線=PFをensembleに統合**。PF×geom blend で現時点 CV 10.16 | PFとgeom誤差相関0.426と低い。0.6·PF+0.4·geom+平滑=10.16(前best13.32から+3.16,全fold一貫9.49〜11.07)。次はtree/NN含む多段blend+壊れwellゲート+PF調整+Kaggle kernelでLB転移検証 | PF×geom blend分析 | [[exp022_particle_filter]] |
| 2026-06-03 | リーク(exp023)は提出採用しない方針(賞転移しない見込み) | 3 test wellはtrainに完全TVTありRMSE=0だが、LB#1=6.8≠0→train TVT≠Kaggle採点真値。privateで無効の公算。正直CVと厳密分離して保持 | exp023 leak_rmse=0 vs LB#1=6.8 | [[exp023_leak_lookup]] |
| 2026-06-03 | **多段ブレンド(exp024)を新best採用 CV=10.077**。PFをensembleに統合 | NNLS(delta,非負,nested5-fold)で pf/geom/trees/nn/attn をブレンド→10.090、+平滑10.077。前best13.32から+3.24、全fold一貫(9.28〜11.08)。重み=PF0.66+attn0.47(幾何系は相関0.98-1.0で冗長、PFのみ0.43直交)。leak-free | exp024 nested CV=10.0897→平滑10.0769 | [[exp024_multistage_blend]] |
| 2026-06-03 | 壊れwellゲートは不成立。NNLS重みで頑健化する | 47壊れwell(pf_rmse>20)オラクル上限→attn=9.46だが、leak-free検出シグナル(PF自己GR残差corr0.225)で分離不能、gate適用は悪化(10.09)。PF信頼性は予測不能(diag_self_calibと整合) | gate検証 | [[exp024_multistage_blend]] |
| 2026-06-03 | PFチューニング採用(init_spread=4,PN=0.01)。full再実行→再ブレンド予定 | ~129well subsetでbaseline10.726→ispr4_pn0.01=10.468(−0.258)。広いinit spread+高め運動雑音の相互作用で探索性向上 | exp025_pf_tune subset grid | [[exp025_pf_tune]] |
| 2026-06-05 | **Horizon distillation (A/B/C案) 全棄却**。情報理論的に(MD,X,Y,Z,GR)→horizonsの関数等価で寄与なし | exp028b: horizons予測R²=0.945だがTVT予測+0.088悪化(CV14.60→14.69)。Niccoli証言「per-formation classifier無効」と完全整合 | exp028b | [[exp028b_horizon_resid]] |
| 2026-06-05 | **Multi-typewell PF採用(blend寄与)**。単体は悪化だがexp022と相補的 | exp030b: 空間最近傍3typewellでPF並走、単体CV=12.15で-1.12悪化、しかしexp033 NNLS blendで weight=0.12 採用 | exp030b | [[exp030b_multi_tw_vec]] |
| 2026-06-05 | **Physical Likelihood PF採用(blend寄与)**。normalized GR + GR derivative で47壊れwell中23救出 | exp031: 単体CV=20.38だが**誤差相関 vs exp022 = 0.333と低い**(相補的)。直接2-blendでCV10.40 | exp031 | [[exp031_pf_physical_lik]] |
| 2026-06-05 | **exp033 = 新best CV 9.977** (-0.085 vs exp026)。8 components NNLS blend | pf_orig0.31 + attn0.29 + pf_tuned0.21 が主軸、残りは多様化補助。test3wells RMSE 3.99/4.62/5.64 | exp033 | [[exp033_final_blend]] |
| 2026-06-05 | **1位LB6.5は leak-free到達不能 と最終確定**。leaders are sub-9 RMSE | per-well offsetはleak-free信号で予測不能(corr<=0.155)、47壊れwell大半解けない。我々のLB予想8.5は「sub-9 leader圏」 | Niccoli証言 + 全実験 | [[exp033_final_blend]] |
| 2026-06-02 | **exp018 モデル多様化blendを採用、新best CV=13.340426**(blend+exp015平滑化) | LGBM+XGB+CatBoost等加重blendが+0.184。平滑化で+0.0012、全fold一貫、leak-free。exp015(13.520)から+0.180 | exp018 CV=13.3416→平滑13.3404 | [[exp018_model_blend]] |
| 2026-06-02 | 多井戸空間モデル(diag_spatial)を棄却 | TVT~f(X,Y,Z)はhidden RMSE149-186。well間隔~6400でTVTは±185しか拘束できずanchor±16に完敗。wellが疎すぎてoffset回収不能 | diag_spatial | [[gr-offset-ceiling]] |
| 2026-06-02 | **1位LB(6.8)接近の本命=typewell-aware NN(exp020)を検証→offset回収不能を最終確認** | lateral GR↔typewell profileのcross-attention(微分可能DTW)でもNN単体16.5と悪化。GR照合/空間/NN/attentionの全paradigmでoffset取れず。public LB6.8は3本分散要因が大きい | exp020 NN16.5/blend13.322 | [[exp020_typewell_attn]] |
| 2026-06-02 | **現best CV=13.320964**(exp018+exp019+exp020 3-blend+平滑)。次は実LB提出でgap測定 | 全fold一貫leak-free。exp015(13.520)から+0.199。グローバルCVでの大幅改善は情報限界で頭打ち | exp020 3-blend平滑 | [[exp020_typewell_attn]] |
| 2026-06-06 | **leak路線 完全終了**。採点test=train非存在のhidden well群と確定 | exp044純leak提出が"submission incorrect format"エラー=hidden wellはtrainに無くleak lookup全NaN。exp034/036/037が全10.794だったのも整合(leak不適用、壊れ4-comp model支配) | exp044 format error | [[exp034_hybrid_leak]] |
| 2026-06-06 | **SaintLouis 5.986はleak-free確定**。leak仮説を完全棄却 | 構造的leak(3 test wellがtrain存在)は採点対象外のサンプルwellのみ。実採点はhidden well | exp044 | [[exp034_hybrid_leak]] |
| 2026-06-06 | **5.986への律速=broken well 47本のPF追跡ロスト**と特定 | PF per-well RMSE中央値5.66(既に5.986並)。47 broken(>20)がpooled CV 11.02に押上げ。broken→good修正でpooled概算6.0。4-offset/well oracle 4.39が裏付け。offsetはGR逐次追跡で可(中央値5.7)、特徴回帰では不能(corr-0.028) | per_well分布 + diag_gr_ceiling | [[exp022_particle_filter]] |
| 2026-06-06 | **P0-P4はexp026未超え**。exp026(LB8.672)が唯一の検証済best維持 | exp040 multi-scale PF CV10.979(+0.045)、exp041 residual GBDT CV10.53だがexp026の10.06に劣る。multi-tw/physical-lik(全体適用)は有害確定 | exp040/041, pdca_blend | [[exp026_final_blend]] |
| 2026-06-06 | **次戦略=broken well救済に全集中**。blend/特徴でなくPF追跡頑健性が勝負 | P-A診断→P-B再初期化/P-C Beam hybrid/P-D観測物理化(broken限定)。各LB検証(gap1.4転移実証済) | 戦略策定 | [[exp022_particle_filter]] |
