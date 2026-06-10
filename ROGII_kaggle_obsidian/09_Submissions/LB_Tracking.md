# LB Tracking

| Date | Submission | Source Exp | CV | LB | Gap | Notes |
|---|---|---|---:|---:|---:|---|
| 2026-05-25 | `submission.csv` | [[exp003_lgb_anchor_trajectory]] | 15.054865 | 14.147 | -0.908 | Kaggle Notebook version 3から提出。Notebook-only competitionのためCSV直接提出ではなくcode submissionを使用。 |
| 2026-06-07 | exp072_proj | [[exp068]] | 9.086 | **8.280** | 0.806 | 現best LB。exp051 blend + projection。 |
| 2026-06-10 | exp073_blend | [[exp073_public_assets_integration]] | 8.79 | **8.630** | +0.16 | **棄却(LB悪化)**。CV改善(9.086→8.79)もLB悪化(8.280→8.630)=負の転移。外部OOF(rav/pilk)が「imputer fold毎非再構築」で膨張→favorable transfer消失。**確定best=exp072 8.280のまま**。教訓: 借り物外部OOFはCV-LB転移を壊す |
