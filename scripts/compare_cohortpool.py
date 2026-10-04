"""Patient-level comparison of Test 1 (real), Test 2 (rf), Test 3 (rfw) on cohort+pool runs.
Patient label = worst-eye ICDR >= 1; patient score = max photo probability.
BRSET: 5 folds pooled out-of-fold (175 patients). mBRSET: each fold model on all 324 patients; ensemble = mean prob of 5 fold models.
Cut-offs chosen on each fold's validation patients only: (a) Youden, (b) specificity >= 0.80.
"""
import pandas as pd, numpy as np, json, sys
from sklearn.metrics import roc_auc_score, roc_curve
from scipy.stats import binomtest
R = sys.argv[1] if len(sys.argv) > 1 else "."
TESTS = {"T1 baseline": "real", "T2 RETFound recipe": "rf", "T3 recipe+weights": "rfw"}
B = 2000; rng = np.random.default_rng(3000); SPEC = 0.80
ext = pd.read_csv(f"{R}/ext_mbrset_steep.csv")

def pat(p, s, pid, g):
    d = pd.DataFrame({"pid": s[pid].values, "prob": p.prob.values, "grade": s[g].values})
    a = d.groupby("pid").agg(prob=("prob", "max"), grade=("grade", "max")).reset_index()
    a["y"] = (a.grade >= 1).astype(int); return a

def cutoffs(v):
    fpr, tpr, th = roc_curve(v.y, v.prob)
    you = th[np.argmax(tpr - fpr)]
    ok = th[(1 - fpr) >= SPEC]; spec = ok.min() if len(ok) else th[0]
    return float(you), float(spec)

data = {}
for name, t in TESTS.items():
    brs, mbr, cuts, foldauc = [], [], [], []
    for f in range(5):
        r = f"{R}/run_{t}_f{f}"
        te = pat(pd.read_csv(f"{r}/predictions.csv"), pd.read_csv(f"{R}/splits/test_real_f{f}.csv"), "patient_id", "DR_ICDR")
        va = pat(pd.read_csv(f"{r}/val_predictions.csv"), pd.read_csv(f"{R}/splits/val_real_f{f}.csv"), "patient_id", "DR_ICDR")
        ex = pat(pd.read_csv(f"{r}/ext/predictions.csv"), ext, "patient", "final_icdr")
        you, sp = cutoffs(va); cuts.append((you, sp))
        te["fold"] = f; te["you"] = te.prob >= you; te["sp80"] = te.prob >= sp
        ex["you"] = ex.prob >= you; ex["sp80"] = ex.prob >= sp; ex["fold"] = f
        brs.append(te); mbr.append(ex)
        foldauc.append((roc_auc_score(te.y, te.prob) if te.y.nunique() > 1 else np.nan, roc_auc_score(ex.y, ex.prob), roc_auc_score(va.y, va.prob)))
    brs = pd.concat(brs).set_index("pid").sort_index()
    m = pd.concat(mbr); ens = m.groupby("pid").agg(prob=("prob", "mean"), grade=("grade", "first"), y=("y", "first"))
    # ensemble decision = majority vote of the 5 fold models at their own validation cut-offs
    ens["you"] = m.groupby("pid")["you"].mean() >= 0.5; ens["sp80"] = m.groupby("pid")["sp80"].mean() >= 0.5
    data[name] = dict(brset=brs, mbr_folds=m, mbr_ens=ens.sort_index(), cuts=cuts, foldauc=foldauc)

def boot_auc(y, scores, idx_sets):
    out = []
    for idx in idx_sets:
        yy = y[idx]
        if yy.min() == yy.max(): continue
        out.append([roc_auc_score(yy, s[idx]) for s in scores])
    return np.array(out)

def sens_spec(df, col):
    s = df[df.y == 1][col].mean(); c = 1 - df[df.y == 0][col].mean(); return s, c

