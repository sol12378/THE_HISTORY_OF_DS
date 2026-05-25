# Leakage-Safe ETL

## Leakage Definition

Leakage occurs when a feature uses information that would not be available at test prediction time.

## High-Risk Sources

- future `TVT`
- post-PS `TVT_input`
- train-only formation marker columns used as ordinary features
- train-only `Geology`
- duplicated public test wells in train
- row-random validation

## Safe Anchor Construction

For each well:

1. detect `ps_idx`
2. use rows `< ps_idx` for anchor and pre-PS slope
3. never use rows `>= ps_idx` except current row's allowed test-time fields: `MD`, `X`, `Y`, `Z`, `GR`

## Safe Rolling Features

GR rolling features can use current and local GR if those values exist in test.

TVT rolling features must be restricted to pre-PS observed `TVT_input`. Do not compute target-side rolling statistics using hidden train `TVT` after PS unless the feature is explicitly training-only for analysis.

## Validation Safety

Group split must occur before any target-aware aggregation. If a feature aggregates target information across wells, compute it fold-wise.
