from pathlib import Path

import pandas as pd


def load_raw(data_dir: str | Path = "data/raw") -> dict[str, pd.DataFrame]:
    data_dir = Path(data_dir)
    tables = {}
    for path in sorted(data_dir.glob("*.csv")):
        tables[path.stem] = pd.read_csv(path)
    return tables
