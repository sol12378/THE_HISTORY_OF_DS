# Data Quality Checks

## Raw Inventory Checks

- train horizontal count と train typewell count が一致する。
- すべてのtrain wellにPNGがある。
- test horizontal count と test typewell count が一致する。
- sample submission IDs が test wells と row indices に対応する。

## Horizontal Checks

- required columnsが存在する。
- `MD` が単調増加している。
- `row_idx` が重複しない。
- `TVT_input` の欠損tailが連続している。
- trainではPrediction Start以前の `TVT_input` が `TVT` と一致する。
- target rowsが空ではない。
- GR missingnessを記録する。

## Typewell Checks

- required columnsが存在する。
- `TVT` と `GR` がnon-nullである。
- `TVT` range が関連するhorizontal wellのTVT rangeと重なる。
- duplicate TVT valuesを明示的に扱う。

## Train/Test Parity Checks

- model feature columns がtrain/test両方に存在する。
- test matrixにtarget columnを入れない。
- submission IDs が sample submission と完全一致する。

## 実験artifact checks

実験を信頼する前に確認すること:

- OOF row count が training target row count と一致する。
- fold column が期待foldを持つ。
- 同一fold内でvalidation wellがtrainingに入らない。
- submission row count が sample submission row count と一致する。
- submission IDs が sample submission と完全一致する。
