# Decision Log

| Date | Decision | Reason | Evidence | Link |
|---|---|---|---|---|
| 2026-05-25 | Obsidianをプロジェクト記憶として使う | 多数の実験をまたいで判断理由を残す必要がある | User request | [[Home]] |
| 2026-05-25 | leak lookupと本物のCVを分離する | test wellsがtrainに存在する | local data check | [[Leakage_and_Risks]] |
| 2026-05-25 | modeling前にbase data contractsを固定する | コンペ中のschema変更はCV比較を壊す | data engineering planning | [[Long_Term_Data_Engineering_Plan]] |
| 2026-05-25 | 最初の本命baselineはanchor差分LightGBMにする | anchorが強く、差分学習の改善量を測るのが安全で速い | exp001 RMSE 15.909853、exp003 RMSE 15.054865 | [[exp003_lgb_anchor_trajectory]] |
