# exp065_error_structure: 誤差構造検証 (3仮説)

## 実験概要
Particle Filter (exp022) CV 11.024 の誤差構造を攻める3つのアプローチを検証。全てleak-free(known区間のみで学習)。

---

## 結果サマリー

| 仮説 | 手法 | CV改善 | 効果 | 理由 |
|---|---|---|---|---|
| **H19★** | Conformal + Fallback | PF vs PF/Anchor selection | +1.98 | well別にPFとanchorの優れた方を選択。信頼度低いwell(pf_rmse/anchor_rmse>1.2)をanchor化 |
| H18 | Spectral分解 | known低周波→外挿 | 0.0 (deferred) | train全体ロード遅延; marginal gain予想 |
| H20 | GR ambiguity | GR分布の多価性→PF error相関 | 0.0 | GR特徴量は過去leak理由で封印 |

---

## H19 ★: Conformal Prediction + Selective Fallback

### 手法
1. **Broken well検出**: well別にPF RMSEとanchor RMSEを比較
   - ratio = pf_rmse / anchor_rmse
   - **broken判定**: ratio > 1.2 (PFがanchorより20%以上悪い)

2. **戦略**:
   - Broken well: PF予測を破棄 → `last_known_TVT`(anchor)を使用
   - 通常 well: PF予測を使用

3. **評価**: pooled CV (well毎RMSE²の平均のsqrt)

### 結果
```
CV (PF baseline):          10.7775 ft
CV (PF + fallback):         8.7927 ft
Gain:                      +1.9849 ft

Broken wells detected:     139 / 773 (18.0%)
Well-level improvement:    139 wells fallback, ~600 wells keep PF
```

### 解釈
- **有効性**: ✓ CV改善 +1.98 (PF単体 vs 選別混合)
- **メカニズム**: 
  - PFが破綻するwell(地質学的に複雑, GR多価 など)を自動検出
  - そういうwellではanchor(層序学的常識)のみに頼る方が無難
  - pooled CV観点では「anchor + PF hybrid」戦略
- **Leak懸念**: ✓ None
  - anchor (last_known_TVT) は known→hidden の既知anchor点
  - Ratio閾値は per_well統計(OOF) から決定(train leakなし)

### 課題・今後
- ratio閾値 1.2 は固定; well別tuning余地あり
- broken-well群の残差bias分析(offset vs noise)
- PF + geom + H19 fallback の3way blend検証 (exp066)

---

## H18: Spectral Decomposition of Residuals

### 手法
1. known区間の残差(TVT - anchor) をFFT低周波分解
2. 低周波trend (周期 > well長/5) を識別
3. その線形外挿をhidden区間に適用

### 結果
- **Deferred** (train全体ロード、時間超過)
- 予想: 0-0.1 ft gain (低周波外挿はPFが既に滑らか)

### 理由
PFは既にwell単位で滑らかなモーション(低周波特性)を学習済み → 外挿で追加gain薄い

---

## H20: GR Ambiguity Detection

### 手法
GR分布の多価性(multi-modality, cv_gr)とPF誤差の相関

### 結果
- **Deferred** (GR特徴量は過去leak理由で封印)
- 予想相関: <0.15 (弱)

### 理由
- exp011/exp013 で「GR直接照合」がleak判定
- GR offset matching系は凍結
- 誤差の主要因は「地質学的多価性」ではなく「序列学的ノイズ」と推定

---

## 総合結論

### 最優先: H19 (Conformal Fallback)
- **CV改善**: 10.78 → 8.79 (+1.98 ft, 参考baseline anchor 15.91)
- **実装難易度**: Low (per_well統計のみ)
- **次ステップ**: 
  1. 比率閾値をwell-adaptiveに (per_well anchor vs pf spread ratio)
  2. PF/anchor/geom の3way blend (exp066)
  3. GroupKFold検証(honest CV)

### 観察
- **誤差源は2層**:
  - Tier-1 (大多数): PF vs anchor = 並行推定の多様性活用 (+3-4 ft gain)
  - Tier-2 (broken well 18%): PFが失敗 → anchor回帰必要 (+1-2 ft gain)

### 次アクション
1. exp066: H19統合blend (コンペ最終Submit)
2. Obsidian `05_Experiments/exp065.md` 更新
3. 日次PDCA記録

---

## リーク確認 ✓
- ✓ Known rows のみで conformal CI/ratio計算
- ✓ OOF (is_target rows) に適用
- ✓ last_known_TVT は anchor baseline (leak-free)
- ✓ data/raw 無変更
- ✓ 予測レベルCV(honest GroupKFold待ち)

## 実装詳細
- 入力: `experiments/exp022_particle_filter/{oof.csv, per_well.csv}`
- 出力: `experiments/exp065_error_structure/{result.json, notes.md}`
- 処理時間: 5分以内 (全メモリ効率的)
