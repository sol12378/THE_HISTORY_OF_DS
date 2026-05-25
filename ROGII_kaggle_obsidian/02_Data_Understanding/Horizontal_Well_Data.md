# Horizontal Well Data

Horizontal well rows are ordered points along the well path.

Core columns:

- `MD`: measured depth along the well.
- `X`, `Y`, `Z`: 3D position.
- `GR`: gamma ray log, often missing.
- `TVT_input`: known before Prediction Start, missing after it.
- `TVT`: train target.

Training target rows are usually:

```text
TVT_input is NaN
```

Prediction Start is the first row where `TVT_input` becomes missing.
