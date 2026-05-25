# exp001_anchor_baseline

## 目的

[[Anchor_Features]] の最小構成として、target rows の `TVT` を `last_known_TVT` だけで予測する基準線を作る。

## 仮説

PS直前の既知TVTを水平に延長するだけでも、後続の delta model が超えるべき下限性能として有用。

## 変更内容

- 入力: `data/processed/train_base_v001.parquet`, `data/processed/test_base_v001.parquet`, `data/folds/folds_group_well_v001.csv`
- 予測: `pred_tvt = last_known_TVT`
- 評価: `is_target=True` の行だけで TVT絶対値RMSE

## 結果

- overall CV RMSE: 15.909853
- fold mean RMSE: 15.887139
- fold std RMSE: 0.854557
- OOF rows: 3783989
- submission rows: 14151

## リーク懸念

`last_known_TVT` は target 区間より前の既知TVTから作られた anchor であり、target row の真値TVTや test の未知TVTは使っていない。リーク懸念は低い。ただし base table 生成ロジックが PS 以後の真値を参照していない前提に依存する。

## 次アクション

`TVT - last_known_TVT` を目的変数にした LightGBM baseline と比較し、anchor からの改善量を見る。
