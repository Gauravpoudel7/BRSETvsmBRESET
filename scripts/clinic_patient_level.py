"""Patient-level (worst eye) per-grade detection with validation cut-off, Jeffreys 95% CIs,
and a 100-patient clinic simulation (54/30/10/5/1) with likelihood ratios. Pools 10 MCCV runs."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, ".")
from src.data import load_metadata, prepare_dataframe
from sklearn.metrics import roc_auc_score
from scipy.stats import beta
MIX = np.array([54, 30, 10, 5, 1]) / 100
def load(csv, pf):
    m = prepare_dataframe(load_metadata(csv), "DR_ICDR", binary_label=True).reset_index(drop=True)
    p = pd.read_csv(pf); assert len(m) == len(p) and (m.label.values == p.label.values).all()
    m["prob"] = p.prob.values; m["g"] = m.DR_ICDR.astype(int); return m
def pat(d): return d.groupby("patient_id").agg(prob=("prob", "max"), g=("g", "max")).reset_index()
def main():
    out = {}
    for level in ("image", "patient"):
        for name in ("BRSET", "mBRSET"):
            hits = {k: [0, 0] for k in range(5)}; aucs = []; aucw = []
            for r in range(1, 11):
                t = f"r{r:02d}"
                v = load(f"data/splits/mccv/val_{t}.csv", f"C:/data/mccv/run_{t}/val_predictions.csv")
                tf = (f"data/splits/mccv/test_{t}.csv", f"C:/data/mccv/run_{t}/predictions.csv") if name == "BRSET" \
                    else ("data/splits/mbrset_test_published.csv", f"C:/data/mccv/run_{t}/mbrset_external/predictions.csv")
                d = load(*tf)
                if level == "patient": v = pat(v); d = pat(d)
                thr = np.quantile(v.prob[v.g == 0], 0.90)
                for k in range(5):
                    s = d[d.g == k]; hits[k][0] += int((s.prob > thr).sum()); hits[k][1] += len(s)
                y = (d.g >= 1).astype(int); aucs.append(roc_auc_score(y, d.prob))
                obs = np.array([(d.g == k).mean() for k in range(5)])
                w = np.array([MIX[k] / obs[k] for k in d.g]); aucw.append(roc_auc_score(y, d.prob, sample_weight=w))
            print(f"\n== {name}, {level} level, validation cut-off, pooled over 10 runs ==")
            print(f"AUROC any DR: normal {np.mean(aucs):.3f} ({min(aucs):.3f}-{max(aucs):.3f}); realistic mix {np.mean(aucw):.3f} ({min(aucw):.3f}-{max(aucw):.3f})")
            for k in range(5):
                x, n = hits[k]; lo, hi = beta.ppf(0.025, x + .5, n - x + .5), beta.ppf(0.975, x + .5, n - x + .5)
                print(f" grade {k}: {'flagged' if k == 0 else 'caught'} {x}/{n} = {x/n:.3f} (95% CI {lo:.3f}-{hi:.3f})")
            out[(name, level)] = hits
    rng = np.random.default_rng(0)
    q = lambda a: np.percentile(a, [2.5, 50, 97.5])
    for (name, level), rate in out.items():
        tps, refs, npvr, ppv, lrp, lrn = [], [], [], [], [], []
        for _ in range(20000):
            s = {k: rng.beta(rate[k][0] + .5, rate[k][1] - rate[k][0] + .5) for k in range(5)}
            n = rng.multinomial(100, MIX); c = [rng.binomial(n[k], s[k]) for k in range(5)]
            tp = sum(c[1:]); fp = c[0]; fn = n[1:].sum() - tp; tn = n[0] - fp
            tps.append(tp); refs.append(sum(c[2:]) / max(1, n[2:].sum()))
            if tn + fn: npvr.append(fn / (fn + tn))
            if tp + fp: ppv.append(tp / (tp + fp))
            se = sum(MIX[k] * s[k] for k in range(1, 5)) / MIX[1:].sum(); sp = 1 - s[0]
            lrp.append(se / (1 - sp)); lrn.append((1 - se) / sp)
        print(f"\n[{name} {level}] 100-patient clinic, 20,000 sims (2.5/50/97.5 pct):")
        print("  sick caught of ~46:", np.round(q(tps), 1)); print("  share referable caught:", np.round(q(refs), 2))
        print("  P(DR | flagged):", np.round(q(ppv), 2), " P(DR | cleared):", np.round(q(npvr), 2), " pre-test 0.46")
        print("  LR+:", np.round(q(lrp), 2), " LR-:", np.round(q(lrn), 3))
if __name__ == "__main__": main()
