# exp004_oof_error_slicing

## 目的

`exp003_lgb_anchor_trajectory` のOOFを、well別・hidden_length別・trajectory形状別に分解し、CVを落としている原因を特定する。

## 仮説

overall CVの悪化は全wellに均等に出るのではなく、long tailや曲がりの強いtrajectoryを持つ一部wellに集中している。

## 結果サマリ

- model RMSE: 15.054865
- anchor RMSE: 15.909853
- RMSE improvement vs anchor: 0.854988
- model MAE: 10.655868
- model bias: -0.109339
- rows: 3,783,989
- wells: 773

## 主要成果物

- `well_error_report.csv`
- `hidden_length_error_report.csv`
- `trajectory_shape_error_report.csv`
- `worst_wells_top30.csv`

## リーク懸念

OOF予測、anchor予測、train base tableのtarget-row metadataのみを使った後処理分析。モデル学習やsubmission生成には使っていないためリーク懸念は低い。ただし、この分析から作る特徴量は必ずtrain/test両方で同じ定義にする。
