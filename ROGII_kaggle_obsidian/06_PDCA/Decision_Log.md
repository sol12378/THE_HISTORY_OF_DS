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
| 2026-06-02 | **exp018 モデル多様化blendを採用、新best CV=13.340426**(blend+exp015平滑化) | LGBM+XGB+CatBoost等加重blendが+0.184。平滑化で+0.0012、全fold一貫、leak-free。exp015(13.520)から+0.180 | exp018 CV=13.3416→平滑13.3404 | [[exp018_model_blend]] |
| 2026-06-02 | 多井戸空間モデル(diag_spatial)を棄却 | TVT~f(X,Y,Z)はhidden RMSE149-186。well間隔~6400でTVTは±185しか拘束できずanchor±16に完敗。wellが疎すぎてoffset回収不能 | diag_spatial | [[gr-offset-ceiling]] |
| 2026-06-02 | **1位LB(6.8)接近の本命=typewell-aware NN(exp020)を検証→offset回収不能を最終確認** | lateral GR↔typewell profileのcross-attention(微分可能DTW)でもNN単体16.5と悪化。GR照合/空間/NN/attentionの全paradigmでoffset取れず。public LB6.8は3本分散要因が大きい | exp020 NN16.5/blend13.322 | [[exp020_typewell_attn]] |
| 2026-06-02 | **現best CV=13.320964**(exp018+exp019+exp020 3-blend+平滑)。次は実LB提出でgap測定 | 全fold一貫leak-free。exp015(13.520)から+0.199。グローバルCVでの大幅改善は情報限界で頭打ち | exp020 3-blend平滑 | [[exp020_typewell_attn]] |
