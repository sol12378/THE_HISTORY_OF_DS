# CLAUDE.md

## Project

ROGII - Wellbore Geology Prediction

## Goal

信頼できるCVをもとに、ROGIIのPublic/Private LBを改善する。

## Language Rule

- 思考内容、仮説、変更内容、実験結果、解釈、次アクションなど、人間向けに言語化する内容は原則として日本語で記録する。
- `ROGII_kaggle_obsidian/` に書く文章も日本語を基本とする。
- コード、ファイル名、列名、設定キー、Kaggle公式用語、ログ出力は必要に応じて英語のまま残してよい。

## Orchestration Rule

- メインエージェントはオーケストラとして振る舞い、設計、分担、レビュー、統合、品質判断を担当する。
- 実装作業が分割できる場合はworkerを使う。
- workerを使う場合、原則として推論レベルはlowにする。
- workerの成果物はメインエージェントが必ず確認し、品質基準を満たさない場合は修正を指示する。
- 目標達成までPlan / Do / Check / Actを回し、途中で止めずに品質ゲートを満たすまで改善する。
- GitHubなど外部リモートへのpushは、必ずユーザーの明示許可を得てから行う。

## Non-negotiable Rules

- `data/raw` は絶対に変更しない
- 成果物、コミット、Obsidianノート、提出物に個人情報・秘密情報・公開リポに含めてはいけないものを入れない
- `.env`、`.kaggle/`、API key、access token、個人の絶対パス、raw Kaggle data、processed parquet、model artifact、OOF、submissionは公開リポに含めない
- commit前に `git status`、staged files、秘密情報スキャンを確認する
- GitHubなど外部リモートへのpushは、必ずユーザーの明示許可を得てから行う
- row random CVは禁止
- 実験は1回につき1目的だけ変更する
- 実験結果は必ず `experiments/expXXX/` に保存する
- OOF、submission、`result.json`、`notes.md`を必ず出力する
- `EXP_SUMMARY.md`を毎回更新する
- `ROGII_kaggle_obsidian/` に思考内容、仮説、変更内容、実験結果、解釈、次アクションを必ず記録する
- CV改善だけで判断せず、リーク懸念をnotesに書く
- 学習時間は原則20分以内。重い実験は事前に明記する
- 既存の良い実験を壊さない
- feature追加時はablationできるようにfeature set名を分ける

## Preferred Workflow

1. `EXP_SUMMARY.md`を読む
2. `ROGII_kaggle_obsidian/00_Index/Home.md`を読む
3. 直近のbest CV / best LB / leak_risk実験を把握する
4. 新しいexp_idを作る
5. configを作る
6. 実験を実行する
7. `result.json` / `oof.csv` / `submission.csv` / `notes.md`を保存する
8. `EXP_SUMMARY.md`を更新する
9. `ROGII_kaggle_obsidian/05_Experiments/` の該当実験ノートを更新する
10. `ROGII_kaggle_obsidian/06_PDCA/Daily_Log/YYYY-MM-DD.md` にPlan/Do/Check/Actを記録する
11. 次の改善案を3つだけ提案する

## Obsidian Knowledge Rules

Obsidian vault: `ROGII_kaggle_obsidian/`

必ず記録するもの:

- コンペ理解・データ理解が更新された内容
- 新しい仮説と、その仮説が生まれた理由
- 実装した変更内容
- 実験config、CV、LB、OOF分析、失敗理由
- リーク懸念、CV-LB gap、採用/棄却判断
- 次にやること

更新先の目安:

- コンペ/評価/ドメイン理解: `01_Competition_Understanding/`
- データ構造/欠損/EDA: `02_Data_Understanding/`
- 特徴量案: `03_Feature_Ideas/`
- CV/評価方針: `04_CV_and_Evaluation/`
- 実験結果: `05_Experiments/`
- 日々のPDCAと意思決定: `06_PDCA/`
- 失敗分析: `07_Error_Analysis/`
- 提出結果: `09_Submissions/`
- データ基盤/ETL/処理設計: `10_Data_Engineering/`

Obsidianには巨大ファイルを置かない。raw data、parquet、model、OOF、submissionはコードリポジトリ内に保存し、Obsidianからパスで参照する。

## Important Concepts

- GroupKFold by well_id
- GroupKFold by typewell_id
- last_known_TVT anchor
- typewell duplicate detection
- OOF error slicing
- CV-LB gap
- tree model blend
