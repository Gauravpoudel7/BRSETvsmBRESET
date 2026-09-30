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


def subgroup_auroc_table(
    probs: np.ndarray,
    labels: np.ndarray,
    metas: list[dict],
    columns: list[str],
    age_median: float | None = None,
) -> pd.DataFrame:
    rows = []
    df_meta = pd.DataFrame(metas)

    for col in columns:
        if col not in df_meta.columns:
            continue
        assigner = SUBGROUP_ASSIGNERS.get(col, lambda v, **kw: str(v))
        kwargs = {"use_median": age_median} if col in {"patient_age", "age"} else {}
        groups = df_meta[col].map(lambda v: assigner(v, **kwargs))

        for grp in sorted(groups.unique()):
            mask = groups == grp
            y = labels[mask.values]
            p = probs[mask.values]
            if len(np.unique(y)) < 2:
                auroc = np.nan
            else:
                auroc = roc_auc_score(y, p)
            rows.append(
                {
                    "attribute": col,
                    "subgroup": grp,
                    "n": int(mask.sum()),
                    "auroc": float(auroc) if auroc == auroc else np.nan,
                }
            )

    result = pd.DataFrame(rows)
    if not result.empty:
        for col in result["attribute"].unique():
            sub = result[result["attribute"] == col]
            valid = sub.loc[sub["subgroup"] != "unknown", "auroc"].dropna()
            if len(valid) >= 2:
                gap = valid.max() - valid.min()
                result.loc[result["attribute"] == col, "gap_note"] = f"gap={gap:.4f}"
    return result


def equity_scaled_auc(subgroup_df: pd.DataFrame) -> float | None:
    """Simple fairness summary: minimum subgroup AUROC across attributes (conservative)."""
    if subgroup_df.empty or "auroc" not in subgroup_df.columns:
        return None
    valid = subgroup_df.dropna(subset=["auroc"])
    if valid.empty:
        return None
    return float(valid.groupby("attribute")["auroc"].min().mean())
