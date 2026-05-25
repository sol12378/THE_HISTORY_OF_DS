from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from rogii.data.raw_inventory import parse_raw_filename, write_raw_inventory

HORIZONTAL_COLUMNS = ["MD", "X", "Y", "Z", "GR", "TVT_input", "TVT"]
BASE_VERSION = "v001"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _public_path(path: Path) -> str:
    parts = path.parts
    if "data" in parts:
        data_index = parts.index("data")
        return Path(*parts[data_index:]).as_posix()
    return path.as_posix()


def _write_meta(path: Path, df: pd.DataFrame, source_paths: list[str]) -> None:
    meta = {
        "version": BASE_VERSION,
        "created_at_utc": _utc_now(),
        "path": _public_path(path),
        "n_rows": int(len(df)),
        "n_cols": int(len(df.columns)),
        "columns": list(df.columns),
        "source_paths": source_paths,
        "split_counts": df["split"].value_counts(dropna=False).to_dict()
        if "split" in df.columns
        else {},
    }
    path.with_suffix(path.suffix + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _prediction_start_index(tvt_input: pd.Series) -> int | None:
    missing = tvt_input.isna()
    if not missing.any():
        return None
    return int(missing.idxmax())


def build_horizontal_base_for_file(path: Path, split: str) -> pd.DataFrame:
    parsed = parse_raw_filename(path)
    if parsed is None:
        raise ValueError(f"対象外のファイル名です: {path}")
    well_id, table_type = parsed
    if table_type != "horizontal_well":
        raise ValueError(f"horizontal_well ではありません: {path}")

    raw = pd.read_csv(path)
    df = pd.DataFrame(index=raw.index)
    df["split"] = split
    df["well_id"] = well_id
    df["row_idx"] = raw.index.astype("int64")
    df["source_path"] = _public_path(path)

    for column in HORIZONTAL_COLUMNS:
        df[column] = raw[column] if column in raw.columns else pd.NA

    ps_idx = _prediction_start_index(df["TVT_input"])
    n_rows = len(df)
    if ps_idx is None:
        ps_idx = n_rows
        known_length = n_rows
        hidden_length = 0
        is_target = pd.Series(False, index=df.index)
    else:
        known_length = ps_idx
        hidden_length = n_rows - ps_idx
        is_target = df["row_idx"] >= ps_idx

    anchor_idx = max(known_length - 1, 0)
    anchor = df.loc[anchor_idx, ["MD", "X", "Y", "Z", "TVT_input"]]

    df["TVT"] = pd.to_numeric(df["TVT"], errors="coerce")
    df["TVT_input"] = pd.to_numeric(df["TVT_input"], errors="coerce")
    df["id"] = pd.NA
    if split == "test":
        target_ids = df.loc[is_target, "row_idx"].map(lambda row_idx: f"{well_id}_{row_idx}")
        df.loc[is_target, "id"] = target_ids

    df["is_target"] = is_target.astype(bool)
    df["is_known_tvt"] = df["TVT_input"].notna()
    df["is_gr_missing"] = df["GR"].isna()
    df["ps_idx"] = int(ps_idx)
    df["n_rows_in_well"] = int(n_rows)
    df["known_length"] = int(known_length)
    df["hidden_length"] = int(hidden_length)
    df["last_known_TVT"] = anchor["TVT_input"]
    df["last_known_MD"] = anchor["MD"]
    df["last_known_X"] = anchor["X"]
    df["last_known_Y"] = anchor["Y"]
    df["last_known_Z"] = anchor["Z"]
    df["delta_MD_from_PS"] = df["MD"] - anchor["MD"]
    df["delta_X_from_PS"] = df["X"] - anchor["X"]
    df["delta_Y_from_PS"] = df["Y"] - anchor["Y"]
    df["delta_Z_from_PS"] = df["Z"] - anchor["Z"]
    df["post_ps_step"] = df["row_idx"] - ps_idx
    df.loc[df["row_idx"] < ps_idx, "post_ps_step"] = 0
    df["row_frac"] = df["row_idx"] / max(n_rows - 1, 1)
    return df


def build_typewell_base_for_file(path: Path, split: str) -> pd.DataFrame:
    parsed = parse_raw_filename(path)
    if parsed is None:
        raise ValueError(f"対象外のファイル名です: {path}")
    well_id, table_type = parsed
    if table_type != "typewell":
        raise ValueError(f"typewell ではありません: {path}")

    raw = pd.read_csv(path)
    df = raw.copy()
    df.insert(0, "source_path", _public_path(path))
    df.insert(0, "row_idx", raw.index.astype("int64"))
    df.insert(0, "well_id", well_id)
    df.insert(0, "split", split)
    df["n_rows_in_well"] = len(df)
    df["row_frac"] = df["row_idx"] / max(len(df) - 1, 1)
    return df


def _collect_base(raw_dir: Path, split: str, table_type: str) -> tuple[pd.DataFrame, list[str]]:
    paths = sorted((raw_dir / split).glob(f"*__{table_type}.csv"))
    builders = {
        "horizontal_well": build_horizontal_base_for_file,
        "typewell": build_typewell_base_for_file,
    }
    frames = [builders[table_type](path, split) for path in paths]
    if not frames:
        return pd.DataFrame(), []
    return pd.concat(frames, ignore_index=True), [_public_path(path) for path in paths]


def build_all_base_tables(
    raw_dir: str | Path = "data/raw",
    interim_dir: str | Path = "data/interim",
    processed_dir: str | Path = "data/processed",
) -> dict[str, Path]:
    raw_dir = Path(raw_dir)
    interim_dir = Path(interim_dir)
    processed_dir = Path(processed_dir)
    interim_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    inventory_path = interim_dir / "raw_inventory_v001.json"
    write_raw_inventory(raw_dir, inventory_path)

    outputs: dict[str, Path] = {"inventory": inventory_path}
    specs = [
        ("train", "horizontal_well", "train_base_v001.parquet"),
        ("test", "horizontal_well", "test_base_v001.parquet"),
        ("train", "typewell", "typewell_train_base_v001.parquet"),
        ("test", "typewell", "typewell_test_base_v001.parquet"),
    ]
    for split, table_type, filename in specs:
        df, source_paths = _collect_base(raw_dir, split, table_type)
        output_path = processed_dir / filename
        df.to_parquet(output_path, index=False)
        _write_meta(output_path, df, source_paths)
        outputs[filename] = output_path
    return outputs