lines = []; P = lines.append
res = {}
for setname in ["BRSET (pooled 5 folds, 175 patients)", "mBRSET ensemble (324 patients)"]:
    key = "brset" if setname.startswith("BRSET") else "mbr_ens"
    dfs = {n: data[n][key] for n in TESTS}
    base = dfs["T1 baseline"]; y = base.y.values; n = len(y)
    for nm in TESTS: assert (dfs[nm].index == base.index).all() and (dfs[nm].y.values == y).all()
    scores = [dfs[nm].prob.values for nm in TESTS]
    idx_sets = [rng.integers(0, n, n) for _ in range(B)]
    bs = boot_auc(y, scores, idx_sets)
    P(f"\n=== {setname}: {int(y.sum())} with DR, {int((1-y).sum())} without ===")
    P("Grades (patients): " + str(base.grade.value_counts().sort_index().to_dict()))
    names = list(TESTS)
    for i, nm in enumerate(names):
        a = roc_auc_score(y, scores[i]); lo, hi = np.percentile(bs[:, i], [2.5, 97.5])
        P(f"{nm:22s} patient AUROC {a:.3f} (95% CI {lo:.3f}-{hi:.3f})")
        res[(setname, nm, "auc")] = (a, lo, hi)
    for i, j in [(1, 0), (2, 0), (2, 1)]:
        d = bs[:, i] - bs[:, j]; obs = roc_auc_score(y, scores[i]) - roc_auc_score(y, scores[j])
        p = min(1.0, 2 * min((d <= 0).mean(), (d >= 0).mean()))
        lo, hi = np.percentile(d, [2.5, 97.5])
        P(f"  {names[i]} minus {names[j]}: {obs:+.3f} (95% CI {lo:+.3f} to {hi:+.3f}), bootstrap p={p:.3f}")
    for col, lab in [("you", "validation Youden cut-off"), ("sp80", "validation cut-off for 80% specificity")]:
        P(f" -- At {lab} --")
        for nm in names:
            s, c = sens_spec(dfs[nm], col)
            pg = dfs[nm][dfs[nm].y == 1].groupby("grade")[col].mean()
            P(f"  {nm:22s} sensitivity {s:.2f}, specificity {c:.2f}; catch by grade " + ", ".join(f"g{int(g)} {v:.2f}" for g, v in pg.items()))
        for i, j in [(1, 0), (2, 0), (2, 1)]:
            for grp, gl in [(1, "sick"), (0, "healthy")]:
                a = dfs[names[i]][col][dfs[names[i]].y == grp].values; b = dfs[names[j]][col][dfs[names[j]].y == grp].values
                n10 = int((a & ~b).sum()); n01 = int((~a & b).sum())
                p = binomtest(n10, n10 + n01, 0.5).pvalue if n10 + n01 else 1.0
                P(f"  McNemar {names[i]} vs {names[j]} on {gl} patients: flagged only by first {n10}, only by second {n01}, p={p:.3f}")

P("\n=== Per-fold patient AUROC (BRSET test / mBRSET / validation) ===")
for nm in TESTS:
    fa = np.array(data[nm]["foldauc"])
    P(f"{nm:22s} " + " | ".join(f"f{k}: {a:.3f}/{b:.3f}/{c:.3f}" for k, (a, b, c) in enumerate(fa)) + f" | mean {np.nanmean(fa[:,0]):.3f}/{fa[:,1].mean():.3f}")
P("\n=== mBRSET per-fold-model thresholded results (mean of 5 models) ===")
for nm in TESTS:
    m = data[nm]["mbr_folds"]
    for col in ["you", "sp80"]:
        ss = [sens_spec(g, col) for _, g in m.groupby("fold")]
        P(f"{nm:22s} {col}: sensitivity {np.mean([a for a,_ in ss]):.2f}, specificity {np.mean([b for _,b in ss]):.2f}")
P("\nValidation cut-offs (Youden, spec80) per fold:")
for nm in TESTS: P(f"{nm:22s} " + "; ".join(f"{a:.3f}, {b:.3f}" for a, b in data[nm]["cuts"]))
txt = "\n".join(lines); print(txt); open(f"{R}/results_comparison.txt", "w").write(txt)
