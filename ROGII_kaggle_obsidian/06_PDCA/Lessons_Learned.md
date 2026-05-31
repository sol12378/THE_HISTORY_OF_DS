# Lessons Learned

- LB用のリーク確認と本物のmodeling判断を分離する。
- 各wellは独立行ではなくsequenceとして扱う。
- serious experimentでは必ずOOFを保存する。
- **feature importance が高くても汎化に有効とは限らない**。CV悪化時はimportanceを根拠に残さない（exp009b: Group E が gain上位なのにCV悪化）。
- **GroupKFoldのgroup単位は「ラベルが共有される最小単位」で切る**。well_idで切っても、複数wellが同一typewell曲線を共有していればtypewell由来特徴量はリークする（exp011で +0.15 過大評価を実証）。外部参照テーブル由来の特徴量を作るときは、その参照の重複を必ず先に検出する。
- **OOFの層別分析は両端だけでなく多数派の中域も見る**。exp009は corr>0.85/<0.60 の両端だけ見て、多数派の中域(0.60-0.85)の静かな劣化を見落とした（exp010で判明）。
- **per-well一意の連続値特徴量はoverfitしやすい**。長尺hard wellでは較正バイアスが外挿で累積し誤差を増幅する。
- **リーク検証は difference-in-differences で fold構成ノイズを相殺する**。同一foldで「特徴量あり/なし」を学習し、fold方式間でgapの変化を見る（exp011）。
