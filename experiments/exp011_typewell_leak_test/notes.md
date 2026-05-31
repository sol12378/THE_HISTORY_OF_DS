# exp011_typewell_leak_test: typewell リーク検証

## 設計
- 重複 typewell グループを単一 fold に集約した deduped fold を構築 (18 wells 移動)。
- 同じ deduped fold 上で exp008 特徴量(E無し)と exp009b 特徴量(E有り)を学習。
- E の悪化幅が fold 方式で変わるかを比較してリークを判定。

## 結果

| fold 方式 | baseline (E無し) | E有り | E − baseline |
|---|---:|---:|---:|
| well-fold (既存) | 13.808621 | 13.932155 | +0.123534 |
| deduped (typewell集約) | 13.651645 | 13.928077 | +0.276432 |

- gap 変化 (deduped − well): +0.152898
- **判定: LEAK_CONFIRMED: E penalty grows under deduped folds**

## baseline fold 別 (deduped)
| fold | rmse | best_iter |
|---|---:|---:|
| 0 | 12.493308 | 587 |
| 1 | 13.712834 | 380 |
| 2 | 13.135460 | 243 |
| 3 | 13.806890 | 574 |
| 4 | 14.865294 | 1012 |

## E fold 別 (deduped)
| fold | rmse | best_iter |
|---|---:|---:|
| 0 | 13.219213 | 416 |
| 1 | 13.877111 | 121 |
| 2 | 13.286750 | 109 |
| 3 | 13.981802 | 772 |
| 4 | 15.074513 | 1284 |

## 解釈
- gap が +0.02 以上拡大 → well-fold が共有 typewell リークで E を過大評価していた。
- gap がほぼ不変 → リークは軽微、悪化は overfit。Group E 封印の妥当性を補強。
