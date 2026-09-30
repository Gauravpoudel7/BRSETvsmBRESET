"""Bootstrap confidence intervals for AUROC and subgroup gaps."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.utils import resample


def bootstrap_auroc(
    probs: np.ndarray,
    labels: np.ndarray,
    patient_ids: np.ndarray | None = None,
    n_samples: int = 1000,
    seed: int = 42,
) -> dict:
    rng = np.random.default_rng(seed)
    if len(np.unique(labels)) < 2:
        return {"auroc_mean": float("nan"), "ci_low": float("nan"), "ci_high": float("nan")}

    scores = []
    indices = np.arange(len(labels))
    for _ in range(n_samples):
        if patient_ids is not None:
            unique_patients = np.unique(patient_ids)
            sampled_patients = resample(unique_patients, replace=True, random_state=rng.integers(1e9))
            idx = np.concatenate([indices[patient_ids == p] for p in sampled_patients])
        else:
            idx = resample(indices, replace=True, random_state=rng.integers(1e9))
        y = labels[idx]
        p = probs[idx]
        if len(np.unique(y)) < 2:
            continue
        scores.append(roc_auc_score(y, p))

    if not scores:
        return {"auroc_mean": float("nan"), "ci_low": float("nan"), "ci_high": float("nan")}

    arr = np.array(scores)
    return {
        "auroc_mean": float(arr.mean()),
        "ci_low": float(np.percentile(arr, 2.5)),
        "ci_high": float(np.percentile(arr, 97.5)),
        "n_bootstrap": len(arr),
    }


def bootstrap_gap(
    subgroup_df: pd.DataFrame,
    attribute: str,
    n_samples: int = 1000,
    seed: int = 42,
) -> dict:
    """Bootstrap gap = max AUROC - min AUROC within attribute (uses stored subgroup AUROCs)."""
    sub = subgroup_df[subgroup_df["attribute"] == attribute].dropna(subset=["auroc"])
    if len(sub) < 2:
        return {"gap_mean": float("nan"), "ci_low": float("nan"), "ci_high": float("nan")}
    aurocs = sub["auroc"].values
    rng = np.random.default_rng(seed)
    gaps = []
    for _ in range(n_samples):
        sample = rng.choice(aurocs, size=len(aurocs), replace=True)
        gaps.append(sample.max() - sample.min())
    arr = np.array(gaps)
    return {
        "gap_mean": float(arr.mean()),
        "ci_low": float(np.percentile(arr, 2.5)),
        "ci_high": float(np.percentile(arr, 97.5)),
    }


def save_bootstrap_results(path: Path, overall: dict, gaps: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"overall_auroc": overall, "subgroup_gaps": gaps}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
