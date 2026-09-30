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
    probs: np.ndarray,
    labels: np.ndarray,
    groups: np.ndarray,
    patient_ids: np.ndarray | None,
    included_groups: list[str],
    n_samples: int = 1000,
    seed: int = 42,
) -> dict:
    """Patient-level bootstrap of the AUROC gap (best minus worst included subgroup).

    Each round resamples patients with replacement, recomputes every included
    subgroup's AUROC, and takes max - min. Also reports how often the named
    worst group is worst, and a two-sided p-style fraction of rounds where the
    gap sign flips between the two groups at the ends.
    """
    groups = np.asarray(groups)
    if len(included_groups) < 2:
        return {"gap": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"), "groups": included_groups}

    def aurocs(idx):
        out = {}
        for g in included_groups:
            m = groups[idx] == g
            y = labels[idx][m]
            if len(np.unique(y)) < 2:
                return None
            out[g] = roc_auc_score(y, probs[idx][m])
        return out

    base = aurocs(np.arange(len(labels)))
    hi_g = max(base, key=base.get); lo_g = min(base, key=base.get)
    rng = np.random.default_rng(seed)
    indices = np.arange(len(labels))
    if patient_ids is not None:
        patient_ids = np.asarray(patient_ids)
        uniq = np.unique(patient_ids)
        by_patient = {p: indices[patient_ids == p] for p in uniq}
    gaps, diffs = [], []
    for _ in range(n_samples):
        if patient_ids is not None:
            sampled = rng.choice(uniq, size=len(uniq), replace=True)
            idx = np.concatenate([by_patient[p] for p in sampled])
        else:
            idx = rng.integers(0, len(labels), len(labels))
        a = aurocs(idx)
        if a is None:
            continue
        gaps.append(max(a.values()) - min(a.values()))
        diffs.append(a[hi_g] - a[lo_g])
    gaps = np.array(gaps); diffs = np.array(diffs)
    return {
        "gap": float(max(base.values()) - min(base.values())),
        "ci_low": float(np.percentile(gaps, 2.5)),
        "ci_high": float(np.percentile(gaps, 97.5)),
        "best_group": hi_g, "worst_group": lo_g,
        "diff_best_minus_worst_ci": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "frac_rounds_worst_group_not_worse": float((diffs <= 0).mean()),
        "subgroup_auroc": {g: float(v) for g, v in base.items()},
        "n_bootstrap": int(len(gaps)),
    }


def save_bootstrap_results(path: Path, overall: dict, gaps: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"overall_auroc": overall, "subgroup_gaps": gaps}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
