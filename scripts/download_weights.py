#!/usr/bin/env python3
"""Download foundation model weights (RETFound via Hugging Face, DINOv3 via timm)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = ROOT / "weights"


def download_retfound(token: str | None = None) -> Path:
    from huggingface_hub import hf_hub_download

    WEIGHTS.mkdir(parents=True, exist_ok=True)
    dest = WEIGHTS / "RETFound_cfp_weights.pth"
    if dest.exists():
        print(f"RETFound already at {dest}")
        return dest

    kwargs = {"repo_id": "YukunZhou/RETFound_mae_natureCFP", "filename": "RETFound_cfp_weights.pth"}
    if token:
        kwargs["token"] = token
    try:
        path = hf_hub_download(**kwargs, local_dir=str(WEIGHTS), local_dir_use_symlinks=False)
        print(f"RETFound downloaded to {path}")
        return Path(path)
    except Exception as e:
        print(f"RETFound download failed (gated model — request access at Hugging Face): {e}")
        print("Manual: https://huggingface.co/YukunZhou/RETFound_mae_natureCFP")
        print(f"Place RETFound_cfp_weights.pth in {WEIGHTS}")
        return dest


def verify_dinov3() -> None:
    import timm
    import torch

    name = "vit_large_patch16_dinov3.lvd1689m"
    print(f"Loading DINOv3 via timm: {name}")
    model = timm.create_model(name, pretrained=True, num_classes=0)
    x = torch.randn(1, 3, 224, 224)
    out = model(x)
    print(f"DINOv3 OK, feature dim={out.shape[-1]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--retfound", action="store_true", help="Download RETFound from Hugging Face")
    parser.add_argument("--dinov3", action="store_true", help="Verify DINOv3 loads via timm")
    parser.add_argument("--hf-token", type=str, default=None)
    args = parser.parse_args()

    if not args.retfound and not args.dinov3:
        args.retfound = True
        args.dinov3 = True

    if args.retfound:
        download_retfound(args.hf_token)
    if args.dinov3:
        verify_dinov3()


if __name__ == "__main__":
    main()
