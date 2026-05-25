# exp003_lgb_anchor_trajectory

## 目的

[[Anchor_Features]] と trajectory 系の安全特徴量で `TVT - last_known_TVT` を学習し、anchor baseline からの改善を確認する。

## 仮説

target 区間内の `MD/X/Y/Z/GR` と PS からの相対位置を使えば、単純な `last_known_TVT` 固定予測より TVT絶対値RMSEを下げられる。

## 変更内容

- 入力: `data/processed/train_base_v001.parquet`, `data/processed/test_base_v001.parquet`, `data/folds/folds_group_well_v001.csv`
- fold: `folds_group_well_v001.csv` の well 単位 Group fold
- target: `TVT - last_known_TVT`
- prediction: `last_known_TVT + pred_delta`
- 特徴量: `MD, X, Y, Z, GR, is_gr_missing, n_rows_in_well, known_length, hidden_length, last_known_TVT, last_known_MD, last_known_X, last_known_Y, last_known_Z, delta_MD_from_PS, delta_X_from_PS, delta_Y_from_PS, delta_Z_from_PS, post_ps_step, row_frac`
- 除外: `TVT`, `TVT_input`, `id`, `is_target`, `is_known_tvt`, `split`, `well_id`, `source_path`, `fold` など train-only marker / target-derived / ID 系列

## 結果

- overall CV RMSE: 15.054865
- fold mean RMSE: 15.042749
- fold std RMSE: 0.602631
- OOF rows: 3783989
- submission rows: 14151

## リーク懸念

target の真値 `TVT` は目的変数の delta 作成と valid 評価にのみ使用し、特徴量には入れていない。`is_target` や `is_known_tvt` など train/test の役割を直接示す marker columns も特徴量から除外した。`last_known_*` と `delta_*_from_PS` は PS 以前の anchor と各行の測定座標に基づく想定で、リーク懸念は低〜中。ただし base table 生成時に test 未知TVTや target 真値由来の情報が混入していないことを継続確認する。

## 次アクション

`feature_importance.csv` と OOF error slicing で、well長・hidden_length・PSからの距離別に誤差を見る。
