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
