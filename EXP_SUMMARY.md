# Experiment Summary

| Exp | Model | Features | Target | CV | LB | Time | Status | Notes |
|---|---|---|---|---:|---:|---:|---|---|
| exp001_xgb_baseline | XGB | basic | direct | - | - | - | planned | starter reproduction |
| exp002_lgb_anchor_delta | LGB | basic+anchor | delta | - | - | - | planned | anchor delta validation |
| exp001_anchor_baseline | rule | last_known_TVT | direct TVT | 15.909853 | - | <1m | completed | PS直前のTVTを固定延長する基準線。leak risk low |
| exp003_lgb_anchor_trajectory | LightGBM | anchor+trajectory+GR | TVT-last_known_TVT | 15.054865 | - | ~2m | completed | anchorから0.854988改善。foldばらつきとwell別悪化に注意 |
