"""local_verify.py: smoke-test rogii_phaseA2 logic with 3 test wells.

Steps:
1. Run exp026 on full test (it handles local paths natively) -> exp026_sub.csv
2. Run fork on full test -> fork_sub.csv   (via subprocess, cwd=tmp)
3. Blend -> blended_sub.csv
4. Compare vs sample_submission for row-count / NaN / tvt range
5. Join with train TVT for 3-well in-distribution RMSE (sanity only)

Logs to experiments/exp084_phaseA2/build_log.txt
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

ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT))

FORK_SCRIPT   = ROOT / "kaggle_notebooks" / "exp080_sp45_fork"   / "rogii_sp45_fork.py"
EXP026_SCRIPT = ROOT / "kaggle_notebooks" / "exp072_proj"         / "_decoded_exp026_b64.py"
DATA_DIR      = ROOT / "data" / "raw"
LOG_PATH      = ROOT / "experiments" / "exp084_phaseA2" / "build_log.txt"
OUT_DIR       = ROOT / "experiments" / "exp084_phaseA2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BLEND_FORK   = 0.70
BLEND_EXP026 = 0.30

_lines = []

def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    _lines.append(line)

def flush_log():
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(_lines) + "\n")


def run_script(script: Path, label: str, out_csv: Path):
    log(f"[{label}] running {script}")
    tmp = Path(tempfile.mkdtemp(prefix=f"rogii_{label}_"))
    env = os.environ.copy()
    env["SHOW_FIGS"] = "0"
    try:
        t0 = time.time()
        r = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(tmp),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=1800,
        )
        elapsed = time.time() - t0
        log(f"[{label}] rc={r.returncode}  elapsed={elapsed:.0f}s")
        # save stdout/stderr
        with open(OUT_DIR / f"log_{label}.txt", "w", encoding="utf-8") as f:
            f.write(r.stdout or "")
            f.write("\n--- STDERR ---\n")
            f.write(r.stderr or "")
        tail = (r.stdout or "")[-2000:]
        if tail: log(f"[{label}] stdout tail:\n{tail}")
        if r.stderr: log(f"[{label}] stderr tail:\n{r.stderr[-1000:]}")

        # locate submission.csv
        cand = tmp / "submission.csv"
        if not cand.exists():
            raise RuntimeError(f"[{label}] submission.csv not found in {tmp}")
        shutil.copy2(str(cand), str(out_csv))
        df = pd.read_csv(out_csv)
        log(f"[{label}] -> {out_csv}  rows={len(df)}  nan={df.tvt.isna().sum()}  "
            f"tvt=[{df.tvt.min():.1f},{df.tvt.max():.1f}]")
        return df
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    log("=== local_verify: exp084_phaseA2 ===")
    log(f"ROOT={ROOT}")
    log(f"FORK_SCRIPT={FORK_SCRIPT}")
    log(f"EXP026_SCRIPT={EXP026_SCRIPT}")

    # --- Step 1: exp026 ---
    exp026_csv = OUT_DIR / "exp026_sub.csv"
    df_exp026 = run_script(EXP026_SCRIPT, "exp026", exp026_csv)

    # --- Step 2: fork ---
    fork_csv = OUT_DIR / "fork_sub.csv"
    df_fork = run_script(FORK_SCRIPT, "fork", fork_csv)

    # --- Step 3: blend ---
    log("blending...")
    fmap = dict(zip(df_fork["id"],   df_fork["tvt"].astype(float)))
    emap = dict(zip(df_exp026["id"], df_exp026["tvt"].astype(float)))
    all_ids = sorted(set(fmap) | set(emap))
    rows = []
    for eid in all_ids:
        fv = fmap.get(eid)
        ev = emap.get(eid)
        if fv is None and ev is None: continue
        if fv is None: b = float(ev)
        elif ev is None: b = float(fv)
        else: b = BLEND_FORK * float(fv) + BLEND_EXP026 * float(ev)
        rows.append({"id": eid, "tvt": b})
    df_blend = pd.DataFrame(rows)
    blend_csv = OUT_DIR / "blended_sub.csv"
    df_blend.to_csv(blend_csv, index=False)
    log(f"blend: rows={len(df_blend)}  nan={df_blend.tvt.isna().sum()}  "
        f"tvt=[{df_blend.tvt.min():.1f},{df_blend.tvt.max():.1f}]  mean={df_blend.tvt.mean():.2f}")

    # --- Sanity: sample_submission ---
    sample = pd.read_csv(DATA_DIR / "sample_submission.csv")
    log(f"sample_submission rows={len(sample)}")
    missing = set(sample["id"]) - set(df_blend["id"])
    log(f"missing from blend: {len(missing)}")
    if missing:
        log(f"  first 5: {sorted(missing)[:5]}")

    # --- Diff stats: fork vs blend ---
    merged = df_fork[["id","tvt"]].rename(columns={"tvt":"fork"}).merge(
        df_blend[["id","tvt"]].rename(columns={"tvt":"blend"}), on="id", how="inner")
    diff = (merged["blend"] - merged["fork"]).abs()
    log(f"fork vs blend diff: mean={diff.mean():.4f}  max={diff.max():.4f}  "
        f"p50={diff.quantile(0.5):.4f}  p95={diff.quantile(0.95):.4f}")

    # --- 3-well sanity RMSE (train truth) ---
    test_files = sorted((DATA_DIR / "test").glob("*__horizontal_well.csv"))[:3]
    test_wids = [f.name.split("__")[0] for f in test_files]
    log(f"3-well sanity RMSE check: {test_wids}")

    # try to get train truth for these wids (unlikely to exist for test, so just report id range)
    merged_sample = sample[["id"]].merge(df_blend[["id","tvt"]], on="id", how="left")
    # filter to 3 wells
    wid_rows = {}
    for wid in test_wids:
        mask = merged_sample["id"].str.startswith(wid)
        sub_wid = merged_sample[mask]
        if len(sub_wid) > 0:
            wid_rows[wid] = sub_wid
            log(f"  {wid}: rows={len(sub_wid)}  tvt=[{sub_wid.tvt.min():.1f},{sub_wid.tvt.max():.1f}]")

    # Check train truth if available (test wells have no TVT truth -> just sanity)
    # For true RMSE we need train wells, but we're targeting test wells.
    # Instead report anchor-baseline RMSE for test wells
    rmse_list = []
    for wid in test_wids:
        hw = pd.read_csv(DATA_DIR / "test" / f"{wid}__horizontal_well.csv")
        anchor = hw["TVT_input"].dropna().iloc[-1] if hw["TVT_input"].notna().any() else np.nan
        tgt_mask = hw["TVT_input"].isna()
        n_tgt = tgt_mask.sum()
        if np.isfinite(anchor) and wid in wid_rows and n_tgt > 0:
            preds = wid_rows[wid]["tvt"].astype(float).to_numpy()
            anchor_preds = np.full(len(preds), anchor)
            # no truth for test -> just report std of our prediction
            log(f"  {wid}: anchor={anchor:.1f}  pred_mean={preds.mean():.1f}  "
                f"pred_std={preds.std():.2f}  n_tgt={n_tgt}")

    log("=== DONE ===")
    flush_log()


if __name__ == "__main__":
    main()
