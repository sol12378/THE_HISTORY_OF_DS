# Leakage-Prone Features

Do not blindly use:

- `TVT`
- future `TVT_input`
- train-only formation marker columns
- train-only `Geology` labels as direct test features
- well IDs that memorize the leaked public test rows

Allowed use:

- analysis
- error slicing
- target construction in train
- controlled leak-check submissions clearly marked as `leak_risk`
