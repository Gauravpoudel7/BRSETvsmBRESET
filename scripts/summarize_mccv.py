#!/usr/bin/env python3
"""Summarise MCCV runs (BRSET test differs per repeat; mBRSET is fixed).

Per run and test set: AUROC (any DR, referable), sensitivity/specificity at 10% FPR with
Wilson 95% CIs, Cohen's kappa, calibration (Brier score, ECE) before and after temperature
scaling fitted on that run's validation set, and PPV/NPV at example screening prevalences.
Writes mccv_per_run.csv, mccv_summary.csv and reliability_<test>.png in --root.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import minimize_scalar
from sklearn.metrics import roc_auc_score, cohen_kappa_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data import load_metadata, prepare_dataframe

EPS = 1e-6
PREVALENCES = (0.05, 0.10, 0.20)  # example scenarios, not measured values

def referable(df):
    g = df["DR_ICDR"].astype(float) >= 2
    if "final_edema" in df.columns:
        g = g | (df["final_edema"].astype(str).str.lower() == "yes")
    elif "macular_edema" in df.columns:
        g = g | (pd.to_numeric(df["macular_edema"], errors="coerce") == 1)
    return g.to_numpy().astype(int)

def wilson(k, n, z=1.959964):
    if n == 0: return (np.nan, np.nan)
    p = k / n; den = 1 + z*z/n
    c = (p + z*z/(2*n)) / den; h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
    return (c - h, c + h)

def logit(p): p = np.clip(p, EPS, 1-EPS); return np.log(p/(1-p))
def sigmoid(z): return 1/(1+np.exp(-z))

def fit_temperature(p, y):
    z = logit(p)
    nll = lambda t: -np.mean(y*np.log(np.clip(sigmoid(z/t),EPS,1)) + (1-y)*np.log(np.clip(1-sigmoid(z/t),EPS,1)))
    return float(minimize_scalar(nll, bounds=(0.05, 50), method="bounded").x)

def ece(p, y, bins=10):
    edges = np.linspace(0, 1, bins+1); idx = np.clip(np.digitize(p, edges[1:-1]), 0, bins-1); e = 0.0
    for b in range(bins):
        m = idx == b
        if m.any(): e += m.mean() * abs(p[m].mean() - y[m].mean())
    return float(e)

def at_10fpr(prob, lab, prefix):
    thr = np.quantile(prob[lab == 0], 0.90); pred = (prob > thr).astype(int)
    tp = int(((pred==1)&(lab==1)).sum()); fn = int(((pred==0)&(lab==1)).sum())
    tn = int(((pred==0)&(lab==0)).sum()); fp = int(((pred==1)&(lab==0)).sum())
    sens, spec = tp/(tp+fn), tn/(tn+fp)
    o = {f"{prefix}sens_at_10fpr": sens, f"{prefix}sens_lo": wilson(tp,tp+fn)[0], f"{prefix}sens_hi": wilson(tp,tp+fn)[1],
         f"{prefix}spec_at_10fpr": spec, f"{prefix}spec_lo": wilson(tn,tn+fp)[0], f"{prefix}spec_hi": wilson(tn,tn+fp)[1],
         f"{prefix}kappa_at_10fpr": cohen_kappa_score(lab, pred), f"{prefix}n_pos": tp+fn, f"{prefix}n_neg": tn+fp}
    for pr in PREVALENCES:
        o[f"{prefix}ppv_prev{int(pr*100)}"] = sens*pr / (sens*pr + (1-spec)*(1-pr))
        o[f"{prefix}npv_prev{int(pr*100)}"] = spec*(1-pr) / (spec*(1-pr) + (1-sens)*pr)
    return o

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="C:/data/mccv")
    ap.add_argument("--mbrset-test", default="data/splits/mbrset_test_published.csv")
    args = ap.parse_args()
    rows, rel = [], {}
    for run in sorted(Path(args.root).glob("run_r*")):
        r = run.name.replace("run_", "")
        vf = run / "val_predictions.csv"
        T = None
        if vf.exists():
            v = pd.read_csv(vf); T = fit_temperature(v["prob"].to_numpy(), v["label"].to_numpy())
        tests = {"BRSET": (Path(""), ROOT / "data/splits/mccv" / f"test_{r}.csv"),
                 "mBRSET": (Path("mbrset_external"), ROOT / args.mbrset_test)}
        for name, (sub, csv) in tests.items():
            pf = run / sub / "predictions.csv"
            if not pf.exists(): continue
            pred = pd.read_csv(pf)
            meta = prepare_dataframe(load_metadata(csv), "DR_ICDR", binary_label=True)
            assert len(meta) == len(pred), (pf, len(meta), len(pred))
            assert (meta["label"].to_numpy() == pred["label"].to_numpy()).all(), pf
            p, y, ref = pred["prob"].to_numpy(), pred["label"].to_numpy(), referable(meta)
            m = {"run": run.name, "test": name, "auroc_any": roc_auc_score(y, p), "auroc_referable": roc_auc_score(ref, p),
                 "sens_at_0.5": float((p[y==1] > 0.5).mean())}
            m.update(at_10fpr(p, y, "")); m.update(at_10fpr(p, ref, "ref_"))
            m["brier"] = float(np.mean((p-y)**2)); m["ece"] = ece(p, y)
            m["mean_pred"] = float(p.mean()); m["observed_rate"] = float(y.mean())
            if T is not None:
                pt = sigmoid(logit(p)/T); m["temperature"] = T
                m["brier_tscaled"] = float(np.mean((pt-y)**2)); m["ece_tscaled"] = ece(pt, y)
            else:
                pt = None
            om = json.loads((run / sub / "overall_metrics.json").read_text())
            m["es_auc"] = om.get("equity_scaled_auc")
            rows.append(m)
            rel.setdefault(name, []).append((p, y, pt))
    df = pd.DataFrame(rows)
    if df.empty: print("No finished runs yet."); return
    root = Path(args.root)
    df.to_csv(root / "mccv_per_run.csv", index=False)
    cols = [c for c in df.columns if c not in ("run", "test")]
    agg = df.groupby("test")[cols].agg(["mean", "std", "min", "max"]).T
    agg.to_csv(root / "mccv_summary.csv")
    print(df.groupby("test").size().rename("runs_done").to_string())
    print(agg.round(3).to_string())
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        for name, items in rel.items():
            fig, ax = plt.subplots(figsize=(4.5, 4.5)); ax.plot([0,1],[0,1],"k--",lw=1,label="perfect")
            for lab_, k in (("raw", 0), ("temperature-scaled", 2)):
                ps = [it[k] for it in items if it[k] is not None]
                if not ps: continue
                P = np.concatenate(ps); Y = np.concatenate([it[1] for it in items if it[k] is not None])
                edges = np.linspace(0,1,11); idx = np.clip(np.digitize(P, edges[1:-1]),0,9)
                xs = [P[idx==b].mean() for b in range(10) if (idx==b).sum() >= 10]
                ys = [Y[idx==b].mean() for b in range(10) if (idx==b).sum() >= 10]
                ax.plot(xs, ys, "o-", label=lab_)
            ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed DR rate"); ax.set_title(f"Reliability, {name} (all runs pooled)")
            ax.legend(); fig.tight_layout(); fig.savefig(root / f"reliability_{name}.png", dpi=150); plt.close(fig)
    except Exception as e:
        print("plot skipped:", e)

if __name__ == "__main__":
    main()
