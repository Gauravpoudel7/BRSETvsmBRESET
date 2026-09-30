#!/usr/bin/env python3
"""Re-pick the decision threshold for a trained model and report how much it helps.

Writes <output>/threshold_calibration.json and <output>/predictions_*.csv.

Three thresholds are compared on mBRSET:
  default   - 0.5, what run_experiment.py uses
  brset_val - Youden threshold picked on the BRSET validation split (no mBRSET labels used)
  mbrset_cal - Youden threshold picked on a patient-level calibration slice of mBRSET
               (default 20% of patients), scored on the other 80%. Repeated over many
               random slices so the result does not depend on one lucky split.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import roc_auc_score, roc_curve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from run_experiment import cache_dir_for, image_root_for, load_config, make_loader, resolve_csv  # noqa: E402
from src.data import load_metadata, prepare_dataframe  # noqa: E402
from src.evaluate import collect_predictions  # noqa: E402
from src.models import build_model  # noqa: E402


def youden(y: np.ndarray, p: np.ndarray) -> float:
    fpr, tpr, thr = roc_curve(y, p)
    return float(thr[int(np.argmax(tpr - fpr))])


def at_threshold(y: np.ndarray, p: np.ndarray, t: float) -> dict:
    pred = (p >= t).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum()); fn = int(((pred == 0) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
    sens = tp / (tp + fn) if tp + fn else float("nan")
    spec = tn / (tn + fp) if tn + fp else float("nan")
    return {
        "threshold": float(t), "n": int(len(y)), "sensitivity": sens, "specificity": spec,
        "balanced_accuracy": (sens + spec) / 2, "accuracy": (tp + tn) / len(y),
        "tp": tp, "fn": fn, "tn": tn, "fp": fp,
    }


def predict(model, df, cfg, which, device):
    loader = make_loader(df, cfg, train=False, image_root=image_root_for(cfg, which),
                         cache_dir=cache_dir_for(cfg, which))
    probs, labels, metas = collect_predictions(model, loader, device)
    return probs, labels.astype(int), metas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--cal-fraction", type=float, default=0.2)
    ap.add_argument("--repeats", type=int, default=200)
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    d = cfg["data"]
    seed = int(cfg.get("seed", 42))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)

    model = build_model(cfg, device)
    state = torch.load(args.checkpoint, map_location=device, weights_only=False)
    model.load_state_dict(state["model"] if "model" in state else state)
    model.eval()

    val_df = prepare_dataframe(load_metadata(resolve_csv(cfg, "val_csv")), d["label_col"],
                               binary_label=True, restrict_diabetic_only=d.get("restrict_diabetic_only", False))
    ext_df = prepare_dataframe(load_metadata(resolve_csv(cfg, "external_test_csv")), d["label_col"],
                               binary_label=True, restrict_diabetic_only=False)

    pv, yv, _ = predict(model, val_df, cfg, "brset", device)
    pm, ym, mm = predict(model, ext_df, cfg, "mbrset", device)
    pd.DataFrame({"prob": pv, "label": yv}).to_csv(out / "predictions_brset_val.csv", index=False)
    pid_col = d.get("patient_col", "patient_id")
    pids = np.array([str(m.get(pid_col, i)) for i, m in enumerate(mm)])
    pd.DataFrame({"patient_id": pids, "prob": pm, "label": ym}).to_csv(out / "predictions_mbrset.csv", index=False)

    result = {
        "checkpoint": args.checkpoint,
        "mbrset_auroc": float(roc_auc_score(ym, pm)),
        "score_summary": {
            "brset_val_median_prob_pos": float(np.median(pv[yv == 1])),
            "brset_val_median_prob_neg": float(np.median(pv[yv == 0])),
            "mbrset_median_prob_pos": float(np.median(pm[ym == 1])),
            "mbrset_median_prob_neg": float(np.median(pm[ym == 0])),
        },
        "default_0.5_on_all_mbrset": at_threshold(ym, pm, 0.5),
    }
    t_val = youden(yv, pv)
    result["brset_val_youden_on_all_mbrset"] = at_threshold(ym, pm, t_val)

    rng = np.random.default_rng(seed)
    uniq = np.unique(pids)
    rows = []
    for _ in range(args.repeats):
        cal_p = set(rng.choice(uniq, size=max(1, int(round(len(uniq) * args.cal_fraction))), replace=False))
        cal = np.array([p in cal_p for p in pids])
        if len(np.unique(ym[cal])) < 2 or len(np.unique(ym[~cal])) < 2:
            continue
        t = youden(ym[cal], pm[cal])
        r = at_threshold(ym[~cal], pm[~cal], t)
        r["auroc_eval"] = float(roc_auc_score(ym[~cal], pm[~cal]))
        r["default_sensitivity_eval"] = at_threshold(ym[~cal], pm[~cal], 0.5)["sensitivity"]
        rows.append(r)
    df = pd.DataFrame(rows)
    df.to_csv(out / "threshold_calibration_repeats.csv", index=False)

    def summ(col):
        return {"mean": float(df[col].mean()), "ci_low": float(df[col].quantile(0.025)),
                "ci_high": float(df[col].quantile(0.975))}

    result["mbrset_calibrated_on_held_out"] = {
        "cal_fraction_of_patients": args.cal_fraction,
        "repeats": int(len(df)),
        **{k: summ(k) for k in ["threshold", "sensitivity", "specificity", "balanced_accuracy",
                                "accuracy", "auroc_eval", "default_sensitivity_eval"]},
    }
    (out / "threshold_calibration.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
