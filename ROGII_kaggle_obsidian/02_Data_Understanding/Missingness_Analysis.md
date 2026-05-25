# Missingness Analysis

Known facts:

- `TVT_input` becomes missing as a contiguous tail for each train well.
- Test submission rows exactly match missing `TVT_input` rows.
- `GR` has substantial missingness and should be treated as signal plus uncertainty.

Required checks:

- missing rate by well
- missing rate by pre-PS/post-PS region
- missing streak length
- relationship between GR missingness and OOF error
