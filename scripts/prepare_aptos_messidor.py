#!/usr/bin/env python3
"""Build APTOS train/val and MESSIDOR-2 test CSVs for the public pilot study."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "pilot"
IMG = OUT / "images"


def binarize_aptos(diagnosis: int) -> int:
    return 0 if int(diagnosis) == 0 else 1


def prepare_aptos(aptos_dir: Path, val_frac: float = 0.15, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse Kaggle APTOS 2019 layout: train.csv + train_images/ or preprocessed_png/."""
    aptos_dir = Path(aptos_dir)
    csv_path = aptos_dir / "train.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing {csv_path}. Download APTOS from Kaggle first.")

    df = pd.read_csv(csv_path)
    df["label"] = df["diagnosis"].map(binarize_aptos)
    df["patient_id"] = df["id_code"]
    df["patient_age"] = pd.NA
    df["patient_sex"] = pd.NA

    image_dirs = [aptos_dir / "train_images", aptos_dir / "preprocessed_train", aptos_dir / "preprocessed_png"]
    image_dir = next((d for d in image_dirs if d.exists()), None)
    if image_dir is None:
        raise FileNotFoundError(f"No image folder found under {aptos_dir}")

    rows = []
    for _, row in df.iterrows():
        code = row["id_code"]
        for ext in (".png", ".jpg", ".jpeg"):
            src = image_dir / f"{code}{ext}"
            if src.exists():
                rel = f"aptos/{src.name}"
                dst = IMG / "aptos" / src.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists():
                    try:
                        import shutil
                        shutil.copy2(src, dst)
                    except OSError:
                        rel = str(src.resolve())
                rows.append(
                    {
                        "image_path": rel,
                        "patient_id": row["patient_id"],
                        "label": row["label"],
                        "patient_age": row["patient_age"],
                        "patient_sex": row["patient_sex"],
                    }
                )
                break
    full = pd.DataFrame(rows)
    if full.empty:
        raise RuntimeError("No APTOS images matched train.csv id_codes.")

    train_df, val_df = train_test_split(
        full, test_size=val_frac, random_state=seed, stratify=full["label"]
    )
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True)


def prepare_messidor(messidor_dir: Path) -> pd.DataFrame:
    """
    Parse MESSIDOR-2 style layout.
    Supports:
      - messidor_dir/IMAGES/*.jpg with messidor_dir/messidor_data.csv
      - messidor_dir/Images/*.jpg with grade CSV from common mirrors
    """
    messidor_dir = Path(messidor_dir)
    rows = []

    csv_candidates = list(messidor_dir.glob("*.csv")) + list(messidor_dir.glob("**/*messidor*.csv"))
    image_dirs = [
        messidor_dir / "IMAGES",
        messidor_dir / "Images",
        messidor_dir / "images",
        messidor_dir,
    ]
    image_dir = next((d for d in image_dirs if d.is_dir() and any(d.glob("*.jpg")) or any(d.glob("*.JPG"))), None)

    if csv_candidates:
        meta = pd.read_csv(csv_candidates[0], sep=";" if ";" in open(csv_candidates[0], encoding="utf-8", errors="ignore").read(200) else ",")
        meta.columns = [c.strip().lower() for c in meta.columns]
        for _, row in meta.iterrows():
            name = None
            for col in ("image", "image_name", "filename", "file"):
                if col in meta.columns:
                    name = str(row[col])
                    break
            if name is None:
                continue
            grade = None
            for col in ("grade", "dr_grade", "retinopathy_grade", "label"):
                if col in meta.columns:
                    grade = row[col]
                    break
            if grade is None:
                continue
            label = 0 if int(grade) == 0 else 1
            src = None
            for base in image_dirs:
                for ext in ("", ".jpg", ".JPG", ".png"):
                    cand = base / f"{name}{ext}" if ext else base / name
                    if cand.exists():
                        src = cand
                        break
                if src:
                    break
            if src is None:
                continue
            dst = IMG / "messidor" / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                import shutil
                shutil.copy2(src, dst)
            rows.append(
                {
                    "image_path": f"messidor/{dst.name}",
                    "patient_id": Path(name).stem,
                    "label": label,
                    "patient_age": row.get("age", pd.NA) if "age" in meta.columns else pd.NA,
                    "patient_sex": pd.NA,
                }
            )
    else:
        if image_dir is None:
            raise FileNotFoundError(f"No MESSIDOR images found under {messidor_dir}")
        for src in sorted(list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.JPG"))):
            # Filename patterns like ImageXX_Y_Z.jpg — last number often grade
            parts = src.stem.replace("-", "_").split("_")
            grade = None
            for p in reversed(parts):
                if p.isdigit() and int(p) <= 4:
                    grade = int(p)
                    break
            if grade is None:
                continue
            dst = IMG / "messidor" / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                import shutil
                shutil.copy2(src, dst)
            rows.append(
                {
                    "image_path": f"messidor/{dst.name}",
                    "patient_id": src.stem,
                    "label": 0 if grade == 0 else 1,
                    "patient_age": pd.NA,
                    "patient_sex": pd.NA,
                }
            )

    test_df = pd.DataFrame(rows)
    if test_df.empty:
        raise RuntimeError("No MESSIDOR rows built. Check directory layout.")
    return test_df.reset_index(drop=True)


def extract_zip(zip_path: Path, dest: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare APTOS + MESSIDOR pilot CSVs")
    parser.add_argument("--aptos-dir", type=str, default=str(ROOT / "data" / "raw" / "aptos"))
    parser.add_argument("--messidor-dir", type=str, default=str(ROOT / "data" / "raw" / "messidor"))
    parser.add_argument("--aptos-zip", type=str, default=None, help="Optional zip to extract first")
    parser.add_argument("--messidor-zip", type=str, default=None)
    parser.add_argument("--sample", type=int, default=0, help="If >0, subsample APTOS train for quick pilot")
    args = parser.parse_args()

    aptos_dir = Path(args.aptos_dir)
    messidor_dir = Path(args.messidor_dir)
    if args.aptos_zip:
        extract_zip(Path(args.aptos_zip), aptos_dir)
    if args.messidor_zip:
        extract_zip(Path(args.messidor_zip), messidor_dir)

    OUT.mkdir(parents=True, exist_ok=True)
    train_df, val_df = prepare_aptos(aptos_dir)
    if args.sample and args.sample < len(train_df):
        train_df = train_df.sample(n=args.sample, random_state=42).reset_index(drop=True)

    test_df = prepare_messidor(messidor_dir)

    train_df.to_csv(OUT / "aptos_train.csv", index=False)
    val_df.to_csv(OUT / "aptos_val.csv", index=False)
    test_df.to_csv(OUT / "messidor_test.csv", index=False)

    print(f"Pilot CSVs written to {OUT}")
    print(f"  APTOS train={len(train_df)} val={len(val_df)}")
    print(f"  MESSIDOR test={len(test_df)}")
    print(f"  Images under {IMG}")


if __name__ == "__main__":
    main()
