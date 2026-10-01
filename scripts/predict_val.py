#!/usr/bin/env python3
"""Save validation-set predictions for a finished run (needed for temperature scaling)."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import numpy as np, pandas as pd, torch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from run_experiment import load_config, make_loader, resolve_csv, image_root_for, cache_dir_for
from src.data import load_metadata, prepare_dataframe
from src.evaluate import collect_predictions
from src.models import build_model

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); a = ap.parse_args()
    cfg = load_config(Path(a.config)); d = cfg["data"]
    out = Path(cfg["output"]["dir"]); dest = out / "val_predictions.csv"
    if dest.exists(): print("exists", dest); return
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    val = prepare_dataframe(load_metadata(resolve_csv(cfg, "val_csv")), d["label_col"],
                            binary_label=d.get("binary_label", True),
                            restrict_diabetic_only=d.get("restrict_diabetic_only", False))
    loader = make_loader(val, cfg, train=False, image_root=image_root_for(cfg, "brset"), cache_dir=cache_dir_for(cfg, "brset"))
    model = build_model(cfg, dev)
    st = torch.load(out / "best_model.pt", map_location=dev, weights_only=False)
    model.load_state_dict(st["model"] if "model" in st else st)
    probs, labels, metas = collect_predictions(model, loader, dev)
    pd.DataFrame({"patient_id": [m.get(d["patient_col"]) for m in metas], "prob": probs, "label": labels}).to_csv(dest, index=False)
    print("saved", dest, len(probs))

if __name__ == "__main__":
    main()
