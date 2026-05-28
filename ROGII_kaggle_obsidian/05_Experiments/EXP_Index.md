# 実験インデックス

| Exp | Status | Model | Features | CV | LB | Notes |
|---|---|---|---|---:|---:|---|
| exp000_leak_lookup | planned | lookup | leaked train target | - | - | 提出形式確認のみ |
| exp001_anchor_baseline | completed | rule | anchor | 15.909853 | - | [[exp001_anchor_baseline]] |
| exp002_slope_baseline | planned | rule | anchor+slope | - | - | trajectory sanity check |
| exp003_lgb_anchor_trajectory | completed | LightGBM | anchor+trajectory+GR | 15.054865 | - | [[exp003_lgb_anchor_trajectory]] |
| exp004_oof_error_slicing | completed | analysis | OOF slices | 15.054865 | 14.147 | [[exp004_oof_error_slicing]] |
| exp005_worst_well_analysis | completed | analysis | worst well pattern | 15.054865 | 14.147 | [[exp005_worst_well_analysis]] |
| exp006_anchor_guard | completed | post-process | anchor guard B案 | 14.724541 | - | [[exp006_anchor_guard]] |
| exp007_traj_features | completed | LightGBM | SAFE+Group A+B+C | 13.867054 | - | [[exp007_traj_features]] |
