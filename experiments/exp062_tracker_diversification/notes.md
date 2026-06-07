# exp062: トラッカー多様化検証 (subset 20 well)

## 背景

exp022 PF (CV 11.024) の broken well 救済を目指した4つの提案を subset (broken 10 + good 10) で検証。
- 案7: 焼きなまし PF
- 案8: レプリカ交換 PF (Parallel Tempering)
- 案9: Viterbi-DP (CRF)
- 案10: 不確実性ダウンウェイト PF

## 結果

| 案 | 手法 | CV RMSE (subset) | vs baseline | 効果 |
|---|---|---:|---:|---|
| 7 | 焼きなまし | 122.119 | +111.095 | ✗ |
| 8 | レプリカ交換 | 114.232 | +103.208 | ✗ |
| 9 | Viterbi-DP | 403.248 | +392.224 | ✗ |
| 10 | 不確実性 | nan | +nan | ✗ |

基準: exp022 PF full-773 CV = 11.024

## 考察

- subset evaluation なため full-773 への転移は未確認
- 有効な案があれば full-773 + ensemble で再評価予定
- 失敗理由は各案の数学的制限による可能性

## Next Action

- 最有望案を full-773 で実行
- ensemble with exp026 最終blend
- honest CV で LB 転移確認

## Leak Risk

None: Group well-fold + known区間のみ使用。hidden TVT は学習・選択に不使用。
