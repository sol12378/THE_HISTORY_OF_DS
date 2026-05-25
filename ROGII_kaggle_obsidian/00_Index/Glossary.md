# Glossary

## Core Terms

- `MD`: Measured Depth, distance along the well path.
- `X`, `Y`, `Z`: 3D coordinates of each horizontal well point.
- `TVT`: True Vertical Thickness, the target geological coordinate.
- `TVT_input`: observed TVT before Prediction Start; missing after Prediction Start.
- `GR`: Gamma Ray log, a geological signature signal.
- `Typewell`: vertical/reference well containing `TVT` and `GR`.
- `Prediction Start`: first row where `TVT_input` becomes missing.
- `OOF`: out-of-fold predictions from local validation.

## Formation Labels

- `ANCC`, `ASTNU`, `ASTNL`, `EGFDU`, `EGFDL`, `BUDA`: formation marker names present in train horizontal files.
- `U` / `L`: likely upper/lower qualifier in geological labels.
- `TGT`: target interval label.
- `THL`, `BHL`: top/base or landing-related interval labels, treated as labels unless confirmed.
