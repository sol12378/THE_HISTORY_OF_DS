"""rogii_phaseA2.py -- Phase A2: fork (sp45, LB 7.625) + exp026 (PF x geom) blend.

Design: subprocess isolation.
  Step 1: Run fork script  -> fork_submission.csv
  Step 2: Run exp026 script -> exp026_submission.csv
  Step 3: blend 0.70 * fork + 0.30 * exp026 -> submission.csv

All ASCII. Kaggle (/kaggle/working, /kaggle/input) and local (data/raw) path-aware.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import time
from pathlib import Path

import numpy as np
import pandas as pd

# ─── Paths ────────────────────────────────────────────────────────────────────
_WORK = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")
_THIS_DIR = Path(__file__).parent.resolve()

FORK_SCRIPT = _THIS_DIR.parent / "exp080_sp45_fork" / "rogii_sp45_fork.py"
EXP026_SCRIPT = _THIS_DIR.parent / "exp072_proj" / "_decoded_exp026_b64.py"

FORK_SUB_PATH   = _WORK / "fork_submission.csv"
EXP026_SUB_PATH = _WORK / "exp026_submission.csv"
FINAL_SUB_PATH  = _WORK / "submission.csv"

LOG_DIR = Path(__file__).parent.parent.parent / "experiments" / "exp084_phaseA2"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_DIR / "build_log.txt"

BLEND_FORK   = 0.70
BLEND_EXP026 = 0.30

# ─── Logger ───────────────────────────────────────────────────────────────────
_log_lines = []

def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    _log_lines.append(line)

def flush_log():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(_log_lines) + "\n")

# ─── Subprocess runner ────────────────────────────────────────────────────────
def run_subprocess(script_path: Path, out_csv: Path, label: str,
                   env_extra: dict = None):
    """Run script in a fresh subprocess. Expected to write submission.csv to CWD."""
    log(f"[{label}] starting: {script_path}")
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    # Each sub-process runs in its own temp workdir so submission.csv paths
    # don't collide and can be collected separately.
    tmp_dir = Path(tempfile.mkdtemp(prefix=f"rogii_{label}_"))
    try:
        env = os.environ.copy()
        env["SHOW_FIGS"] = "0"   # suppress matplotlib in fork
        if env_extra:
            env.update(env_extra)

        # Point sub-processes at the temp dir as working dir.
        # Both scripts write submission.csv to /kaggle/working when on Kaggle,
        # but locally they write to Path(".") which resolves relative to cwd.
        # We set cwd=tmp_dir so Path(".") == tmp_dir for local runs.
        t0 = time.time()
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(tmp_dir),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.time() - t0
        log(f"[{label}] returncode={result.returncode}  elapsed={elapsed:.0f}s")

        # Log stdout/stderr tails
        stdout_tail = result.stdout[-4000:] if result.stdout else ""
        stderr_tail = result.stderr[-2000:] if result.stderr else ""
        if stdout_tail:
            log(f"[{label}] stdout (tail):\n{stdout_tail}")
        if stderr_tail:
            log(f"[{label}] stderr (tail):\n{stderr_tail}")

        # Locate the generated submission.csv
        candidate = tmp_dir / "submission.csv"
        if not candidate.exists():
            # On Kaggle, scripts write to /kaggle/working
            candidate = Path("/kaggle/working") / "submission.csv"

        if not candidate.exists():
            raise RuntimeError(f"[{label}] submission.csv not found after run. "
                               f"returncode={result.returncode}")

        shutil.copy2(str(candidate), str(out_csv))
        df = pd.read_csv(out_csv)
        log(f"[{label}] collected -> {out_csv}  rows={len(df)}  "
            f"tvt=[{df.tvt.min():.1f}, {df.tvt.max():.1f}]  "
            f"nan={df.tvt.isna().sum()}")

        if result.returncode != 0:
            log(f"[{label}] WARNING: non-zero returncode. Check logs above.")

        return df

    finally:
        # Clean up temp dir (ignore errors on Windows locked files)
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception:
            pass


# ─── Fork-specific: fork writes multiple files; final is submission.csv ───────
def run_fork_subprocess(out_csv: Path):
    """Run the fork kernel. It writes multiple csv files and ends with
    overwriting submission.csv with the 0.55 blend. We collect that."""
    return run_subprocess(FORK_SCRIPT, out_csv, "fork")


def run_exp026_subprocess(out_csv: Path):
    return run_subprocess(EXP026_SCRIPT, out_csv, "exp026")


# ─── Blend ────────────────────────────────────────────────────────────────────
def blend(df_fork: pd.DataFrame, df_exp026: pd.DataFrame) -> pd.DataFrame:
    log(f"blending: fork={len(df_fork)} rows  exp026={len(df_exp026)} rows  "
        f"w_fork={BLEND_FORK}  w_exp026={BLEND_EXP026}")

    fork_map   = dict(zip(df_fork["id"],   df_fork["tvt"].astype(float)))
    exp026_map = dict(zip(df_exp026["id"], df_exp026["tvt"].astype(float)))

    all_ids = sorted(set(fork_map) | set(exp026_map))
    log(f"union ids: {len(all_ids)}")

    rows = []
    missing_fork = 0
    missing_exp026 = 0
    for eid in all_ids:
        fv = fork_map.get(eid)
        ev = exp026_map.get(eid)
        if fv is None and ev is None:
            continue
        if fv is None:
            missing_fork += 1
            blended = float(ev)
        elif ev is None:
            missing_exp026 += 1
            blended = float(fv)
        else:
            blended = BLEND_FORK * float(fv) + BLEND_EXP026 * float(ev)
        rows.append({"id": eid, "tvt": blended})

    log(f"missing_fork_fallback={missing_fork}  missing_exp026_fallback={missing_exp026}")
    out = pd.DataFrame(rows)
    nan_count = out["tvt"].isna().sum()
    log(f"blend result: rows={len(out)}  nan={nan_count}  "
        f"tvt=[{out.tvt.min():.1f}, {out.tvt.max():.1f}]  mean={out.tvt.mean():.2f}")
    if nan_count > 0:
        raise ValueError(f"NaN in blend output: {nan_count}")
    return out


# ─── Sanity checks ────────────────────────────────────────────────────────────
def sanity_check(sub: pd.DataFrame, sample_sub_path: Path):
    sample = pd.read_csv(sample_sub_path)
    expected_ids = set(sample["id"])
    actual_ids   = set(sub["id"])
    missing = expected_ids - actual_ids
    extra   = actual_ids - expected_ids
    log(f"sanity: expected={len(expected_ids)}  actual={len(actual_ids)}  "
        f"missing={len(missing)}  extra={len(extra)}")
    if missing:
        log(f"  MISSING ids (first 5): {sorted(missing)[:5]}")
    if extra:
        log(f"  EXTRA ids (first 5): {sorted(extra)[:5]}")
    if sub["tvt"].isna().any():
        raise ValueError("submission has NaN tvt")
    tvt_arr = sub["tvt"].astype(float)
    if not ((tvt_arr > 5000) & (tvt_arr < 20000)).all():
        log("WARNING: some tvt values outside [5000, 20000] range")
    log(f"sanity OK: rows={len(sub)}  tvt=[{tvt_arr.min():.1f},{tvt_arr.max():.1f}]")


def diff_stats(df_fork: pd.DataFrame, df_blend: pd.DataFrame):
    merged = df_fork[["id","tvt"]].rename(columns={"tvt":"fork"}).merge(
        df_blend[["id","tvt"]].rename(columns={"tvt":"blend"}), on="id", how="inner")
    diff = (merged["blend"] - merged["fork"]).abs()
    log(f"fork vs blend diff: mean={diff.mean():.4f}  max={diff.max():.4f}  "
        f"p50={diff.quantile(0.5):.4f}  p95={diff.quantile(0.95):.4f}")


# ─── Find sample_submission.csv ───────────────────────────────────────────────
def find_sample_sub() -> Path:
    for root in (Path("/kaggle/input"), Path("data/raw"), Path("data")):
        if root.exists():
            hits = list(root.rglob("sample_submission.csv"))
            if hits:
                return hits[0]
    raise FileNotFoundError("sample_submission.csv not found")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    log("=== rogii_phaseA2: fork + exp026 blend (Phase A2) ===")
    log(f"FORK_SCRIPT   = {FORK_SCRIPT}")
    log(f"EXP026_SCRIPT = {EXP026_SCRIPT}")
    log(f"FINAL_SUB     = {FINAL_SUB_PATH}")
    log(f"blend weights : fork={BLEND_FORK}  exp026={BLEND_EXP026}")

    t_total = time.time()

    # Step 1: fork
    log("--- Step 1: fork pipeline ---")
    df_fork = run_fork_subprocess(FORK_SUB_PATH)

    # Step 2: exp026
    log("--- Step 2: exp026 pipeline ---")
    df_exp026 = run_exp026_subprocess(EXP026_SUB_PATH)

    # Step 3: blend
    log("--- Step 3: blend ---")
    df_final = blend(df_fork, df_exp026)

    # Sanity check against sample_submission
    try:
        sample_sub = find_sample_sub()
        sanity_check(df_final, sample_sub)
    except Exception as e:
        log(f"sanity_check warning: {e}")

    # Diff stats
    diff_stats(df_fork, df_final)

    # Write output
    df_final.to_csv(FINAL_SUB_PATH, index=False)
    log(f"wrote final submission: {FINAL_SUB_PATH}  rows={len(df_final)}")

    total_elapsed = time.time() - t_total
    log(f"=== DONE in {total_elapsed:.0f}s ===")

    flush_log()
    return df_final


if __name__ == "__main__":
    main()
