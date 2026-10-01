#!/usr/bin/env python3
"""Monte Carlo cross-validation (MCCV) splits.

Pools ALL diabetic BRSET patients (published train + val + test) and, for each repeat,
draws a new random patient-level 60/20/20 train/val/test split, stratified by whether
the patient has any DR. mBRSET stays fixed as the external test set.
Also writes one config per repeat.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-config", default="configs/brset_mbrset_retfound.yaml")
    ap.add_argument("--repeats", type=int, default=10)
    ap.add_argument("--val-frac", type=float, default=0.20)
    ap.add_argument("--test-frac", type=float, default=0.20)
    ap.add_argument("--out-root", default="C:/data/mccv")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(ROOT / args.base_config, encoding="utf-8"))
    tr = pd.read_csv(ROOT / cfg["data"]["train_csv"])
    va = pd.read_csv(ROOT / cfg["data"]["val_csv"])
    te = pd.read_csv(ROOT / "data/splits/brset_test_diabetic.csv")
    pool = pd.concat([tr, va, te], ignore_index=True)
    pcol = cfg["data"]["patient_col"]
    pos = pool.groupby(pcol)["DR_ICDR"].apply(lambda s: int((s.fillna(0) > 0).any()))
    split_dir = ROOT / "data" / "splits" / "mccv"
    split_dir.mkdir(parents=True, exist_ok=True)
    cfg_dir = ROOT / "configs" / "mccv"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for r in range(1, args.repeats + 1):
        rng = np.random.default_rng(1000 + r)
        val_pat, test_pat = [], []
        for lab in (0, 1):
            ids = pos[pos == lab].index.to_numpy().copy()
            rng.shuffle(ids)
            n_te = int(round(len(ids) * args.test_frac)); n_va = int(round(len(ids) * args.val_frac))
            test_pat.extend(ids[:n_te]); val_pat.extend(ids[n_te:n_te + n_va])
        is_te = pool[pcol].isin(set(test_pat)); is_va = pool[pcol].isin(set(val_pat))
        tr_r, va_r, te_r = pool[~is_te & ~is_va], pool[is_va], pool[is_te]
        assert not set(tr_r[pcol]) & set(va_r[pcol]) and not set(tr_r[pcol]) & set(te_r[pcol]) and not set(va_r[pcol]) & set(te_r[pcol])
        tr_p = split_dir / f"train_r{r:02d}.csv"; va_p = split_dir / f"val_r{r:02d}.csv"; te_p = split_dir / f"test_r{r:02d}.csv"
        tr_r.to_csv(tr_p, index=False); va_r.to_csv(va_p, index=False); te_r.to_csv(te_p, index=False)
        c = yaml.safe_load(open(ROOT / args.base_config, encoding="utf-8"))
        c["seed"] = 1000 + r
        c["data"]["train_csv"] = tr_p.relative_to(ROOT).as_posix()
        c["data"]["val_csv"] = va_p.relative_to(ROOT).as_posix()
        c["data"]["test_csv"] = te_p.relative_to(ROOT).as_posix()
        c["data"]["also_eval_external"] = True
        c["output"]["dir"] = f"{args.out_root}/run_r{r:02d}"
        c["experiment"] = "exp1"
        yaml.safe_dump(c, open(cfg_dir / f"mccv_r{r:02d}.yaml", "w", encoding="utf-8"), sort_keys=False)
        rows.append({"repeat": r, "train_images": len(tr_r), "train_patients": tr_r[pcol].nunique(),
                     "val_images": len(va_r), "val_patients": va_r[pcol].nunique(),
                     "val_pos_images": int((va_r["DR_ICDR"] > 0).sum()),
                     "test_images": len(te_r), "test_patients": te_r[pcol].nunique(),
                     "test_pos_images": int((te_r["DR_ICDR"] > 0).sum())})
    summ = pd.DataFrame(rows)
    summ.to_csv(split_dir / "mccv_split_summary.csv", index=False)
    print(summ.to_string(index=False))

if __name__ == "__main__":
    main()
