from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class RawFileRecord:
    split: str
    well_id: str
    table_type: str
    source_path: str
    n_rows: int
    n_cols: int
    columns: list[str]


def parse_raw_filename(path: Path) -> tuple[str, str] | None:
    """`{well_id}__{table_type}.csv` 形式だけを対象にする。"""
    stem = path.stem
    if "__" not in stem:
        return None
    well_id, table_type = stem.split("__", 1)
    if table_type not in {"horizontal_well", "typewell"}:
        return None
    return well_id, table_type


def public_path(path: Path) -> str:
    parts = path.parts
    if "data" in parts:
        data_index = parts.index("data")
        return Path(*parts[data_index:]).as_posix()
    return path.as_posix()


def iter_raw_csv_files(raw_dir: str | Path = "data/raw") -> list[Path]:
    raw_dir = Path(raw_dir)
    paths: list[Path] = []
    for split in ("train", "test"):
        paths.extend((raw_dir / split).glob("*__*.csv"))
    return sorted(paths)


def build_raw_inventory(raw_dir: str | Path = "data/raw") -> dict[str, object]:
    raw_dir = Path(raw_dir)
    records: list[RawFileRecord] = []
    for split in ("train", "test"):
        for path in sorted((raw_dir / split).glob("*__*.csv")):
            parsed = parse_raw_filename(path)
            if parsed is None:
                continue
            well_id, table_type = parsed
            df = pd.read_csv(path, nrows=5)
            n_rows = sum(1 for _ in path.open("r", encoding="utf-8")) - 1
            records.append(
                RawFileRecord(
                    split=split,
                    well_id=well_id,
                    table_type=table_type,
                    source_path=public_path(path),
                    n_rows=n_rows,
                    n_cols=len(df.columns),
                    columns=list(df.columns),
                )
            )

    summary: dict[str, object] = {
        "version": "raw_inventory_v001",
        "raw_dir": public_path(raw_dir),
        "n_files": len(records),
        "by_split_table": {},
        "files": [asdict(record) for record in records],
    }
    by_split_table: dict[str, int] = {}
    for record in records:
        key = f"{record.split}/{record.table_type}"
        by_split_table[key] = by_split_table.get(key, 0) + 1
    summary["by_split_table"] = by_split_table
    return summary


def write_raw_inventory(
    raw_dir: str | Path = "data/raw",
    output_path: str | Path = "data/interim/raw_inventory_v001.json",
) -> dict[str, object]:
    inventory = build_raw_inventory(raw_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return inventory
