"""Training loop for binary DR classification."""

from __future__ import annotations

import os
import random
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.evaluate import compute_metrics_from_logits


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    scaler: torch.amp.GradScaler | None = None,
    accum_steps: int = 1,
    use_amp: bool = False,
    grade_weights: dict | None = None,
    lr_sched=None,
    epoch: int = 0,
) -> dict:
    model.train()
    total_loss = 0.0
    n = 0
    accum_steps = max(int(accum_steps), 1)
    optimizer.zero_grad(set_to_none=True)
    for step, (images, labels, metas) in enumerate(tqdm(loader, desc="train", leave=False)):
        if lr_sched is not None and step % accum_steps == 0:
            lr_sched(optimizer, epoch + step / len(loader))
        images = images.to(device)
        labels = labels.to(device)
        with torch.amp.autocast(device_type="cuda", enabled=use_amp):
            logits = model(images)
            per = criterion(logits, labels)
            if grade_weights is not None:
                w = torch.tensor([grade_weights[int(m["DR_ICDR"])] for m in metas], device=device, dtype=per.dtype)
                loss = (per * w).sum() / w.sum()
            else:
                loss = per.mean()
            loss = loss / accum_steps
        if use_amp and scaler is not None:
            scaler.scale(loss).backward()
        else:
            loss.backward()
        if (step + 1) % accum_steps == 0 or (step + 1) == len(loader):
            if use_amp and scaler is not None:
                scaler.step(optimizer)
                scaler.update()
            else:
                optimizer.step()
            optimizer.zero_grad(set_to_none=True)
        total_loss += loss.item() * accum_steps * len(labels)
        n += len(labels)
    return {"loss": total_loss / max(n, 1)}


@torch.no_grad()
def evaluate_loader(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    use_amp: bool = False,
) -> dict:
    model.eval()
    all_logits, all_labels = [], []
    for images, labels, _ in tqdm(loader, desc="eval", leave=False):
        images = images.to(device)
        with torch.amp.autocast(device_type="cuda", enabled=use_amp):
            logits = model(images)
        all_logits.append(logits.float().cpu())
        all_labels.append(labels)
    logits = torch.cat(all_logits)
    labels = torch.cat(all_labels)
    return compute_metrics_from_logits(logits, labels)


def capture_rng_state() -> dict:
    state = {
        "torch": torch.get_rng_state(),
        "numpy": np.random.get_state(),
        "python": random.getstate(),
    }
    if torch.cuda.is_available():
        state["cuda"] = torch.cuda.get_rng_state_all()
    return state


def restore_rng_state(state: dict) -> None:
    torch_state = state["torch"].detach().cpu().contiguous()
    torch.set_rng_state(torch_state)
    np.random.set_state(state["numpy"])
    random.setstate(state["python"])
    if state.get("cuda") and torch.cuda.is_available():
        torch.cuda.set_rng_state_all([item.detach().cpu().contiguous() for item in state["cuda"]])


def save_last_checkpoint(path: Path, payload: dict) -> None:
    """Write via a temp file, then rename, so a power cut cannot leave a half file."""
    temporary = path.with_name(path.name + ".tmp")
    torch.save(payload, temporary)
    os.replace(temporary, path)


def build_retfound_optimizer(model: nn.Module, train_cfg: dict):
    """AdamW + layer-wise lr decay + warmup/half-cycle cosine, as in RETFound main_finetune.py."""
    import math
    eff_batch = int(train_cfg["batch_size"]) * max(int(train_cfg.get("grad_accum_steps", 1)), 1)
    base_lr = float(train_cfg.get("blr", 5e-3)) * eff_batch / 256
    min_lr = float(train_cfg.get("min_lr", 1e-6))
    ld = float(train_cfg.get("layer_decay", 0.65))
    wd = float(train_cfg.get("weight_decay", 0.05))
    warmup = int(train_cfg.get("warmup_epochs", 10))
    total = int(train_cfg["epochs"])
    num_layers = len(model.backbone.blocks) + 1
    groups = {}
    for name, p in model.named_parameters():
        if not p.requires_grad:
            continue
        short = name[len("backbone."):] if name.startswith("backbone.") else None
        if short is not None and (short in ("cls_token", "pos_embed") or short.startswith("patch_embed")):
            lid = 0
        elif short is not None and short.startswith("blocks."):
            lid = int(short.split(".")[1]) + 1
        else:
            lid = num_layers
        no_wd = p.ndim == 1 or (short in ("cls_token", "pos_embed"))
        key = (lid, no_wd)
        if key not in groups:
            groups[key] = {"params": [], "weight_decay": 0.0 if no_wd else wd, "lr_scale": ld ** (num_layers - lid)}
        groups[key]["params"].append(p)
    optimizer = torch.optim.AdamW(list(groups.values()), lr=base_lr)

    def lr_sched(opt, ep: float):
        if ep < warmup:
            lr = base_lr * ep / warmup
        else:
            lr = min_lr + (base_lr - min_lr) * 0.5 * (1.0 + math.cos(math.pi * (ep - warmup) / (total - warmup)))
        for g in opt.param_groups:
            g["lr"] = lr * g["lr_scale"]

    print(f"RETFound optimizer: base_lr={base_lr:.2e} layer_decay={ld} wd={wd} warmup={warmup} groups={len(groups)}")
    return optimizer, lr_sched, warmup


