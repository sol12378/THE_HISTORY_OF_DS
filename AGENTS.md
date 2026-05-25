# AGENTS.md

You are an experiment assistant for the ROGII Kaggle competition.

Always:

- Create one experiment at a time.
- Never modify raw data.
- Save all artifacts under `experiments/expXXX/`.
- Update `EXP_SUMMARY.md`.
- Update the Obsidian vault under `ROGII_kaggle_obsidian/` whenever the work changes project understanding, experiment results, feature ideas, CV policy, data engineering decisions, submissions, or next actions.
- Prefer fast experiments under 20 minutes.
- Do not optimize for public LB only.
- Explain leakage risks.

Before coding:

- Read `EXP_SUMMARY.md`.
- Read `ROGII_kaggle_obsidian/00_Index/Home.md` when it exists.
- Check the best previous experiment.
- State the exact hypothesis.
- Link the hypothesis to an Obsidian note under `03_Feature_Ideas/`, `04_CV_and_Evaluation/`, or `10_Data_Engineering/` when applicable.

After coding:

- Save `result.json`.
- Save `oof.csv`.
- Save `submission.csv` if applicable.
- Write `notes.md`.
- Update the matching experiment note in `ROGII_kaggle_obsidian/05_Experiments/`.
- Update `ROGII_kaggle_obsidian/06_PDCA/Daily_Log/YYYY-MM-DD.md` with Plan, Do, Check, Act notes.
- Update `ROGII_kaggle_obsidian/06_PDCA/Decision_Log.md` for any non-trivial decision.
- Update `ROGII_kaggle_obsidian/09_Submissions/LB_Tracking.md` after every Kaggle submission.

Obsidian logging rules:

- Write concise but specific notes: what changed, why it changed, what evidence supports it, and what should happen next.
- Record failed experiments and dead ends. They are part of the project memory.
- Separate leaderboard-only leakage checks from genuine validation results.
- Use Obsidian links such as `[[CV_Strategy]]`, `[[Anchor_Features]]`, and `[[exp003_lgb_anchor_trajectory]]`.
- Do not store large raw data, parquet files, model weights, OOF files, or submissions in Obsidian. Link to their paths in this repository instead.
