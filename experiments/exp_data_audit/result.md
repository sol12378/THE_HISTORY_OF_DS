# データ精査結果 (exp_data_audit)

**目的**: exp034 LB乖離の原因検証  
**実施日**: 2026-06-05  
**担当**: Data Audit Worker

---

## 1. 全カラム列挙 & 未使用カラム調査

### 結論: **未使用カラムなし（既知カラムが全て）**

| ファイル | カラム | 形態 |
|---------|--------|------|
| train horizontal_well | MD, X, Y, Z, ANCC, ASTNU, ASTNL, EGFDU, EGFDL, BUDA, TVT, GR, TVT_input | 13列 |
| test horizontal_well | MD, X, Y, Z, GR, TVT_input | 6列 |
| train typewell | TVT, GR, Geology | 3列 |
| test typewell | TVT, GR | 2列 |

### 既使用カラム
`MD, X, Y, Z, GR, TVT, TVT_input, ANCC, ASTNU, ASTNL, EGFDU, EGFDL, BUDA, Geology`

### 未使用カラム
**なし** — 全カラムが既に feature engineering 対象 または target 関連。

**評価**: 隠れた新情報なし。data leak はカラム追加ではなく、別系統から流入している可能性高い。

---

## 2. 空間座標近傍分析

### 発見: **3つのtest wells すべてが train wells の近傍に存在**

| Test well | 座標 (X_mean, Y_mean) | 最近傍 train well | 距離 (m) | 次近傍 | 距離 |
|-----------|----------------------|------------------|---------|--------|------|
| 000d7d20 | (2983513.9, 1071417.7) | ff0aea78 | **466.5** | 32fe84c9 | 2430.1 |
| 00bbac68 | (3008500.4, 1086928.4) | 00bbac68 | 0.0 (自身) | 155887bb | 1010.0 |
| 00e12e8b | (2969568.6, 1062552.7) | 42669188 | **370.4** | 8cc21f01 | 3249.7 |

### **重要**: 距離 < 500m の隣接well

- `000d7d20` ← `ff0aea78` (dist 466.5)
- `00e12e8b` ← `42669188` (dist 370.4)

これらの train wells は、対応する test wells と **ほぼ同じ地層セクション（TVT値）** をカバーしている。

---

## 3. train vs test CSV 構造差分

### 3.1 TVT カラムの有無

**train CSV には TVT があるが、test CSV には TVT がない**

```
Test horizontal_well:  [MD, X, Y, Z, GR, TVT_input]           ← TVT欠落
Train horizontal_well: [MD, X, Y, Z, ANCC, ..., TVT, GR, TVT_input] ← TVT あり
```

**test typewell には Geology カラムがない**

```
Test typewell:  [TVT, GR]            ← Geology欠落
Train typewell: [TVT, GR, Geology]   ← Geology あり
```

### 3.2 TVT_input の一致性

3つの test wells ともに、train CSV の TVT_input と完全一致：

| Test well | TVT_input rows (not null) | 対応 train CSV TVT_input |
|-----------|--------------------------|----------------------|
| 000d7d20 | 1442 | 完全一致 ✅ |
| 00bbac68 | 1545 | 完全一致 ✅ |
| 00e12e8b | 2083 | 完全一致 ✅ |

**解釈**: known section (TVT_input not null) は train/test で同一 → **train CSV の TVT 情報が test wells の"正解"として存在する**。

---

## 4. 隣接train wells とのTVT重複分析

### **重大発見: 隣接 train wells が test wells の地層セクションと重複**

| Test well | 隣接 train well | TVT重複数 | 重複率 |
|-----------|-----------------|----------|--------|
| 000d7d20 | ff0aea78 | 327/1442 | **22.7%** |
| 00e12e8b | 42669188 | 504/2083 | **24.2%** |

**重複TVT例** (000d7d20 - ff0aea78):
```
11388.21, 11404.7, 11414.28, 11518.87, 11592.3, ...
```

**解釈**:
- 隣接 train wells は、test wells の known section と **大量の共通TVT値を持つ**。
- これは地質的に「**同じ地層面を両well が貫いている**」ことを意味する。
- 距離 466m, 370m は業界的には「同一構造ブロック」（offsetwell相当）。

---

## 5. PNG メタデータ & 外部リソース

### PNG ファイル

| 分類 | 有無 | 備考 |
|-----|-----|------|
| test PNG | ❌ なし | test 側には PNG 画像がない |
| train PNG | ✅ あり (773 ファイル) | 1枚あたり ~800KB。geological cross-section plot。 |

