"""Load fundus image datasets from CSV metadata."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


# Official mBRSET names -> names the rest of the pipeline already uses.
MBRSET_COLUMN_ALIASES = {
    "file": "image_id",
    "final_icdr": "DR_ICDR",
    "patient": "patient_id",
    "age": "patient_age",
    "sex": "patient_sex",
}


def load_metadata(csv_path: str | Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def normalize_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Rename mBRSET columns when the BRSET name is not already present."""
    out = df.copy()
    rename = {
        src: dst
        for src, dst in MBRSET_COLUMN_ALIASES.items()
        if src in out.columns and dst not in out.columns
    }
    out = out.rename(columns=rename)
    if "educational_level" in out.columns and "education" not in out.columns:
        out["education"] = out["educational_level"]
    return out


def cache_filename(image_id: object) -> str:
    name = str(image_id).strip()
    stem = Path(name).stem if name.lower().endswith((".png", ".jpg", ".jpeg", ".tif")) else name
    return f"{stem}.jpg"


def resolve_image_path(
    row: pd.Series,
    image_col: str,
    image_root: str | Path,
    cache_dir: str | Path | None = None,
) -> Path:
    raw = str(row[image_col])
    if cache_dir is not None:
        cached = Path(cache_dir) / cache_filename(raw)
        if cached.exists():
            return cached
    root = Path(image_root)
    candidate = root / raw
    if candidate.exists():
        return candidate
    if not raw.lower().endswith((".png", ".jpg", ".jpeg")):
        for ext in (".png", ".jpg", ".jpeg", ".tif"):
            alt = root / f"{raw}{ext}"
            if alt.exists():
                return alt
    return candidate


def binarize_dr_label(value: Any) -> int:
    """ICDR 0 = normal (0); 1-4 or string DR = positive (1)."""
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"normal", "0"}:
            return 0
        return 1
    try:
        num = int(value)
        return 0 if num == 0 else 1
    except (TypeError, ValueError):
        return 1


def prepare_dataframe(
    df: pd.DataFrame,
    label_col: str,
    binary_label: bool = True,
    restrict_diabetic_only: bool = False,
) -> pd.DataFrame:
    out = normalize_metadata(df)
    if restrict_diabetic_only and "diabetes" in out.columns:
        out = out[out["diabetes"].astype(str).str.lower().isin({"yes", "1", "true"})]
    if label_col not in out.columns and "DR_ICDR" in out.columns:
        label_col = "DR_ICDR"
    out = out.dropna(subset=[label_col])
    if binary_label:
        out["label"] = out[label_col].map(binarize_dr_label)
    else:
        out["label"] = out[label_col]
    return out.reset_index(drop=True)


class FundusCrop:
    """Crop to the bright fundus region, then pad to a square with black.

    BRSET photos are about 1.3:1 and mBRSET photos are square, so a plain
    Resize((224, 224)) squashes the BRSET fundus into an oval but keeps the
    mBRSET fundus round. Cropping first gives both the same round shape.
    """

    def __init__(self, threshold: int = 15, min_fraction: float = 0.02):
        self.threshold = threshold
        self.min_fraction = min_fraction

    def __call__(self, image: Image.Image) -> Image.Image:
        gray = np.asarray(image.convert("L"))
        mask = gray > self.threshold
        rows = np.where(mask.mean(axis=1) > self.min_fraction)[0]
        cols = np.where(mask.mean(axis=0) > self.min_fraction)[0]
        if len(rows) == 0 or len(cols) == 0:
            return image
        image = image.crop((int(cols.min()), int(rows.min()), int(cols.max()) + 1, int(rows.max()) + 1))
        w, h = image.size
        side = max(w, h)
        canvas = Image.new("RGB", (side, side), (0, 0, 0))
        canvas.paste(image, ((side - w) // 2, (side - h) // 2))
        return canvas


def build_transforms(image_size: int = 224, train: bool = True, fundus_crop: bool = False, aug: str = "basic") -> transforms.Compose:
    pre = [FundusCrop()] if fundus_crop else []
    if train and aug == "retfound":
        # Same train transform as the official RETFound main_finetune.py (timm create_transform,
        # RandAugment rand-m9-mstd0.5-inc1, random erasing p=0.25 pixel mode, bicubic).
        from timm.data import create_transform
        return transforms.Compose(pre + [create_transform(
            input_size=image_size, is_training=True, auto_augment="rand-m9-mstd0.5-inc1",
            re_prob=0.25, re_mode="pixel", re_count=1, interpolation="bicubic",
            mean=IMAGENET_MEAN, std=IMAGENET_STD)])
    if train:
        return transforms.Compose(
            pre
            + [
                transforms.Resize((image_size, image_size)),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
            ]
        )
    return transforms.Compose(
        pre
        + [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ]
    )


class FundusDataset(Dataset):
    def __init__(
        self,
        df: pd.DataFrame,
        image_col: str,
        label_col: str,
        image_root: str | Path,
        transform: transforms.Compose | None = None,
        cache_dir: str | Path | None = None,
    ):
        self.df = df.reset_index(drop=True)
        self.image_col = image_col
        self.label_col = label_col if label_col in self.df.columns else "label"
        self.image_root = Path(image_root)
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.transform = transform

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor, dict[str, Any]]:
        row = self.df.iloc[idx]
        path = resolve_image_path(row, self.image_col, self.image_root, self.cache_dir)
        image = Image.open(path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        label = int(row[self.label_col])
        meta = row.to_dict()
        return image, torch.tensor(label, dtype=torch.long), meta


def collate_with_meta(batch):
    images, labels, metas = zip(*batch)
    return torch.stack(images), torch.stack(labels), list(metas)
