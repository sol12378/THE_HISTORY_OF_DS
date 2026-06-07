# exp065_error_structure — 誤差構造検証 (3仮説)

## タスク
Particle Filter (exp022) CV 11.024 の誤差を攻める3つの仮説を検証（leak-free）。

## 3つの仮説

### H19 ★ PRIORITY: Conformal Prediction + Selective Fallback
**仮説**: known区間の残差分布からconformal予測区間を構築 → CI幅が広い(信頼度低い)well = "broken"と判定 → そういうwellをanchor/geomにフォールバック

**狙い**: 過去「broken well AUC 0.5 gateの代替」という課題の、leak-freeな解法

**実装**: 
1. 各wellのknown区間で予測残差をとる(TVT - pred)
2. 残差の90%分位を使い conformal CI幅 = 2×Q90%
3. CI幅 > 15ft なら broken = True (閾値tunable)
4. broken well では pred_tvt の代わりに last_known_TVT を使う(ゼロオフセット = anchor相当)
5. pooled RMSE & width vs pf_rmse 相関を測る

**評価基準**:
- CV改善(11.024 を超える)
- width vs pf_rmse 相関 > 0.225 = 「CI幅が実際の破損を予測している」

---

### H18: Spectral Decomposition of Residuals
**仮説**: known区間の残差をFFT低周波分解 → linear trendを外挿してhidden区間に補正

**狙い**: 低周波offset biasを捕捉

**評価**: CV改善量

---

### H20: Adversarial/Ambiguity Detection
**仮説**: GR多価性が強いwell(分布がmulti-modal)はPF誤差が大きい

**狙い**: GR ambiguity score vs PF RMSE の相関を測る

**評価**: 相関 > 0.225 なら viable

---

## 実装上の詳細

### Data Structure
- train_base_v001.parquet: 全行 (5.1M行), is_known_tvt フラグ付き
  - known: is_known_tvt == True (last_known_TVT anchor までの区間)
  - hidden: is_known_tvt == False (予測対象)
  
- exp022 oof.csv: is_target == True の行のみ (3.8M行, 全hidden)
  - 含まれるもの: TVT(truth), pred_tvt, last_known_TVT, error(TVT - pred)
  - missing: is_known_tvt, MD

### Leak-free Protocol
- conformal CI学習: known rows ONLY
- 予測は oof (is_target rows) に適用
- hidden TVT の「真値」は OOF に既に含まれている

---

## 予想される結果

### H19 期待値
- 相関 > 0.225 なら broken detection 成功
- CV: 11.024 → 10.8-10.9 (gain 0.1-0.2) が現実的

### H18 期待値
- 低周波外挿は marginal (既にPFが滑らか)
- gain < 0.1

### H20 期待値
- GR ambiguity は weak (<0.15)
- GR特徴量は過去封印 (leak 理由)

---

## リーク確認チェック
- ✓ known rows のみで conformal CI学習
- ✓ GR分析も known rows only
- ✓ data/raw 無変更
- ✓ fallback (last_known_TVT) は anchor baseline 同等

---

## 次アクション
1. H19 の width 閾値(現在 15ft)を well毎に tuning
2. broken-well subgroup の残差bias分析
3. PF + H19 fallback を geom/anchor と blend (exp066)