def fit(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    cfg: dict,
    device: torch.device,
    output_dir: Path,
    resume_path: Path | None = None,
) -> nn.Module:
    train_cfg = cfg["train"]
    criterion = nn.CrossEntropyLoss(reduction="none", label_smoothing=float(train_cfg.get("label_smoothing", 0.0)))
    grade_weights = None
    if train_cfg.get("grade_weighting") == "sqrt_inv":
        # Square-root inverse frequency per ICDR grade (Lancet Digit Health 2026 RETFound study).
        counts = train_loader.dataset.df["DR_ICDR"].astype(int).value_counts()
        grade_weights = {int(g): float((counts.max() / n) ** 0.5) for g, n in counts.items()}
        print(f"grade_weights={grade_weights} counts={counts.sort_index().to_dict()}")
    lr_sched = None
    warmup = 0
    if train_cfg.get("optimizer") == "retfound":
        optimizer, lr_sched, warmup = build_retfound_optimizer(model, train_cfg)
    else:
        optimizer = torch.optim.Adam(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=float(train_cfg["learning_rate"]),
        )

    best_auroc = -1.0
    patience = int(train_cfg.get("early_stop_patience", 5))
    stale = 0
    use_amp = bool(train_cfg.get("amp", False)) and device.type == "cuda"
    accum_steps = int(train_cfg.get("grad_accum_steps", 1))
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "train_log.txt"
    start_epoch = 0
    if resume_path is not None:
        saved = torch.load(resume_path, map_location="cpu", weights_only=False)
        model.load_state_dict(saved["model"])
        optimizer.load_state_dict(saved["optimizer"])
        for slot in optimizer.state.values():
            for key, value in slot.items():
                if isinstance(value, torch.Tensor):
                    slot[key] = value.to(device)
        if use_amp and saved.get("scaler"):
            scaler.load_state_dict(saved["scaler"])
        best_auroc = float(saved["best_val_auroc"])
        stale = int(saved["early_stop_counter"])
        start_epoch = int(saved["epoch"])
        restore_rng_state(saved["rng"])
        print(
            f"Resumed from epoch {start_epoch} best_val_auroc={best_auroc} "
            f"early_stop_counter={stale}"
        )
        log_lines = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
    else:
        log_lines = []
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    print(
        f"Train settings: amp={use_amp} batch_size={train_cfg['batch_size']} "
        f"grad_accum_steps={accum_steps} "
        f"effective_batch={int(train_cfg['batch_size']) * max(accum_steps, 1)}"
    )

    total_epochs = int(train_cfg["epochs"])
    for epoch in range(start_epoch, total_epochs):
        t0 = time.time()
        train_stats = train_one_epoch(
            model,
            train_loader,
            optimizer,
            criterion,
            device,
            scaler=scaler,
            accum_steps=accum_steps,
            use_amp=use_amp,
            grade_weights=grade_weights,
            lr_sched=lr_sched,
            epoch=epoch,
        )
        train_s = time.time() - t0
        t1 = time.time()
        val_stats = evaluate_loader(model, val_loader, device, use_amp=use_amp)
        val_s = time.time() - t1
        finished_epoch = epoch + 1
        line = (
            f"epoch={finished_epoch} train_loss={train_stats['loss']:.4f} "
            f"val_auroc={val_stats['auroc']:.4f} train_s={train_s:.1f} val_s={val_s:.1f}"
        )
        print(line)
        log_lines.append(line)

        if val_stats["auroc"] > best_auroc:
            best_auroc = val_stats["auroc"]
            stale = 0
            torch.save(
                {"model": model.state_dict(), "epoch": finished_epoch, "val_auroc": best_auroc},
                output_dir / "best_model.pt",
            )
        elif finished_epoch > warmup:
            stale += 1

        if train_cfg.get("save_last_checkpoint", True):
          save_last_checkpoint(
            output_dir / "last_checkpoint.pt",
            {
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "scaler": scaler.state_dict() if use_amp else None,
                "scheduler": None,
                "epoch": finished_epoch,
                "best_val_auroc": best_auroc,
                "early_stop_counter": stale,
                "rng": capture_rng_state(),
            },
        )
        if stale >= patience:
            print(f"Early stop at epoch {finished_epoch}")
            break

    if device.type == "cuda":
        peak_mb = torch.cuda.max_memory_allocated(device) / (1024 ** 2)
        mem_line = f"peak_gpu_memory_mb={peak_mb:.1f}"
        print(mem_line)
        log_lines.append(mem_line)
    (output_dir / "train_log.txt").write_text("\n".join(log_lines), encoding="utf-8")
    ckpt = output_dir / "best_model.pt"
    if ckpt.exists():
        state = torch.load(ckpt, map_location=device, weights_only=False)
        model.load_state_dict(state["model"])
    return model
