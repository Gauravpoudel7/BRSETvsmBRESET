#!/usr/bin/env python3
"""Build pilot CSVs from Hugging Face mirrors (no Kaggle / ADCIS form required)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "pilot"
IMG = OUT / "images"


def _save_image(img, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        img.save(path)


def prepare_aptos_hf(max_images: int = 800, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    if max_images <= 0:
        train = pd.read_csv(OUT / "aptos_train.csv")
        val = pd.read_csv(OUT / "aptos_val.csv")
        return train, val

    from datasets import load_dataset

    repos = [
        "sngsfydy/aptos_train",
        "EslamHasan/APTOS2019DiabeticRetinopathy",
        "ming0100/aptos",
    ]
    rows = []
    for repo in repos:
        try:
            ds = load_dataset(repo, split="train")
            print(f"APTOS source: {repo} ({len(ds)} rows)")
            for i, ex in enumerate(ds):
                if len(rows) >= max_images:
                    break
                img = ex.get("image")
                if img is None:
                    continue
                label_raw = ex.get("label", ex.get("diagnosis", ex.get("class", 0)))
                code = str(ex.get("id_code", ex.get("id", f"aptos_{i}")))
                fname = re.sub(r"[^\w.-]", "_", code) + ".png"
                _save_image(img, IMG / "aptos" / fname)
                rows.append(
                    {
                        "image_path": f"aptos/{fname}",
                        "patient_id": code,
                        "label": 0 if int(label_raw) == 0 else 1,
                        "patient_age": None,
                        "patient_sex": None,
                    }
                )
            if rows:
                break
        except Exception as e:
            print(f"  skip {repo}: {e}")

    if not rows:
        raise RuntimeError("No APTOS images loaded from Hugging Face.")

    df = pd.DataFrame(rows)
    return train_test_split(df, test_size=0.15, random_state=seed, stratify=df["label"])


def _messidor_binary_label(ex: dict) -> int:
    """Map OctoMed/Messidor2 QA fields to binary DR label."""
    ans = str(ex.get("answer", "")).strip()
    opts = ex.get("options") or []
    if isinstance(opts, str):
        opts = [opts]

    # Letter answer (A, B, C, ...)
    if len(ans) == 1 and ans.isalpha() and opts:
        idx = ord(ans.upper()) - ord("A")
        if 0 <= idx < len(opts):
            text = str(opts[idx]).lower()
            if any(k in text for k in ("no dr", "no diabetic", "normal", "grade 0", "r0", "none")):
                return 0
            return 1

    lower = ans.lower()
    if "no dr" in lower or "no diabetic" in lower or "normal" in lower:
        return 0
    for ch in ans:
        if ch.isdigit():
            return 0 if int(ch) == 0 else 1

    if opts:
        for i, opt in enumerate(opts):
            if str(opt) == ans or str(opt).lower() in lower:
                return 0 if i == 0 else 1
    return 1


def prepare_messidor_hf(max_images: int = 300) -> pd.DataFrame:
    from datasets import load_dataset

    print("Loading OctoMed/Messidor2 (streaming)...")
    ds = load_dataset("OctoMed/Messidor2", split="test", streaming=True)
    rows = []
    for i, ex in enumerate(ds):
        if len(rows) >= max_images:
            break
        img = ex["image"]
        label = _messidor_binary_label(ex)
        fname = f"mess_{i:04d}.png"
        _save_image(img, IMG / "messidor" / fname)
        rows.append(
            {
                "image_path": f"messidor/{fname}",
                "patient_id": f"m{i}",
                "label": label,
                "patient_age": None,
                "patient_sex": None,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aptos-max", type=int, default=800)
    parser.add_argument("--messidor-max", type=int, default=300)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    train_df, val_df = prepare_aptos_hf(max_images=args.aptos_max)
    test_df = prepare_messidor_hf(max_images=args.messidor_max)

    train_df.to_csv(OUT / "aptos_train.csv", index=False)
    val_df.to_csv(OUT / "aptos_val.csv", index=False)
    test_df.to_csv(OUT / "messidor_test.csv", index=False)

    print(f"Pilot data ready under {OUT}")
    print(f"  APTOS train={len(train_df)} val={len(val_df)}")
    print(f"  MESSIDOR test={len(test_df)}")


if __name__ == "__main__":
    main()
