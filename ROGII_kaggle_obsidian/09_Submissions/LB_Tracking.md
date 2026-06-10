# LB Tracking

| Date | Submission | Source Exp | CV | LB | Gap | Notes |
|---|---|---|---:|---:|---:|---|
| 2026-05-25 | `submission.csv` | [[exp003_lgb_anchor_trajectory]] | 15.054865 | 14.147 | -0.908 | Kaggle Notebook version 3から提出。Notebook-only competitionのためCSV直接提出ではなくcode submissionを使用。 |
| 2026-06-07 | exp072_proj | [[exp068]] | 9.086 | **8.280** | 0.806 | 現best LB。exp051 blend + projection。 |
| 2026-06-10 | exp073_blend (running) | [[exp073_public_assets_integration]] | **8.79** | 実行中 | - | sol12378/rogii-exp073-blend。exp026(pf+geom)+ravaghi(lgb3/cb1/cb2)+pilkwang(cat) 固定重みblend+projection。pilk_tcnは採点時再現不能で除外・再fit。leak-free。joint OOF 8.69。目標LB<=7.419 |
