#!/usr/bin/env python3
"""
exp065 H19: Conformal Prediction + Selective Fallback (★)

Key insight: OOF has ONLY is_target rows (all beyond last_known_TVT).
To train conformal intervals, must use actual train set known rows.
Then apply conformal rule to OOF (is_target) rows.

Leak-free: Use ONLY known rows (before last_known_TVT anchor point).
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

root = "/Users/satouryuuichi/Desktop/DS/ROGII-Wellbore-Geology-Prediction"

print("[LOAD] exp022 OOF, per_well, full train...")
oof = pd.read_csv(f"{root}/experiments/exp022_particle_filter/oof.csv")
per_well = pd.read_csv(f"{root}/experiments/exp022_particle_filter/per_well.csv")
train = pd.read_parquet(f"{root}/data/processed/train_base_v001.parquet")

print(f"  OOF: {oof.shape}, per_well: {per_well.shape}, train: {train.shape}")

# Build predictions dict: (well_id, row_idx) -> pred_tvt
# We'll compute in-well predictions using any available model reference
# For OOF, use the actual values directly

# ============================================================================
# H19: CONFORMAL PREDICTION + SELECTIVE FALLBACK ★
# ============================================================================
print("\n" + "="*80)
print("[H19] CONFORMAL PREDICTION + SELECTIVE FALLBACK (★)")
print("="*80)
print("Method: Train conformal intervals on known rows; apply to is_target rows")

broken_scores = []
all_pf_errors = []
all_final_errors = []

for well_id in train['well_id'].unique():
    train_well = train[train['well_id'] == well_id].sort_values('MD')
    oof_well = oof[oof['well_id'] == well_id]

    if len(train_well) < 10 or len(oof_well) == 0:
        continue

    # TRAINING on known rows (leak-free)
    known = train_well[train_well['is_known_tvt'] == True]
    if len(known) < 5:
        continue

    # We need PF predictions on known rows
    # Build a simple anchor baseline for known rows: use last_known_TVT (zero offset)
    # Or better: use exp022 anchor RMSE as proxy
    # For proper conformal, compute PF residuals on known rows if possible

    # Approximation: use the fact that OOF errors give us PF accuracy
    # Compute residuals on is_target rows as proxy for well-level error spread

    # Known region residuals (actual): TVT - anchor
    known_residuals = (known['TVT'].values - known['last_known_TVT'].values).astype(float)
    # This is the "trend" in known region

    # Conformal: empirical quantile of absolute trend
    quantile_90 = np.percentile(np.abs(known_residuals), 90)
    interval_width = 2 * quantile_90

    # PF RMSE for this well (from per_well)
    pf_rmse_row = per_well[per_well['well_id'] == well_id]['pf_rmse'].values
    if len(pf_rmse_row) == 0:
        continue
    pf_rmse = pf_rmse_row[0]

    # Broken decision: wide interval = uncertain well
    broken_threshold = 15.0
    is_broken = interval_width > broken_threshold

    # Apply strategy to OOF (is_target) rows
    if is_broken:
        # Fallback: use anchor (last_known_TVT)
        preds_final = oof_well['last_known_TVT'].values
    else:
        # Use PF predictions
        preds_final = oof_well['pred_tvt'].values

    # Compute RMSEs on OOF
    errors_pf = oof_well['error'].values  # TVT - pred_tvt (from OOF)
    errors_final = oof_well['TVT'].values - preds_final

    rmse_pf = np.sqrt(np.mean(errors_pf ** 2))
    rmse_final = np.sqrt(np.mean(errors_final ** 2))

    all_pf_errors.extend(errors_pf)
    all_final_errors.extend(errors_final)

    broken_scores.append({
        'well_id': well_id,
        'pf_rmse': float(pf_rmse),
        'interval_width': float(interval_width),
        'broken': is_broken,
        'n_target': len(oof_well),
        'rmse_pf': float(rmse_pf),
        'rmse_final': float(rmse_final),
        'gain': float(rmse_pf - rmse_final)
    })

if len(broken_scores) == 0:
    print("ERROR: No wells processed!")
    exit(1)

broken_df = pd.DataFrame(broken_scores)

# Pooled CV
cv_pf = np.sqrt(np.mean(np.array(all_pf_errors) ** 2))
cv_final = np.sqrt(np.mean(np.array(all_final_errors) ** 2))

# Correlation: width vs PF RMSE
corr_width_rmse = broken_df[['interval_width', 'pf_rmse']].corr().iloc[0, 1]

n_broken = broken_df['broken'].sum()
n_total = len(broken_df)
gain_total = cv_pf - cv_final

print(f"\nResults (N={n_total} wells):")
print(f"  CV (PF baseline):            {cv_pf:.4f}")
print(f"  CV (+ conformal fallback):   {cv_final:.4f}")
print(f"  Total gain:                  {gain_total:.4f}")
print(f"  Broken wells detected:       {n_broken} / {n_total} ({100*n_broken/n_total:.1f}%)")
print(f"  Correlation(width vs RMSE):  {corr_width_rmse:.4f}")
print(f"    (strong >0.225, weak <0.15)")

if n_broken > 0:
    median_gain_broken = broken_df[broken_df['broken']]['gain'].median()
    mean_gain_broken = broken_df[broken_df['broken']]['gain'].mean()
    n_improved_broken = (broken_df[broken_df['broken']]['gain'] > 0).sum()
    print(f"  Gains on broken wells:")
    print(f"    Median: {median_gain_broken:.4f}")
    print(f"    Mean:   {mean_gain_broken:.4f}")
    print(f"    Improved: {n_improved_broken} / {n_broken}")
else:
    median_gain_broken = 0.0
    mean_gain_broken = 0.0

h19_result = {
    'method': 'Conformal Prediction + Selective Fallback',
    'cv_baseline': float(cv_pf),
    'cv_with_rejection': float(cv_final),
    'gain': float(gain_total),
    'n_wells': int(n_total),
    'broken_detected': int(n_broken),
    'broken_pct': float(100 * n_broken / n_total),
    'correlation_width_vs_rmse': float(corr_width_rmse),
    'median_gain_broken': float(median_gain_broken),
    'mean_gain_broken': float(mean_gain_broken),
    'leak_risk': 'none (conformal CI trained on known rows only)'
}

# ============================================================================
# H18: SPECTRAL DECOMPOSITION
# ============================================================================
print("\n" + "="*80)
print("[H18] SPECTRAL DECOMPOSITION (secondary)")
print("="*80)

h18_results = []
for well_id in train['well_id'].unique():
    train_well = train[train['well_id'] == well_id].sort_values('MD')
    oof_well = oof[oof['well_id'] == well_id]

    if len(train_well) < 20 or len(oof_well) == 0:
        continue

    # Known rows for FFT fitting
    known = train_well[train_well['is_known_tvt'] == True]
    if len(known) < 10:
        continue

    try:
        # Trend: TVT vs MD in known region
        md_known = known['MD'].values.astype(float)
        tvt_known = known['TVT'].values.astype(float)
        last_known_tvt = known['last_known_TVT'].values[0]

        # Residuals: actual offset from anchor
        residuals_known = (tvt_known - last_known_tvt).astype(float)

        # FFT low-pass decomposition
        fft_vals = np.fft.rfft(residuals_known)
        n_keep = max(2, len(fft_vals) // 5)
        fft_vals[n_keep:] = 0
        residuals_lowfreq = np.fft.irfft(fft_vals, n=len(residuals_known)).real

        # Fit trend to low-freq component
        z = np.polyfit(md_known, residuals_lowfreq, deg=1)
        poly = np.poly1d(z)

        # Extrapolate to OOF MD
        md_oof = np.full(len(oof_well), np.nan)
        # Need MD from train's is_target rows
        oof_rows_idx = oof_well['row_idx'].values
        train_oof = train_well[train_well['row_idx'].isin(oof_rows_idx)].set_index('row_idx')
        md_oof = train_oof.loc[oof_rows_idx, 'MD'].values.astype(float)

        if len(md_oof) != len(oof_well):
            continue

        residuals_pred = poly(md_oof)

        # Corrected predictions: anchor + extrapolated trend
        corrected_pred = oof_well['last_known_TVT'].values + residuals_pred
        errors_corr = oof_well['TVT'].values - corrected_pred

        rmse_orig = np.sqrt(np.mean(oof_well['error'].values ** 2))
        rmse_corr = np.sqrt(np.mean(errors_corr ** 2))

        h18_results.append({
            'rmse_orig': rmse_orig ** 2,
            'rmse_corr': rmse_corr ** 2,
            'gain': rmse_orig - rmse_corr
        })
    except Exception as e:
        pass

if h18_results:
    cv_orig_h18 = np.sqrt(np.mean([r['rmse_orig'] for r in h18_results]))
    cv_corr_h18 = np.sqrt(np.mean([r['rmse_corr'] for r in h18_results]))
    gain_h18 = cv_orig_h18 - cv_corr_h18
    wells_improved_h18 = sum(1 for r in h18_results if r['gain'] > 0)

    print(f"Results (N={len(h18_results)} wells):")
    print(f"  CV (original):               {cv_orig_h18:.4f}")
    print(f"  CV (+ spectral extrap):      {cv_corr_h18:.4f}")
    print(f"  Gain:                        {gain_h18:.4f}")
    print(f"  Wells improved:              {wells_improved_h18} / {len(h18_results)}")

    h18_result = {
        'method': 'Spectral Decomposition (FFT + linear extrapolation)',
        'cv_original': float(cv_orig_h18),
        'cv_corrected': float(cv_corr_h18),
        'gain': float(gain_h18),
        'n_wells': len(h18_results),
        'wells_improved': wells_improved_h18,
        'leak_risk': 'none (known rows only)'
    }
else:
    h18_result = {
        'method': 'Spectral Decomposition',
        'note': 'No wells processed',
        'gain': 0.0,
        'leak_risk': 'none'
    }

# ============================================================================
# H20: GR AMBIGUITY
# ============================================================================
print("\n" + "="*80)
print("[H20] GR AMBIGUITY DETECTION (tertiary)")
print("="*80)

ambiguity_scores = []
for well_id in train['well_id'].unique():
    train_well = train[train['well_id'] == well_id]

    if len(train_well) < 20:
        continue

    # GR analysis on known rows (leak-free)
    known = train_well[train_well['is_known_tvt'] == True]
    if len(known) < 10:
        continue

    gr_vals = known['GR'].values
    gr_vals = gr_vals[~np.isnan(gr_vals)]

    if len(gr_vals) < 10:
        continue

    # GR dispersion
    hist, _ = np.histogram(gr_vals, bins=20)
    n_peaks = np.sum((hist[1:-1] > hist[:-2]) & (hist[1:-1] > hist[2:]))
    gr_std = np.std(gr_vals)
    gr_mean = np.mean(gr_vals)
    cv_gr = gr_std / gr_mean if gr_mean != 0 else 1.0

    ambiguity = float(n_peaks + cv_gr)

    # PF RMSE for this well
    pf_rmse_row = per_well[per_well['well_id'] == well_id]['pf_rmse'].values
    if len(pf_rmse_row) == 0:
        continue

    ambiguity_scores.append({
        'well_id': well_id,
        'ambiguity': ambiguity,
        'pf_rmse': float(pf_rmse_row[0])
    })

if len(ambiguity_scores) > 2:
    ambiguity_df = pd.DataFrame(ambiguity_scores)
    corr_ambiguity = ambiguity_df[['ambiguity', 'pf_rmse']].corr().iloc[0, 1]
    print(f"Results (N={len(ambiguity_df)} wells):")
    print(f"  Correlation(GR ambiguity vs PF RMSE): {corr_ambiguity:.4f}")

    h20_result = {
        'method': 'GR Ambiguity Detection (multi-modality proxy)',
        'correlation_ambiguity_vs_rmse': float(corr_ambiguity),
        'n_wells_analyzed': len(ambiguity_df),
        'verdict': 'WEAK' if abs(corr_ambiguity) < 0.15 else 'MODERATE',
        'leak_risk': 'none (known GR only)'
    }
else:
    h20_result = {
        'method': 'GR Ambiguity Detection',
        'note': 'Insufficient data',
        'leak_risk': 'none'
    }

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

results = {
    'exp_id': 'exp065_error_structure',
    'created_at': datetime.now().isoformat(),
    'baseline': {
        'method': 'exp022_particle_filter',
        'cv_rmse': 11.024014426002738
    },
    'hypothesis_19_conformal': h19_result,
    'hypothesis_18_spectral': h18_result,
    'hypothesis_20_ambiguity': h20_result,
    'overall_verdict': {
        'h19_priority': f"CV {cv_final:.4f} vs {cv_pf:.4f}, gain={gain_total:+.4f}. Width-RMSE corr={corr_width_rmse:.3f}.",
        'h18_secondary': f"Gain {h18_result.get('gain', 0):+.4f}",
        'h20_tertiary': f"Correlation {h20_result.get('correlation_ambiguity_vs_rmse', 0):.3f}",
        'recommendation': f"H19 shows {'PROMISE' if gain_total > 0.1 else 'MARGINAL GAIN'}. Investigate broken-well subgroup for width threshold tuning."
    }
}

with open(f"{root}/experiments/exp065_error_structure/result.json", 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✓ result.json saved\n")
print(f"H19 ★ (Conformal):")
print(f"  CV: {cv_pf:.4f} -> {cv_final:.4f} ({gain_total:+.4f})")
print(f"  Broken: {n_broken}/{n_total}, Width-RMSE corr: {corr_width_rmse:.4f}")
print(f"\nH18 (Spectral): {h18_result.get('gain', 0):+.4f}")
print(f"\nH20 (GR ambiguity): corr={h20_result.get('correlation_ambiguity_vs_rmse', 0):.4f}")
print("\n[COMPLETE]")
