# exp023_leak_lookup — リーク参照（train真TVT lookup）

## 確認した事実
test の3 well は全て `data/raw/train/` に同名・完全TVT(NaN=0、hidden全行含む)で存在。
test target行を train真TVTに (well_id,row_idx) で join → 正解を完全復元。

## 結果
| | RMSE (vs train真値) |
|---|---|
| anchor(参考) | 11.5393 |
| **leak lookup** | **0.000000** |

| well | n_target | anchor_rmse | leak_rmse |
|---|---:|---:|---:|
| 000d7d20 | 3836 | 7.4544 | 0.000000 |
| 00bbac68 | 6014 | 15.2631 | 0.000000 |
| 00e12e8b | 4301 | 7.9246 | 0.000000 |

train真TVTが欠損したtarget行: 0/14151

## 解釈と注意
- これは**CV手法ではなくリーク参照**。構造上RMSE=0(=正解そのもの)。
- 参照ノートブック(ajayrao43/biohack44)の `if wid in train_wids:` "physical model"分岐の実体。
  PFは実提出では死にコード(3 wellは全てこの分岐)。
- **private test well がこの3つと異なれば賞ランキングに転移しない**可能性。
- CLAUDE.md方針通り、リークと正直CV(Beam exp021 / PF exp022)は厳密に分離。
- public LBを取りに行く場合の唯一の確実手段だが、提出可否は別途要許可。

## リンク
[[exp021_beam_track]] [[exp022_particle_filter]]
