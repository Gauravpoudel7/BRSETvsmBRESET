#!/usr/bin/env python3
"""Smoke test: PyTorch CUDA + optional RETFound weight load + one training step."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
import torch.nn as nn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def smoke_timm(device: torch.device) -> None:
    import timm

    model = timm.create_model("vit_base_patch16_224", pretrained=False, num_classes=2)
    model = model.to(device)
    x = torch.randn(2, 3, 224, 224, device=device)
    y = torch.tensor([0, 1], device=device)
    logits = model(x)
    loss = nn.CrossEntropyLoss()(logits, y)
    loss.backward()
    print(f"timm ViT forward+backward OK on {device}, loss={loss.item():.4f}")


def smoke_dinov3(device: torch.device) -> None:
    from src.models import build_model

    cfg = {
        "model": {
            "name": "dinov3",
            "backbone": "vit_large_patch16_dinov3.lvd1689m",
            "num_classes": 2,
            "pretrained": True,
            "freeze_backbone": False,
        }
    }
    model = build_model(cfg, device)
    x = torch.randn(1, 3, 224, 224, device=device)
    out = model(x)
    print(f"DINOv3 forward OK, output shape={tuple(out.shape)}")


def smoke_retfound(checkpoint: Path, device: torch.device) -> None:
    from src.models import build_model

    cfg = {
        "model": {
            "name": "retfound",
            "retfound_checkpoint": str(checkpoint),
            "num_classes": 2,
            "freeze_backbone": False,
        }
    }
    model = build_model(cfg, device)
    x = torch.randn(1, 3, 224, 224, device=device)
    out = model(x)
    print(f"RETFound load OK, output shape={tuple(out.shape)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["timm", "retfound", "dinov3"], default="timm")
    parser.add_argument("--checkpoint", type=str, default=None)
    args = parser.parse_args()

    print(f"Python: {sys.version}")
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if args.model == "timm":
        smoke_timm(device)
    elif args.model == "dinov3":
        smoke_dinov3(device)
    else:
        if not args.checkpoint:
            print("RETFound smoke test skipped: pass --checkpoint path/to/RETFound_cfp_weights.pth")
            print("Request access: https://huggingface.co/YukunZhou/RETFound_mae_natureCFP")
            sys.exit(0)
        smoke_retfound(Path(args.checkpoint), device)

    print("Smoke test passed.")


if __name__ == "__main__":
    main()
