"""Cohort plan from the patient spreadsheets only (no images, no GPU).
Patient-level (worst eye) counts per ICDR grade, any-DR by diabetes duration,
and the precision (95% Wilson half-width) each test design can give per grade
and for clinic-weighted (54/30/10/5/1) sensitivity."""
import numpy as np, pandas as pd
B = r"C:\data\brset_mbrset\brazilian-ophthalmological\1.0.2\label_brset.csv"
M = r"C:\data\brset_mbrset\mbrset\1.0\labels_mbrset.csv"
def wil(x, n, z=1.96):
    p = x / n; d = 1 + z*z/n; return 100 * z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
hw = lambda n, p=.5: wil(round(n*p), n)
W = np.array([30, 10, 5, 1]) / 46
wh = lambda ns, p=.5: 196*np.sqrt(sum(W**2*p*(1-p)/np.array(ns)))
def worst(d):
    d = d.dropna(subset=["DR_ICDR"])
    return d.groupby("patient_id").agg(g=("DR_ICDR", "max"), dur=("diabetes_time_y", "first"))
def main():
    b = pd.read_csv(B); m = pd.read_csv(M).rename(columns={"patient": "patient_id", "final_icdr": "DR_ICDR", "dm_time": "diabetes_time_y"})
    for nm, d in [("BRSET diabetic", b[b.diabetes == "yes"]), ("BRSET labelled non-diabetic", b[b.diabetes != "yes"]), ("mBRSET all", m)]:
        w = worst(d); print(f"\n{nm}: {len(d)} images, {len(w)} patients; patients per grade {w.g.value_counts().sort_index().astype(int).to_dict()}")
        dur = pd.to_numeric(w.dur, errors="coerce")
        if dur.notna().any():
            bins = pd.cut(dur, [-1, 9.999, 19.999, 200], labels=["<10y", "10-19y", "20y+"])
            print(pd.crosstab(bins, w.g.astype(int)))
    print("\nPer-grade 95% half-width (%), grades 1-4, at sensitivity 0.5 / 0.8:")
    designs = {"mBRSET published test (258 pts)": [23, 37, 7, 14], "mBRSET all (1,287 pts)": [96, 200, 28, 71],
               "BRSET 5-fold CV (all 1,346)": [52, 162, 33, 154], "BRSET one 60/20/20 test": [10, 30, 8, 32]}
    for nm, ns in designs.items():
        print(f" {nm}: {[round(hw(n)) for n in ns]} / {[round(hw(n,.8)) for n in ns]}; clinic-weighted +-{wh(ns):.1f}")
    for t in (10, 5): print(f" n per grade for +-{t}%: {next(n for n in range(5,3000) if hw(n,.8)<=t)} (p=.8), {next(n for n in range(5,3000) if hw(n)<=t)} (p=.5)")
    for t in (7.5, 5): print(f" mild patients for clinic-weighted +-{t}% (other grades = mBRSET all): {next(n for n in range(10,3000) if wh([n,200,28,71])<=t)}")
if __name__ == "__main__": main()
