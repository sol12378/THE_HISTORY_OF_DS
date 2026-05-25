# Anchor Features

## Hypothesis

Prediction Start just before missing `TVT_input` contains the strongest information about future TVT.

## Candidate Features

- `last_known_TVT`
- `last_known_MD`
- `last_known_X`
- `last_known_Y`
- `last_known_Z`
- `delta_MD_from_PS`
- `delta_X_from_PS`
- `delta_Y_from_PS`
- `delta_Z_from_PS`
- `pre_PS_TVT_slope`
- `pre_PS_TVT_curvature`

## Target Transform

Prefer:

```text
target_delta = TVT - last_known_TVT
```
