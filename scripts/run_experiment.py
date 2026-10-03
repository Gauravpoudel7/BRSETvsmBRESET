#!/usr/bin/env python3
"""End-to-end experiment runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import yaml
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.bootstrap import bootstrap_auroc, bootstrap_gap, save_bootstrap_results
from src.data import (
    FundusDataset,
    build_transforms,
    collate_with_meta,
    load_metadata,
    prepare_dataframe,
)
from src.evaluate import collect_predictions, compute_metrics_from_logits
from src.models import build_model
from src.subgroups import assign_groups, equity_scaled_auc, min_subgroup_auroc, parse_age, subgroup_auroc_table
from src.train import evaluate_loader, fit


def load_config(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def image_root_for(cfg: dict, which: str) -> str:
    data_cfg = cfg["data"]
    if which == "mbrset":
        return data_cfg.get("mbrset_image_root") or data_cfg["image_root"]
    return data_cfg.get("brset_image_root") or data_cfg["image_root"]


def cache_dir_for(cfg: dict, which: str) -> Path | None:
    root = cfg.get("data", {}).get("cache_root")
    if not root:
        return None
    return Path(root) / which


def make_loader(df, cfg, train: bool, image_root: str, cache_dir: str | Path | None = None):
    data_cfg = cfg["data"]
    label_col = "label" if "label" in df.columns else data_cfg["label_col"]
    image_col = data_cfg["image_col"] if data_cfg["image_col"] in df.columns else "image_id"
    ds = FundusDataset(
        df=df,
        image_col=image_col,
        label_col=label_col,
        image_root=image_root,
        cache_dir=cache_dir,
        transform=build_transforms(
            cfg["model"]["image_size"], train=train, fundus_crop=bool(data_cfg.get("fundus_crop", False)),
            aug=str(cfg["train"].get("augment", "basic")),
            crop_scale_min=cfg["train"].get("crop_scale_min"),
        ),
    )
    return DataLoader(
        ds,
        batch_size=int(cfg["train"]["batch_size"]),
        shuffle=train,
        num_workers=int(cfg["train"].get("num_workers", 0)),
        collate_fn=collate_with_meta,
        pin_memory=torch.cuda.is_available(),
    )


def resolve_csv(cfg: dict, key: str) -> Path:
    data_cfg = cfg["data"]
    path = Path(data_cfg[key])
    if not path.is_absolute():
        path = ROOT / path
    if path.exists():
        return path
    if "splits_dir" in data_cfg and key in {"train_csv", "val_csv", "test_csv", "external_test_csv"}:
        alt = ROOT / data_cfg.get("splits_dir", "") / Path(data_cfg[key]).name
        if alt.exists():
            return alt
    return path


def limit_rows(df: pd.DataFrame, n: int | None, seed: int) -> pd.DataFrame:
    if n is None or len(df) <= int(n):
        return df
    n = int(n)
    if "label" in df.columns and df["label"].nunique() > 1:
        parts = []
        remaining = n
        groups = list(df.groupby("label"))
        for i, (_, part) in enumerate(groups):
            if i == len(groups) - 1:
                take = remaining
            else:
                take = max(1, int(round(n * len(part) / len(df))))
                take = min(take, len(part), remaining)
            parts.append(part.sample(n=take, random_state=seed))
            remaining -= take
        out = pd.concat(parts, ignore_index=True)
        return out.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, default=None, help="For exp2: skip training")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Continue training from <output>/last_checkpoint.pt",
    )
    parser.add_argument("--experiment", type=str, default=None, help="Override config experiment (exp1 or exp2)")
    parser.add_argument("--output", type=str, default=None, help="Override config output directory")
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    if args.experiment:
        cfg["experiment"] = args.experiment
    if args.output:
        cfg.setdefault("output", {})["dir"] = args.output
    set_seed(int(cfg.get("seed", 42)))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    data_cfg = cfg["data"]
    out_dir = Path(cfg["output"]["dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    train_df = prepare_dataframe(
        load_metadata(resolve_csv(cfg, "train_csv")),
        data_cfg["label_col"],
        binary_label=data_cfg.get("binary_label", True),
        restrict_diabetic_only=data_cfg.get("restrict_diabetic_only", False),
    )
    val_df = prepare_dataframe(
        load_metadata(resolve_csv(cfg, "val_csv")),
        data_cfg["label_col"],
        binary_label=data_cfg.get("binary_label", True),
        restrict_diabetic_only=data_cfg.get("restrict_diabetic_only", False),
    )

    experiment = cfg.get("experiment", "exp1")
    if experiment == "exp2":
        test_key = "external_test_csv" if "external_test_csv" in data_cfg else "test_csv"
    else:
        test_key = "test_csv"

    test_df = prepare_dataframe(
        load_metadata(resolve_csv(cfg, test_key)),
        data_cfg["label_col"],
        binary_label=data_cfg.get("binary_label", True),
        restrict_diabetic_only=False,
    )

    seed = int(cfg.get("seed", 42))
    train_df = limit_rows(train_df, data_cfg.get("max_train_rows"), seed)
    val_df = limit_rows(val_df, data_cfg.get("max_val_rows"), seed)
    test_df = limit_rows(test_df, data_cfg.get("max_test_rows"), seed)

    brset_root = image_root_for(cfg, "brset")
    test_which = "mbrset" if experiment == "exp2" else "brset"
    test_root = image_root_for(cfg, test_which)
    train_loader = make_loader(
        train_df, cfg, train=True, image_root=brset_root, cache_dir=cache_dir_for(cfg, "brset")
    )
    val_loader = make_loader(
        val_df, cfg, train=False, image_root=brset_root, cache_dir=cache_dir_for(cfg, "brset")
    )
    test_loader = make_loader(
        test_df, cfg, train=False, image_root=test_root, cache_dir=cache_dir_for(cfg, test_which)
    )

    model = build_model(cfg, device)

    resume_path = None
    if args.resume:
        resume_path = out_dir / "last_checkpoint.pt"
        if not resume_path.is_file():
            raise FileNotFoundError(f"No checkpoint to resume: {resume_path}")

    if args.resume:
        model = fit(model, train_loader, val_loader, cfg, device, out_dir, resume_path=resume_path)
    elif args.checkpoint:
        state = torch.load(args.checkpoint, map_location=device, weights_only=False)
        model.load_state_dict(state["model"] if "model" in state else state)
    elif experiment != "exp2" or not (out_dir / "best_model.pt").exists():
        model = fit(model, train_loader, val_loader, cfg, device, out_dir)

    def report(loader, dest: Path, subgroup_cols: list) -> None:
        dest.mkdir(parents=True, exist_ok=True)
        use_amp = bool(cfg.get("train", {}).get("amp", False)) and device.type == "cuda"
        test_metrics = evaluate_loader(model, loader, device, use_amp=use_amp)
        print(f"Test metrics ({dest.name}): {test_metrics}")
        probs, labels, metas = collect_predictions(model, loader, device)
        patient_col = data_cfg.get("patient_col")
        patient_ids = (
            np.array([m.get(patient_col, i) for i, m in enumerate(metas)]) if patient_col else None
        )
        age_vals = pd.Series([parse_age(m.get("patient_age", m.get("age"))) for m in metas]).dropna()
        age_median = float(age_vals.median()) if len(age_vals) else None
        subgroup_df = (
            subgroup_auroc_table(probs, labels, metas, subgroup_cols, age_median=age_median)
            if subgroup_cols
            else pd.DataFrame()
        )
        esa = equity_scaled_auc(subgroup_df) if not subgroup_df.empty else None
        boot_n = int(cfg.get("eval", {}).get("bootstrap_samples", 200))
        boot_overall = bootstrap_auroc(
            probs, labels, patient_ids, n_samples=boot_n, seed=int(cfg.get("seed", 42))
        )
        boot_gaps = {}
        if not subgroup_df.empty:
            meta_df = pd.DataFrame(metas)
            for attr in subgroup_df["attribute"].unique():
                inc = subgroup_df[(subgroup_df["attribute"] == attr) & subgroup_df["included"]]["subgroup"].tolist()
                groups = assign_groups(meta_df, attr, age_median if attr in {"patient_age", "age"} else None).values
                boot_gaps[attr] = bootstrap_gap(
                    probs, labels, groups, patient_ids, inc, n_samples=boot_n, seed=int(cfg.get("seed", 42))
                )
        pred_df = pd.DataFrame({"patient_id": patient_ids if patient_ids is not None else np.arange(len(probs)),
                                "prob": probs, "label": labels})
        pred_df.to_csv(dest / "predictions.csv", index=False)
        overall_payload = {**test_metrics, "equity_scaled_auc": esa,
                           "min_subgroup_auroc": min_subgroup_auroc(subgroup_df) if not subgroup_df.empty else None,
                           "bootstrap": boot_overall}
        (dest / "overall_metrics.json").write_text(json.dumps(overall_payload, indent=2), encoding="utf-8")
        if not subgroup_df.empty:
            subgroup_df.to_csv(dest / "subgroup_metrics.csv", index=False)
        save_bootstrap_results(dest / "bootstrap_gaps.json", boot_overall, boot_gaps)

    primary_subgroups = data_cfg.get("subgroup_columns", [])
    if experiment == "exp2":
        primary_subgroups = data_cfg.get("mbrset_subgroup_columns", primary_subgroups)
    report(test_loader, out_dir, primary_subgroups)

    if data_cfg.get("also_eval_external") and "external_test_csv" in data_cfg:
        external_df = prepare_dataframe(
            load_metadata(resolve_csv(cfg, "external_test_csv")),
            data_cfg["label_col"],
            binary_label=data_cfg.get("binary_label", True),
            restrict_diabetic_only=False,
        )
        external_df = limit_rows(external_df, data_cfg.get("max_external_rows"), seed)
        external_loader = make_loader(
            external_df,
            cfg,
            train=False,
            image_root=image_root_for(cfg, "mbrset"),
            cache_dir=cache_dir_for(cfg, "mbrset"),
        )
        report(
            external_loader,
            out_dir / "mbrset_external",
            data_cfg.get("mbrset_subgroup_columns", primary_subgroups),
        )

    runtime = {
        "device": str(device),
        "batch_size": cfg["train"]["batch_size"],
        "experiment": experiment,
        "n_train": len(train_df),
        "n_val": len(val_df),
        "n_test": len(test_df),
    }
    (out_dir / "run_info.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")
    print(f"Results saved to {out_dir}")


if __name__ == "__main__":
    main()
