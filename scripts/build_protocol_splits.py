#!/usr/bin/env python3
"""Derive protocol splits from the published Li et al. no-overlap CSVs.

Does not redraw the patient assignment. BRSET train and val are restricted to
diabetic patients. The published BRSET test split is kept, and a diabetic-only
test subset is saved beside it. mBRSET external test is the published test split.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.subgroups import assign_age_subgroup, assign_sex_subgroup, parse_age

REF = ROOT / ".reference" / "brset_mlcp" / "data"
BRSET_LABELS = Path(r"C:\data\brset_mbrset\brazilian-ophthalmological\1.0.2\label_brset.csv")
MBRSET_LABELS = Path(r"C:\data\brset_mbrset\mbrset\1.0\labels_mbrset.csv")
OUT = ROOT / "data" / "splits"


def canon_mbrset_id(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    lower = text.lower()
    for ext in (".jpg", ".jpeg", ".png"):
        if lower.endswith(ext):
            text = text[: -len(ext)]
            break
    try:
        number = float(text)
    except ValueError:
        return text
    return f"{number:.1f}"


def is_diabetic(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin({"yes", "1", "true"})


def attach_brset(ref_name: str, official: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    ref = pd.read_csv(REF / ref_name)
    ref["image_id"] = ref["image_id"].astype(str)
    official = official.copy()
    official["image_id"] = official["image_id"].astype(str)
    merged = ref[["image_id"]].merge(official, on="image_id", how="left", indicator=True)
    missing = int((merged["_merge"] != "both").sum())
    out = merged[merged["_merge"] == "both"].drop(columns="_merge")
    stats = {
        "reference_rows": int(len(ref)),
        "joined_rows": int(len(out)),
        "unmatched_reference_rows": missing,
    }
    return out.reset_index(drop=True), stats


def attach_mbrset(ref_name: str, official: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    ref = pd.read_csv(REF / ref_name)
    official = official.copy()
    ref["_key"] = ref["file"].map(canon_mbrset_id)
    official["_key"] = official["file"].map(canon_mbrset_id)
    merged = ref[["_key"]].merge(official, on="_key", how="left", indicator=True)
    missing = int((merged["_merge"] != "both").sum())
    out = merged[merged["_merge"] == "both"].drop(columns=["_merge", "_key"])
    out = out.rename(
        columns={
            "file": "image_id",
            "final_icdr": "DR_ICDR",
            "patient": "patient_id",
            "age": "patient_age",
            "sex": "patient_sex",
        }
    )
    stats = {
        "reference_rows": int(len(ref)),
        "joined_rows": int(len(out)),
        "unmatched_reference_rows": missing,
    }
    return out.reset_index(drop=True), stats


def drop_missing_labels(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    out = df.dropna(subset=["DR_ICDR"]).reset_index(drop=True)
    return out, before - len(out)


def binary_positive(series: pd.Series) -> pd.Series:
    return series.map(lambda v: 0 if int(float(v)) == 0 else 1)


def summarize(name: str, df: pd.DataFrame) -> dict:
    ages = df["patient_age"].map(parse_age)
    known_age = ages.dropna()
    median = float(known_age.median()) if len(known_age) else float("nan")
    groups = ages.map(lambda a: assign_age_subgroup(a, use_median=median))
    sex = df["patient_sex"].map(assign_sex_subgroup)
    labels = binary_positive(df["DR_ICDR"])
    return {
        "split": name,
        "n_images": int(len(df)),
        "n_patients": int(df["patient_id"].nunique()),
        "n_dr_positive": int(labels.sum()),
        "dr_prevalence": float(labels.mean()) if len(df) else float("nan"),
        "age_median": median,
        "n_young": int((groups == "young").sum()),
        "n_old": int((groups == "old").sum()),
        "n_age_unknown": int((groups == "unknown").sum()),
        "n_age_under_50": int((ages < 50).sum()),
        "n_male": int((sex == "male").sum()),
        "n_female": int((sex == "female").sum()),
        "n_sex_unknown": int((sex == "unknown").sum()),
    }


def overlap_count(frames: list[pd.DataFrame]) -> int:
    sets = [set(df["patient_id"].astype(str)) for df in frames]
    total = 0
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            total += len(sets[i] & sets[j])
    return total


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    brset = pd.read_csv(BRSET_LABELS)
    mbrset = pd.read_csv(MBRSET_LABELS)

    train, train_stats = attach_brset("train_brset_nooverlap.csv", brset)
    val, val_stats = attach_brset("val_brset_nooverlap.csv", brset)
    test, test_stats = attach_brset("test_brset_nooverlap.csv", brset)
    external, external_stats = attach_mbrset("test_mbrset_nooverlap.csv", mbrset)

    print("Join vs published splits:")
    for name, stats in (
        ("brset_train", train_stats),
        ("brset_val", val_stats),
        ("brset_test", test_stats),
        ("mbrset_test", external_stats),
    ):
        print(f"  {name}: {stats}")

    published_overlap = overlap_count([train, val, test])
    print(f"Patient overlap across published BRSET train/val/test: {published_overlap}")

    train, train_drop = drop_missing_labels(train)
    val, val_drop = drop_missing_labels(val)
    test, test_drop = drop_missing_labels(test)
    external, external_drop = drop_missing_labels(external)
    train_d = train[is_diabetic(train["diabetes"])].reset_index(drop=True)
    val_d = val[is_diabetic(val["diabetes"])].reset_index(drop=True)
    test_d = test[is_diabetic(test["diabetes"])].reset_index(drop=True)
    print(
        "Diabetic filter (diabetes == yes): "
        f"train {len(train)} -> {len(train_d)}, "
        f"val {len(val)} -> {len(val_d)}, "
        f"test {len(test)} -> {len(test_d)}"
    )
    train_d_drop = 0
    val_d_drop = 0
    test_d_drop = 0
    print(
        "Rows dropped for missing DR grade: "
        f"train_published {train_drop}, val_published {val_drop}, "
        f"train_diabetic {train_d_drop}, val_diabetic {val_d_drop}, "
        f"test {test_drop}, test_diabetic {test_d_drop}, mbrset_test {external_drop}"
    )

    filtered_overlap = overlap_count([train_d, val_d, test])
    print(f"Patient overlap across diabetic train, diabetic val, published test: {filtered_overlap}")
    if published_overlap != 0 or filtered_overlap != 0:
        raise SystemExit("Patient overlap is not 0. Refusing to save splits.")

    files = {
        "brset_train_published.csv": train,
        "brset_val_published.csv": val,
        "brset_train_diabetic.csv": train_d,
        "brset_val_diabetic.csv": val_d,
        "brset_test_published.csv": test,
        "brset_test_diabetic.csv": test_d,
        "mbrset_test_published.csv": external,
    }
    for name, frame in files.items():
        frame.to_csv(OUT / name, index=False)
        print(f"Wrote {OUT / name} ({len(frame)} rows)")

    rows = [
        summarize("brset_train_published", train),
        summarize("brset_val_published", val),
        summarize("brset_train_diabetic", train_d),
        summarize("brset_val_diabetic", val_d),
        summarize("brset_test_published", test),
        summarize("brset_test_diabetic", test_d),
        summarize("mbrset_test_published", external),
    ]
    for row in rows:
        row["patient_overlap_brset_splits"] = filtered_overlap
    summary = pd.DataFrame(rows)
    summary_path = OUT / "split_summary.csv"
    summary.to_csv(summary_path, index=False)
    print(summary.to_string(index=False))
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
