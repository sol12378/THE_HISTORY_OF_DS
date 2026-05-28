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
