# Experiment Summary

| Exp | Model | Features | Target | CV | LB | Time | Status | Notes |
|---|---|---|---|---:|---:|---:|---|---|
| exp001_xgb_baseline | XGB | basic | direct | - | - | - | planned | starter reproduction |
| exp002_lgb_anchor_delta | LGB | basic+anchor | delta | - | - | - | planned | anchor delta validation |
| exp001_anchor_baseline | rule | last_known_TVT | direct TVT | 15.909853 | - | <1m | completed | PS直前のTVTを固定延長する基準線。leak risk low |
| exp003_lgb_anchor_trajectory | LightGBM | anchor+trajectory+GR | TVT-last_known_TVT | 15.054865 | 14.147 | ~2m | completed | anchorから0.854988改善。Public LBはCVより0.908良いがtest 3 wellsのため過信しない |
| exp004_oof_error_slicing | analysis | OOF slices | error analysis | 15.054865 | 14.147 | <1m | completed | well/hidden_length/trajectory形状別にexp003を分析。327 wellsでanchorより悪化 |
| exp005_worst_well_analysis | analysis | OOF slices | worst well pattern | 15.054865 | 14.147 | <2m | completed | worst well共通点: downward+anchor強+hidden4000超。8000+でanchorに負け。11 anchor_blown wells検出 |
| exp006_anchor_guard | post-process | blend | anchor guard B案 | 14.724541 | - | <1m | completed | hidden>8000→anchor、mean_pred_delta>30→anchor。+0.330 CV改善。test wellsはno_guardで提出変わらず |
| exp007_traj_features | LightGBM | SAFE+A+B+C | TVT-last_known_TVT | 13.867054 | - | ~10m | completed | Group A: pre-PS TVT slope/curv。Group B: dZ/dMD per-row+pre-PS dir。Group C: kh_ratio,hidden_frac。+1.188 vs exp003 |
| exp007b_guard | LGB(1500)+guard | SAFE+A+B+C | TVT-last_known_TVT | 13.853360(raw)/13.985993(blend) | - | ~15m | completed | n_est=1500でfold4改善(872iter)。raw+0.014 vs exp007。双方向guard逆効果(17 wells LGB<anchor)。best=raw 13.853360 |
| exp008_gr_rolling | LightGBM | SAFE+A+B+C+D | TVT-last_known_TVT | 13.808621 | **12.339** | ~15m | completed | Group D: pre-PS GR統計+rolling。+0.045 vs exp007b。LB=12.339 (rank 1041/1906, 54.6%)。CV-LB gap=-1.469(LBがCVより良い)。exp003比 LB+1.808大幅改善。CVがLBに確実に転化することを確認 |
| exp009_typewell_gr_alignment | LightGBM | SAFE+A+B+C+D+E | TVT-last_known_TVT | 13.922291 | - | ~20m | completed | **悪化 -0.114**。per-well E(862M)は有効だがper-row tw_tvt_correction(0.5M)がノイズ。GR点単位補正は失敗。系列ベース alignment が必要 |
| exp009b_typewell_gr_well_only | LightGBM | SAFE+A+B+C+D+E_well | TVT-last_known_TVT | 13.932154 | - | ~20m | completed | **悪化 -0.124** vs exp008。per-row E削除後も改善せず。E_well特徴量(importance高い)がoverf itting原因。exp008がbest維持。Group E 封印。 |
| exp010_oof_slicing_fold24 | analysis | OOF slices | exp009b vs exp008 | 13.808621 | - | <1m | completed | fold2/4悪化要因。corr 0.60-0.85帯(496wells/多数派)が+0.167悪化、corr>0.85(243)は-0.198改善、corr<0.60(34)は+0.761崩壊。worst wellsは長尺hard well(E補正がノイズ蓄積)。exp009の矛盾解消=多数派中域が静かに劣化 |
| exp011_typewell_leak_test | LGB ×2 | E無し vs E有り on dedup fold | TVT-last_known_TVT | base 13.651645 / E 13.928077 | - | ~3m | completed | **typewell leak確定**。重複typewell集約foldでE-baseline gapが+0.124→+0.276に拡大(DiD +0.153)。well_id GroupKFoldがE特徴量を過大評価していた。exp010の共有well診断(-0.182 vs +0.090)と整合。**Group E 完全封印確定**。今後typewell-grouped fold採用を検討 |
