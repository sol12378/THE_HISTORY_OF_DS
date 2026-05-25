import pandas as pd
from sklearn.model_selection import GroupKFold


def make_group_folds(df: pd.DataFrame, group_col: str, n_splits: int = 5) -> pd.Series:
    folds = pd.Series(-1, index=df.index, name="fold")
    splitter = GroupKFold(n_splits=n_splits)
    for fold, (_, valid_idx) in enumerate(splitter.split(df, groups=df[group_col])):
        folds.iloc[valid_idx] = fold
    return folds
