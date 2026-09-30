#!/usr/bin/env python3
"""Create minimal synthetic stand-in dataset for pipeline smoke tests."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "standin"
IMG = OUT / "images"


def make_split(n: int, prefix: str, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        pid = i // 2
        rows.append(
            {
                "image_path": f"{prefix}_{i:04d}.png",
                "patient_id": f"p{pid}",
                "label": int(rng.random() > 0.7),
                "patient_age": float(rng.integers(25, 85)),
                "patient_sex": int(rng.choice([1, 2])),
            }
        )
    return pd.DataFrame(rows)


def write_images(df: pd.DataFrame) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    for _, row in df.iterrows():
        path = IMG / row["image_path"]
        if path.exists():
            continue
        arr = np.random.default_rng(hash(row["image_path"]) % 2**32).integers(0, 255, (224, 224, 3), dtype=np.uint8)
        Image.fromarray(arr).save(path)


def main() -> None:
    train = make_split(40, "aptos_tr", 42)
    val = make_split(16, "aptos_va", 43)
    test = make_split(24, "mess_te", 44)
    all_df = pd.concat([train, val, test], ignore_index=True)
    write_images(all_df)

    OUT.mkdir(parents=True, exist_ok=True)
    train.to_csv(OUT / "aptos_train.csv", index=False)
    val.to_csv(OUT / "aptos_val.csv", index=False)
    test.to_csv(OUT / "messidor_test.csv", index=False)
    print(f"Stand-in data written to {OUT}")
    print(f"  train={len(train)} val={len(val)} test={len(test)} images={len(list(IMG.glob('*.png')))}")


if __name__ == "__main__":
    main()
