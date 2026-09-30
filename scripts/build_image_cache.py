#!/usr/bin/env python3
"""Resize split images to short side 256. Does not modify the raw files."""

from __future__ import annotations

import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data import cache_filename, resolve_image_path

CACHE = Path(r"C:\data\cache_256")
BRSET_RAW = Path(r"C:\data\brset_mbrset\brazilian-ophthalmological\1.0.2\fundus_photos")
MBRSET_RAW = Path(r"C:\data\brset_mbrset\mbrset\1.0\images")
SPLITS = ROOT / "data" / "splits"

JOBS = [
    ("brset", SPLITS / "brset_train_published.csv", BRSET_RAW),
    ("brset", SPLITS / "brset_val_published.csv", BRSET_RAW),
    ("brset", SPLITS / "brset_test_published.csv", BRSET_RAW),
    ("mbrset", SPLITS / "mbrset_test_published.csv", MBRSET_RAW),
]


def resize_short_side(image: Image.Image, short: int = 256) -> Image.Image:
    width, height = image.size
    scale = short / min(width, height)
    size = (max(1, round(width * scale)), max(1, round(height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def cache_one(src: str, dest: str) -> str:
    destination = Path(dest)
    if destination.exists():
        return "skipped"
    source = Path(src)
    if not source.exists():
        return "missing"
    with Image.open(source) as image:
        resized = resize_short_side(image.convert("RGB"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        resized.save(destination, format="JPEG", quality=95)
    return "written"


def main() -> None:
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for tag, csv_path, raw_root in JOBS:
        dest_dir = CACHE / tag
        dest_dir.mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(csv_path)
        print(f"{tag} {csv_path.name}: {len(df)} rows", flush=True)
        for image_id in df["image_id"].astype(str):
            dest = dest_dir / cache_filename(image_id)
            key = str(dest)
            if key in seen:
                continue
            seen.add(key)
            if dest.exists():
                continue
            src = resolve_image_path(pd.Series({"image_id": image_id}), "image_id", raw_root)
            pairs.append((str(src), str(dest)))

    workers = max(1, min(8, os.cpu_count() or 1))
    print(f"to_write={len(pairs)} workers={workers}", flush=True)
    written = skipped = missing = 0
    if pairs:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(cache_one, src, dest) for src, dest in pairs]
            for i, future in enumerate(as_completed(futures), start=1):
                status = future.result()
                if status == "written":
                    written += 1
                elif status == "skipped":
                    skipped += 1
                else:
                    missing += 1
                    print(f"missing raw file in batch item {i}", flush=True)
                if i % 500 == 0:
                    print(f"progress {i}/{len(pairs)} written={written}", flush=True)
    already = len(seen) - len(pairs)
    print(
        f"cache={CACHE} written={written} skipped_existing={already + skipped} "
        f"missing_raw={missing} unique={len(seen)}",
        flush=True,
    )
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
