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
| exp007b_guard | completed | LGB(n=1500)+guard | SAFE+Group A+B+C | 13.853360(raw) | - | [[exp007b_guard]] |
| exp008_gr_rolling | completed | LightGBM | SAFE+Group A+B+C+D | 13.808621 | - | [[exp008_gr_rolling]] |
| exp009_typewell_gr_alignment | completed | LightGBM | SAFE+Group A+B+C+D+E | 13.922291 | - | [[exp009_typewell_gr_alignment]] |
| exp009b_typewell_gr_well_only | completed | LightGBM | SAFE+A+B+C+D+E_well | 13.932154 | - | [[exp009b_typewell_gr_well_only]] |
| exp010_oof_slicing_fold24 | completed | analysis | OOF slices (corr層別) | 13.808621 | - | [[exp010_oof_slicing_fold24]] |
| exp011_typewell_leak_test | completed | LGB×2 (DiD) | E無し vs E有り on dedup fold | base 13.651645 / E 13.928077 | - | [[exp011_typewell_leak_test]] |
