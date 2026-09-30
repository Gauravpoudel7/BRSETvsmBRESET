"""Subgroup metric reporting."""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def parse_age(value: float | int | str) -> float:
    """Numeric age. mBRSET censors the oldest ages as the text '>= 90'."""
    if pd.isna(value):
        return float("nan")
    if isinstance(value, str):
        text = value.strip()
        if text.startswith(">="):
            text = text[2:].strip()
        try:
            return float(text)
        except ValueError:
            return float("nan")
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def assign_age_subgroup(age: float | int | str, cutoff: float = 50.0, use_median: float | None = None) -> str:
    number = parse_age(age)
    if number != number:
        return "unknown"
    threshold = use_median if use_median is not None else cutoff
    return "young" if number < threshold else "old"


def assign_sex_subgroup(sex: float | int | str) -> str:
    if pd.isna(sex):
        return "unknown"
    if isinstance(sex, str):
        s = sex.strip().lower()
        if s in {"f", "female", "2", "woman"}:
            return "female"
        if s in {"m", "male", "1", "man"}:
            return "male"
        return "unknown"
    val = int(float(sex))
    # BRSET: 1=male, 2=female. mBRSET: 0=female, 1=male (PhysioNet codebook).
    if val == 1:
        return "male"
    if val == 2:
        return "female"
    if val == 0:
        return "female"
    return "unknown"


def assign_education_subgroup(value: float | int | str) -> str:
    """mBRSET educational_level: 1 = illiterate, 2-7 = literate (PhysioNet codebook)."""
    if pd.isna(value):
        return "unknown"
    text = str(value).strip().lower()
    if text in {"illiterate"}:
        return "illiterate"
    if text in {"literate", "educated"}:
        return "literate"
    try:
        code = int(float(text))
    except ValueError:
        return "unknown"
    if code == 1:
        return "illiterate"
    if 2 <= code <= 7:
        return "literate"
    return "unknown"


def assign_insurance_subgroup(value: float | int | str) -> str:
    """mBRSET insurance: 0 = uninsured, 1 = insured (PhysioNet codebook)."""
    if pd.isna(value):
        return "unknown"
    text = str(value).strip().lower()
    if text in {"1", "1.0", "yes", "insured", "true"}:
        return "insured"
    if text in {"0", "0.0", "no", "uninsured", "false"}:
        return "uninsured"
    return "unknown"


SUBGROUP_ASSIGNERS: dict[str, Callable] = {
    "patient_age": lambda v, **kw: assign_age_subgroup(v, **kw),
    "age": lambda v, **kw: assign_age_subgroup(v, **kw),
    "patient_sex": lambda v, **kw: assign_sex_subgroup(v),
    "sex": lambda v, **kw: assign_sex_subgroup(v),
    "education": lambda v, **kw: assign_education_subgroup(v),
    "educational_level": lambda v, **kw: assign_education_subgroup(v),
    "insurance": lambda v, **kw: assign_insurance_subgroup(v),
}


MIN_SUBGROUP_N = 30
MIN_SUBGROUP_POS = 5


def assign_groups(metas: list[dict] | pd.DataFrame, col: str, age_median: float | None = None) -> pd.Series:
    df_meta = metas if isinstance(metas, pd.DataFrame) else pd.DataFrame(metas)
    assigner = SUBGROUP_ASSIGNERS.get(col, lambda v, **kw: str(v))
    kwargs = {"use_median": age_median} if col in {"patient_age", "age"} else {}
    return df_meta[col].map(lambda v: assigner(v, **kwargs)).reset_index(drop=True)


def subgroup_auroc_table(
    probs: np.ndarray,
    labels: np.ndarray,
    metas: list[dict] | pd.DataFrame,
    columns: list[str],
    age_median: float | None = None,
    min_n: int = MIN_SUBGROUP_N,
    min_pos: int = MIN_SUBGROUP_POS,
) -> pd.DataFrame:
    """AUROC per subgroup.

    A subgroup counts toward gaps and ES-AUC ("included") only if it is not
    "unknown", has at least min_n images, and has at least min_pos positive and
    min_pos negative images. Tiny groups are still listed so nothing is hidden.
    """
    rows = []
    df_meta = metas if isinstance(metas, pd.DataFrame) else pd.DataFrame(metas)
    overall = roc_auc_score(labels, probs) if len(np.unique(labels)) > 1 else np.nan
    for col in columns:
        if col not in df_meta.columns:
            continue
        groups = assign_groups(df_meta, col, age_median)
        for grp in sorted(groups.unique()):
            mask = (groups == grp).values
            y = labels[mask]
            p = probs[mask]
            n_pos = int((y == 1).sum()); n_neg = int((y == 0).sum())
            auroc = roc_auc_score(y, p) if n_pos and n_neg else np.nan
            included = grp != "unknown" and mask.sum() >= min_n and n_pos >= min_pos and n_neg >= min_pos
            rows.append({
                "attribute": col, "subgroup": grp, "n": int(mask.sum()),
                "n_pos": n_pos, "n_neg": n_neg,
                "auroc": float(auroc) if auroc == auroc else np.nan,
                "included": bool(included),
            })
    result = pd.DataFrame(rows)
    if not result.empty:
        for col in result["attribute"].unique():
            sel = (result["attribute"] == col)
            valid = result.loc[sel & result["included"], "auroc"].dropna()
            if len(valid) >= 2:
                result.loc[sel, "gap"] = float(valid.max() - valid.min())
                result.loc[sel, "es_auc"] = float(overall / (1 + (valid - overall).abs().sum()))
    return result


def equity_scaled_auc(subgroup_df: pd.DataFrame) -> float | None:
    """Mean over attributes of ES-AUC = AUC / (1 + sum |AUC_group - AUC|) (Luo et al., FairVision).

    Only included subgroups (not unknown, big enough) count.
    """
    if subgroup_df.empty or "es_auc" not in subgroup_df.columns:
        return None
    per_attr = subgroup_df.dropna(subset=["es_auc"]).groupby("attribute")["es_auc"].first()
    return float(per_attr.mean()) if len(per_attr) else None


def min_subgroup_auroc(subgroup_df: pd.DataFrame) -> float | None:
    if subgroup_df.empty:
        return None
    v = subgroup_df.loc[subgroup_df["included"], "auroc"].dropna()
    return float(v.min()) if len(v) else None
