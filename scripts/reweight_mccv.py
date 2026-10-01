#!/usr/bin/env python3
"""Re-score MCCV runs as if the test set had a realistic screening grade mix.

Each test image is weighted by target_share[grade] / observed_share[grade], so the weighted
test set matches the target ICDR mix (default: 54/30/10/5/1 for grades 0-4, per Nicholas).
No retraining is needed. Also reports per-grade sensitivity at the threshold giving 10% FPR
on grade 0, and the effective sample size of each weighted grade.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data import load_metadata, prepare_dataframe

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="C:/data/mccv")
    ap.add_argument("--mbrset-test", default="data/splits/mbrset_test_published.csv")
    ap.add_argument("--mix", default="54,30,10,5,1")
    a = ap.parse_args()
    target = np.array([float(x) for x in a.mix.split(",")]); target /= target.sum()
    rows = []
    for run in sorted(Path(a.root).glob("run_r*")):
        r = run.name.replace("run_", "")
        tests = {"BRSET": (Path(""), ROOT / "data/splits/mccv" / f"test_{r}.csv"),
                 "mBRSET": (Path("mbrset_external"), ROOT / a.mbrset_test)}
        for name, (sub, csv) in tests.items():
            pf = run / sub / "predictions.csv"
            if not pf.exists(): continue
            pred = pd.read_csv(pf)
            meta = prepare_dataframe(load_metadata(csv), "DR_ICDR", binary_label=True)
            assert len(meta) == len(pred) and (meta["label"].to_numpy() == pred["label"].to_numpy()).all(), pf
            g = meta["DR_ICDR"].astype(float).round().astype(int).to_numpy()
            p = pred["prob"].to_numpy()
            obs = np.array([(g == k).mean() for k in range(5)])
            w = np.array([target[k] / obs[k] if obs[k] > 0 else 0.0 for k in g])
            anyy, refy = (g >= 1).astype(int), (g >= 2).astype(int)
            m = {"run": run.name, "test": name,
                 "auroc_any_raw": roc_auc_score(anyy, p), "auroc_any_realmix": roc_auc_score(anyy, p, sample_weight=w),
                 "auroc_ref_raw": roc_auc_score(refy, p), "auroc_ref_realmix": roc_auc_score(refy, p, sample_weight=w)}
            thr = np.quantile(p[g == 0], 0.90)
            sens = {k: float((p[g == k] > thr).mean()) if (g == k).any() else np.nan for k in range(1, 5)}
            for k in range(1, 5): m[f"sens_grade{k}"] = sens[k]; m[f"n_grade{k}"] = int((g == k).sum())
            m["n_grade0"] = int((g == 0).sum())
            m["sens_any_realmix"] = float(sum(target[k] * sens[k] for k in range(1, 5)) / target[1:].sum())
            m["sens_ref_realmix"] = float(sum(target[k] * sens[k] for k in range(2, 5)) / target[2:].sum())
            rows.append(m)
    df = pd.DataFrame(rows)
    if df.empty: print("No runs."); return
    df.to_csv(Path(a.root) / "mccv_realmix_per_run.csv", index=False)
    cols = [c for c in df.columns if c not in ("run", "test")]
    agg = df.groupby("test")[cols].agg(["mean", "min", "max"]).T
    agg.to_csv(Path(a.root) / "mccv_realmix_summary.csv")
    print(df.groupby("test").size().rename("runs").to_string()); print(agg.round(3).to_string())

if __name__ == "__main__":
    main()
