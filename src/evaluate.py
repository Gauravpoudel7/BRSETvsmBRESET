"""Evaluation metrics for DR classification."""

from __future__ import annotations

import numpy as np
import torch
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix


def compute_metrics_from_logits(
    logits: torch.Tensor,
    labels: torch.Tensor,
    threshold: float = 0.5,
) -> dict:
    probs = torch.softmax(logits, dim=1)[:, 1].numpy()
    y = labels.numpy().astype(int)
    preds = (probs >= threshold).astype(int)

    out = {
        "n": int(len(y)),
        "accuracy": float(accuracy_score(y, preds)),
        "auroc": float("nan"),
        "sensitivity": float("nan"),
        "specificity": float("nan"),
    }
    if len(np.unique(y)) >= 2:
        out["auroc"] = float(roc_auc_score(y, probs))
        tn, fp, fn, tp = confusion_matrix(y, preds, labels=[0, 1]).ravel()
        out["sensitivity"] = float(tp / (tp + fn)) if (tp + fn) else float("nan")
        out["specificity"] = float(tn / (tn + fp)) if (tn + fp) else float("nan")
    return out


def collect_predictions(
    model,
    loader,
    device,
) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    model.eval()
    probs_list, labels_list, metas = [], [], []
    with torch.no_grad():
        for images, labels, meta in loader:
            images = images.to(device)
            logits = model(images)
            probs = torch.softmax(logits, dim=1)[:, 1].cpu().numpy()
            probs_list.append(probs)
            labels_list.append(labels.numpy())
            metas.extend(meta)
    return np.concatenate(probs_list), np.concatenate(labels_list), metas
