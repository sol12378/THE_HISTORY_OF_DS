# OOF分析ガイド

すべての実験でOOFに以下を保存する。

- `well_id`
- `row_idx`
- `fold`
- `TVT`
- `pred`
- `error`
- `abs_error`
- `TVT_input_isna`

必須集計:

- overall RMSE
- fold RMSE
- well RMSE
- bias
- Prediction Startからの距離別error
- GR欠損率別error