**train PNG の内容** (サンプル: 000d7d20.png):
```
- Gamma Ray Log (深度軸: MD 0-5000m)
- TVT plot (赤・青の交差記号列で個別解釈点を表示)
- Well Path Projection (水平井の坑跡)
- 色分けされた地層解釈線（構造断面）
```

**評価**: PNG は geosteering interpretation を行うための reference image。train/test 対称性なし（test には PNG がない）。

### 外部リソース

- **ROGII公開資源**: docs/ROGII_geosteering_domain_knowledge.md に業界標準ワークフロー（typewell選択, multi-hypothesis, DTW+dip）を記載。
- **公開論文**: URTeC 1590259, SPWLA standard （ROGII doc で参照）。
- **ドメイン知識**: 100年近い「GR well-to-well correlation」は確立手法。

---

## 6. 構造リーク仮説の検証

### H2: 別系統 leak (train TVT が test に流入)

**確度: 高い**

根拠:
1. train CSV に `TVT` カラムが存在。test には ない。
2. test wells 3つとも train CSV に記録されている（構造的 leak）。
3. test known section (TVT_input) は train CSV の TVT と数値レベルで一致。
4. **隣接 train wells (ff0aea78, 42669188) の TVT が test TVT_input と大量重複** → 同じ地層セク内のwell間対比により、間接的に test wells の TVT が推定可能な構造。

**leak pathway の仮説**:
```
train.TVT (train CSV の known section)
    ↓
隣接 train wells の地層 geometry / GR correlation
    ↓
test wells の TVT_input を補外 / typewell対比で推定
```

### H3: External data（公開 well database）

**確度: 低い**

根拠:
- README に「data/raw は Kaggle downloads」と明記。
- PNG や CSV フォーマットに公式データベース形式の痕跡なし。
- ドメイン知識ドキュメントは ROGII 業界ドメインであり、外部ソースの直接利用ではない。

---

## 7. 1位解法 (LB 5.986) への示唆

SaintLouis 1位は LB 5.986 を達成（vs exp026: 8.672）。既知の leak を超える手段：

### 仮説A: Multi-hypothesis PF + 隣接well typewell

上記の「隣接 train wells との重複」を活用:
```
Well 000d7d20 の typewell 候補:
  1. 最初の typewell (現在の 000d7d20 自身のtypewell)
  2. 隣接 train well ff0aea78 の 000d7d20 用typewell変換
  3. 他の空間近傍 train wells
     
→ 複数 typewell で並列 PF → 尤度加重平均
```

**効果**: よりロバストな TVT offset 推定。隣接well の「地層確度」を活用。

### 仮説B: PNG 構造線抽出 + 独立回帰

train PNG に描かれた interpretation line（構造面）を CNN で抽出 → TVT-MD 関係を別シグナルとして feed。
（ドメイン知識 doc に「当たれば −1.0以上の伸び」と示唆。）

### 仮説C: 多層 typewell 割り当て (ROGII GeoAssist の再現)

ROGII 公式ドキュメント曰く:
> 「自動で最も近い typewell を見つけ、複数 offset well から複数解釈を構築し最良相関を選ぶ」

⇒ **well 単位でなく, layer unit 単位で typewell を切り替える** 設計。

---

## 結論

| 項目 | 発見 |
|-----|------|
| **未使用カラム** | なし（leak はカラム追加でない） |
| **空間構造** | test wells は train wells 近傍に密集（466m, 370m） |
| **train-test 差分** | TVT カラムが test から欠落。TV_input は一致 |
| **隣接well との重複** | **ff0aea78, 42669188 の TVT が 22-24% 重複** ✅ |
| **PNG** | geosteering interpretation。train のみ。test には なし |
| **新情報** | **なし**（既知の leak パターンを超える新情報は検出されず） |

### 最終評価

exp034 LB乖離 (10.794) の主因は、引き続き **train TVT leak の利用有無**。
新シグナル源ではなく、既知パターンの活用度（multi-typewell, dip補正, typewell選択基準）に差あり。

1位 (5.986) の達成には:

1. **Multi-hypothesis typewell blend** (隣接/空間近傍 train wells の活用)
2. **PNG 構造線抽出** (独立回帰シグナル) 
3. **Well単位 → Layer単位の typewell 割り当て**

を組み合わせた、より精密なPFが必要と判定。

---

## 計算時間

- 全カラム列挙: ~1s
- 空間近傍分析 (773 train wells): ~3s
- train/test CSV差分: ~5s
- 隣接well TVT比較: ~3s
- PNG確認: ~1s

**合計: ~13秒（予定15-20分に対し大幅高速化）**
