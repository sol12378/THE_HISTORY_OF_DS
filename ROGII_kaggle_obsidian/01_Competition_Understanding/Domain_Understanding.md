# Domain Understanding

The competition asks us to infer where the horizontal well is positioned within geological TVT space after the Prediction Start.

Key intuition:

- `MD` increases along the well path.
- `Z` describes physical vertical depth.
- `TVT` describes position relative to geological layering.
- `GR` behaves like a noisy geological fingerprint.
- `typewell` provides the reference GR curve on the TVT axis.

The core modeling question:

```text
After Prediction Start, is the well following the same layer, moving upward through layers, or moving downward through layers?
```
