from pathlib import Path


def list_raw_files(data_dir: str | Path = "data/raw") -> list[Path]:
    return sorted(Path(data_dir).glob("*"))
