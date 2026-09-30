"""Model builders for foundation-model fine-tuning."""

from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn
import timm


class ClassificationHead(nn.Module):
    def __init__(self, in_features: int, num_classes: int, hidden: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class TimmClassifier(nn.Module):
    def __init__(
        self,
        backbone: str,
        num_classes: int = 2,
        pretrained: bool = True,
        freeze_backbone: bool = False,
        global_pool: str = "avg",
    ):
        super().__init__()
        self.backbone = timm.create_model(
            backbone, pretrained=pretrained, num_classes=0, global_pool=global_pool
        )
        feat_dim = self.backbone.num_features
        self.head = ClassificationHead(feat_dim, num_classes)
        if freeze_backbone:
            for p in self.backbone.parameters():
                p.requires_grad = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        feats = self.backbone(x)
        return self.head(feats)


def _resolve_checkpoint(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    repo_path = Path(__file__).resolve().parents[1] / candidate
    if repo_path.exists() or not candidate.exists():
        return repo_path
    return candidate


def build_model(cfg: dict, device: torch.device) -> nn.Module:
    model_cfg = cfg["model"]
    name = model_cfg.get("name", "timm")
    num_classes = model_cfg.get("num_classes", 2)
    freeze = model_cfg.get("freeze_backbone", False)

    if name == "retfound":
        checkpoint = model_cfg.get("retfound_checkpoint")
        if not checkpoint:
            raise FileNotFoundError("RETFound config is missing model.retfound_checkpoint")
        model = _load_retfound_classifier(checkpoint, num_classes, freeze)
    elif name == "dinov3":
        checkpoint = model_cfg.get("dinov3_checkpoint")
        backbone = model_cfg.get("backbone", "vit_large_patch16_dinov3.lvd1689m")
        if checkpoint and Path(checkpoint).exists():
            model = _load_dinov3_classifier(checkpoint, backbone, num_classes, freeze)
        else:
            model = TimmClassifier(
                backbone=backbone,
                num_classes=num_classes,
                pretrained=model_cfg.get("pretrained", True),
                freeze_backbone=freeze,
            )
    else:
        model = TimmClassifier(
            backbone=model_cfg.get("backbone", "vit_base_patch16_224"),
            num_classes=num_classes,
            pretrained=model_cfg.get("pretrained", True),
            freeze_backbone=freeze,
        )

    return model.to(device)


def _encoder_state(raw: dict) -> dict:
    """Keep RETFound encoder weights. Drop the MAE decoder and mask token."""
    cleaned = {}
    for key, value in raw.items():
        name = key
        for prefix in ("encoder.", "backbone.", "module."):
            if name.startswith(prefix):
                name = name[len(prefix) :]
        if name == "mask_token" or name.startswith("decoder"):
            continue
        cleaned[name] = value
    return cleaned


def _load_retfound_classifier(
    checkpoint_path: str | Path,
    num_classes: int,
    freeze_backbone: bool,
) -> nn.Module:
    """Load RETFound ViT-L encoder weights. Raise if the file or the match is bad."""
    path = _resolve_checkpoint(checkpoint_path)
    if not path.is_file():
        raise FileNotFoundError(f"RETFound checkpoint not found: {path}")

    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    if not isinstance(ckpt, dict) or "model" not in ckpt:
        raise RuntimeError(f"RETFound checkpoint {path} has no 'model' key")
    state = _encoder_state(ckpt["model"])

    model = TimmClassifier(
        backbone="vit_large_patch16_224",
        num_classes=num_classes,
        pretrained=False,
        freeze_backbone=freeze_backbone,
        global_pool="token",
    )
    encoder_keys = set(model.backbone.state_dict().keys())
    missing, unexpected = model.backbone.load_state_dict(state, strict=False)
    loaded = len(encoder_keys) - len(missing)
    print(
        f"RETFound load: loaded={loaded} missing={len(missing)} "
        f"unexpected={len(unexpected)} encoder_keys={len(encoder_keys)} path={path}"
    )
    if len(encoder_keys) == 0 or loaded / len(encoder_keys) < 0.90:
        raise RuntimeError(
            f"RETFound weights did not load into the ViT-L encoder "
            f"({loaded}/{len(encoder_keys)} keys). Refusing to continue with a random or timm stand-in."
        )
    return model


def _load_dinov3_classifier(
    checkpoint_path: str | Path,
    backbone: str,
    num_classes: int,
    freeze_backbone: bool,
) -> nn.Module:
    """Load DINOv3 ViT checkpoint from file; attach classification head."""
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    state = ckpt.get("model", ckpt.get("state_dict", ckpt))
    model = TimmClassifier(
        backbone=backbone,
        num_classes=num_classes,
        pretrained=False,
        freeze_backbone=freeze_backbone,
    )
    missing, unexpected = model.backbone.load_state_dict(state, strict=False)
    if missing:
        print(f"DINOv3 load: missing keys: {len(missing)}")
    if unexpected:
        print(f"DINOv3 load: unexpected keys: {len(unexpected)}")
    return model
