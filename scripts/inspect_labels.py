#!/usr/bin/env python3
"""Print label-file columns, missingness, and image coverage. Read-only."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

BRSET_LABELS = Path(r"C:\data\brset_mbrset\brazilian-ophthalmological\1.0.2\label_brset.csv")
BRSET_IMAGES = Path(r"C:\data\brset_mbrset\brazilian-ophthalmological\1.0.2\fundus_photos")
MBRSET_LABELS = Path(r"C:\data\brset_mbrset\mbrset\1.0\labels_mbrset.csv")
MBRSET_IMAGES = Path(r"C:\data\brset_mbrset\mbrset\1.0\images")

BRSET_MAP = {
    "image_col": "image_id",
    "label_col": "DR_ICDR",
    "patient_col": "patient_id",
    "age": "patient_age",
    "sex": "patient_sex",
    "education": None,
    "insurance": None,
    "camera": "camera",
    "diabetes": "diabetes",
}

MBRSET_MAP = {
    "image_col": "file",
    "label_col": "final_icdr",
    "patient_col": "patient",
    "age": "age",
    "sex": "sex",
    "education": "educational_level",
    "insurance": "insurance",
    "camera": None,
    "diabetes": None,
}


def image_name(value: object) -> str:
    raw = str(value).strip()
    if raw.lower().endswith((".jpg", ".jpeg", ".png")):
        return raw
    return f"{raw}.jpg"


def coverage(df: pd.DataFrame, col: str, image_dir: Path) -> dict:
    names = df[col].map(image_name)
    present = names.map(lambda n: (image_dir / n).exists())
    missing = names[~present]
    return {
        "rows": int(len(df)),
        "unique_ids": int(df[col].nunique()),
        "images_found": int(present.sum()),
        "images_missing": int((~present).sum()),
        "missing_examples": missing.head(10).tolist(),
    }


def column_report(df: pd.DataFrame, mapping: dict) -> list[dict]:
    rows = []
    for role, col in mapping.items():
        if col is None or col not in df.columns:
            rows.append({"role": role, "column": col, "present": False, "missing": None, "nunique": None})
            continue
        rows.append(
            {
                "role": role,
                "column": col,
                "present": True,
                "missing": int(df[col].isna().sum()),
                "nunique": int(df[col].nunique(dropna=True)),
            }
        )
    return rows


def main() -> None:
    br = pd.read_csv(BRSET_LABELS)
    mb = pd.read_csv(MBRSET_LABELS)
    report = {
        "brset": {
            "path": str(BRSET_LABELS),
            "n_rows": int(len(br)),
            "n_cols": int(br.shape[1]),
            "columns": list(br.columns),
            "mapped": column_report(br, BRSET_MAP),
            "image_coverage": coverage(br, "image_id", BRSET_IMAGES),
            "DR_ICDR_counts": {str(k): int(v) for k, v in br["DR_ICDR"].value_counts(dropna=False).sort_index().items()},
            "diabetes_counts": {str(k): int(v) for k, v in br["diabetes"].value_counts(dropna=False).items()},
            "sex_counts": {str(k): int(v) for k, v in br["patient_sex"].value_counts(dropna=False).items()},
            "camera_counts": {str(k): int(v) for k, v in br["camera"].value_counts(dropna=False).items()},
        },
        "mbrset": {
            "path": str(MBRSET_LABELS),
            "n_rows": int(len(mb)),
            "n_cols": int(mb.shape[1]),
            "columns": list(mb.columns),
            "mapped": column_report(mb, MBRSET_MAP),
            "image_coverage": coverage(mb, "file", MBRSET_IMAGES),
            "final_icdr_counts": {
                str(k): int(v) for k, v in mb["final_icdr"].value_counts(dropna=False).sort_index().items()
            },
            "sex_counts": {str(k): int(v) for k, v in mb["sex"].value_counts(dropna=False).items()},
            "educational_level_counts": {
                str(k): int(v) for k, v in mb["educational_level"].value_counts(dropna=False).sort_index().items()
            },
            "insurance_counts": {str(k): int(v) for k, v in mb["insurance"].value_counts(dropna=False).items()},
        },
    }
    out = Path("results/inspect_labels.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
