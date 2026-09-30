#!/usr/bin/env python3
"""Re-score subgroups from saved predictions (CPU only, no model needed).

Usage: rescore_subgroups.py --config CFG --predictions PRED.csv --split external_test_csv|test_csv --output DIR
Writes DIR/subgroup_metrics_v2.csv and DIR/fairness_v2.json.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from run_experiment import load_config, resolve_csv  # noqa: E402
from src.bootstrap import bootstrap_auroc, bootstrap_gap  # noqa: E402
from src.data import load_metadata, prepare_dataframe  # noqa: E402
from src.subgroups import assign_groups, equity_scaled_auc, min_subgroup_auroc, parse_age, subgroup_auroc_table  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--predictions", required=True)
    ap.add_argument("--split", default="external_test_csv"); ap.add_argument("--output", required=True)
    ap.add_argument("--bootstrap", type=int, default=1000)
    a = ap.parse_args()
    cfg = load_config(Path(a.config)); d = cfg["data"]; seed = int(cfg.get("seed", 42))
    meta = prepare_dataframe(load_metadata(resolve_csv(cfg, a.split)), d["label_col"], binary_label=True,
                             restrict_diabetic_only=False)
    pred = pd.read_csv(a.predictions)
    assert len(pred) == len(meta), (len(pred), len(meta))
    assert (pred["label"].values == meta["label"].values).all(), "label order mismatch"
    assert (pred["patient_id"].astype(str).values == meta[d.get("patient_col", "patient_id")].astype(str).values).all(), "patient order mismatch"
    probs = pred["prob"].values; labels = pred["label"].values.astype(int)
    pids = meta[d.get("patient_col", "patient_id")].astype(str).values
    cols = d.get("mbrset_subgroup_columns") if a.split == "external_test_csv" else d.get("subgroup_columns")
    ages = meta["patient_age"].map(parse_age).dropna() if "patient_age" in meta else pd.Series(dtype=float)
    age_median = float(ages.median()) if len(ages) else None
    sub = subgroup_auroc_table(probs, labels, meta, cols, age_median=age_median)
    out = Path(a.output); out.mkdir(parents=True, exist_ok=True)
    sub.to_csv(out / "subgroup_metrics_v2.csv", index=False)
    gaps = {}
    for attr in sub["attribute"].unique():
        inc = sub[(sub["attribute"] == attr) & sub["included"]]["subgroup"].tolist()
        g = assign_groups(meta, attr, age_median if attr in {"patient_age", "age"} else None).values
        gaps[attr] = bootstrap_gap(probs, labels, g, pids, inc, n_samples=a.bootstrap, seed=seed)
    res = {
        "predictions": a.predictions, "n": int(len(labels)), "age_median_cutoff": age_median,
        "auroc": float(roc_auc_score(labels, probs)),
        "auroc_bootstrap": bootstrap_auroc(probs, labels, pids, n_samples=a.bootstrap, seed=seed),
        "equity_scaled_auc": equity_scaled_auc(sub), "min_subgroup_auroc": min_subgroup_auroc(sub),
        "es_auc_per_attribute": sub.dropna(subset=["es_auc"]).groupby("attribute")["es_auc"].first().to_dict(),
        "subgroup_gaps": gaps,
    }
    (out / "fairness_v2.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(sub.to_string(index=False)); print(json.dumps({k: v for k, v in res.items() if k != "subgroup_gaps"}, indent=2))
    for k, v in gaps.items():
        print(k, {x: v.get(x) for x in ["gap", "ci_low", "ci_high", "worst_group", "diff_best_minus_worst_ci", "frac_rounds_worst_group_not_worse"]})


if __name__ == "__main__":
    main()
