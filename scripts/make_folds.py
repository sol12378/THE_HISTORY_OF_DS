#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd

from rogii.data.split_strategy import make_group_folds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw/train.csv")
    parser.add_argument("--strategy", choices=["group_well", "group_typewell"], required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--n-splits", type=int, default=5)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    group_col = "well_id" if args.strategy == "group_well" else "typewell_id"
    if group_col not in df.columns:
        raise ValueError(f"Missing required group column: {group_col}")

    folds = df.copy()
    folds["fold"] = make_group_folds(df, group_col=group_col, n_splits=args.n_splits)
    keep_cols = [c for c in ["row_id", "well_id", "typewell_id", "fold"] if c in folds.columns]
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    folds[keep_cols].to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
