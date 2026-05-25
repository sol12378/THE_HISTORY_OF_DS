# Leakage and Risks

## Known Leakage Risk

The current downloadable test wells are also present in train:

- `000d7d20`
- `00bbac68`
- `00e12e8b`

The train files contain `TVT` for rows that appear in sample submission. Any direct lookup submission must be marked `leak_risk` and used only to verify submission mechanics.

## Train-Only Columns

These horizontal-well columns are train-only:

- `ANCC`
- `ASTNU`
- `ASTNL`
- `EGFDU`
- `EGFDL`
- `BUDA`
- `TVT`

Do not use them as ordinary production features unless equivalent test-side values are generated without leakage.
