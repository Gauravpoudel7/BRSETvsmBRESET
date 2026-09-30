# Protocol addendum 1: extra (secondary) analyses

**Date written:** 2026-09-28
**Written before any BRSET or mBRSET result was seen.** Data download had only just started; no model had been trained or evaluated on either dataset.

**Relation to the locked protocol:** This file does **not** change `study-protocol.md`. The locked protocol, its primary question, its primary endpoint (subgroup AUROC and change in gap under Exp 2) and its analysis rules stay exactly as written on 2026-09-02. Everything below is an **extra, secondary** analysis. If anything here seems to conflict with the locked protocol, the locked protocol wins.

**Order:** These analyses run only **after** the locked protocol's analysis order (section 9, steps 1 to 5) is finished. Results from these extras must be reported in a clearly labelled "Secondary analyses (Addendum 1)" section and must not be used to change how the primary results are reported.

---

## A1. Who does the model send back? (fairness of abstention / referral)

### Question
When the model is allowed to say "not sure" (abstain, so the patient is sent for a retake or a human grader), does the abstention rate differ across patient subgroups, and does switching from clinic to handheld images make that difference bigger?

### Why
Confidence-based filtering is being proposed for handheld screening on mBRSET (for example the SureSight preprint, arXiv 2607.03643, July 2026), but its effect on different patient groups has not been reported. If some groups are sent back much more often, they carry extra cost and travel, even when accuracy on answered cases looks good.

### Data and models
- No new training. Use the exact models from Exp 1 (BRSET) and their Exp 2 evaluation (mBRSET test split).
- Same subgroups as protocol section 6 (age, sex on both datasets; education, insurance on mBRSET only). Same underpowered labels apply.

### Method
1. For each test image, take the model's predicted probability of DR, `p`.
2. Confidence score: `c = max(p, 1 - p)`.
3. Abstention rule, fixed in advance: abstain if `c` is below a threshold chosen so that the model abstains on **20%** of the **BRSET validation** set. The threshold is set once, on BRSET validation, and then used unchanged on BRSET test and mBRSET test.
4. Also report a coverage curve (coverage from 100% down to 50% in 5% steps), per subgroup.
5. Patient-level decision (secondary): a patient is "sent back" if any of their images is abstained on.

### Outcomes
- **A1 primary:** abstention rate per subgroup and the **abstention gap** (highest minus lowest subgroup rate) on BRSET test and on mBRSET test.
- **Change in abstention gap** (mBRSET minus BRSET) for age and sex.
- Accuracy on answered cases per subgroup: AUROC, sensitivity, specificity.
- Share of true DR cases that were abstained on, per subgroup (missed-by-deferral).
- 95% CIs from 1,000 patient-level bootstrap resamples, as in protocol section 7.

### What counts as a finding
A difference is only called a finding if its 95% CI excludes zero. Otherwise it is reported as "no clear difference detected", together with the CI width.

---

## A2. Does fixing the camera gap also fix fairness? (fairness of adaptation)

### Question
When the model is adapted to handheld images, do subgroup gaps shrink along with the overall AUROC gain, or does the average improve while some groups stay behind? And how many labelled handheld images are needed before the subgroup gaps close?

This extends secondary question 2 of the locked protocol (Exp 3).

### Splits
- Use the published Li et al. / `brset_mlcp` split files: `train_mbrset_nooverlap.csv` as the **adaptation pool** and `test_mbrset_nooverlap.csv` as the **only** mBRSET test set.
- The adaptation pool is split once, at patient level, into adaptation-train (85%) and adaptation-val (15%), seed 42. This split is saved to a file and reused for every method.
- **No image or patient from the mBRSET test split is ever used for training, tuning, threshold setting or early stopping.**
- Every A2 method is scored on the same mBRSET test split as Exp 2, so results are directly comparable.

### Methods compared (all start from the Exp 1 model)
- **M0, no adaptation:** the Exp 2 result (reference).
- **M1, supervised fine-tuning** on labelled handheld images (this is Exp 3). Training settings as in protocol section 5, early stopping on adaptation-val AUROC.
- **M2, image harmonisation:** a fixed, training-free colour and brightness normalisation that maps handheld images towards BRSET image statistics (for example histogram matching to the BRSET training set mean histogram), applied before the frozen Exp 1 model. No labels used.
- **M3, unsupervised test-time adaptation:** update only the normalisation layers' statistics and affine parameters on unlabelled mBRSET adaptation-train images (entropy-minimisation style, as in TENT), then freeze and evaluate. No labels used.

M2 and M3 are optional if time runs short; M1 is the priority.

### Label-budget curve (M1 only)
- Fine-tune with **100, 250, 500 and 1,000** labelled handheld images, plus the full adaptation-train pool.
- Images are sampled by patient (all images of a sampled patient are included), stratified by DR label, seed 42. Smaller budgets are subsets of larger ones.
- If time allows, repeat each budget with 3 seeds (42, 43, 44) and report mean and spread.

### Outcomes
- Overall AUROC on mBRSET test for every method and budget.
- Subgroup AUROC, gap and equity-scaled AUC for every method and budget.
- **Gap change versus M0** for each method (does the fix close the gap?).
- Label-budget curves for overall AUROC and for each subgroup gap.
- Calibration (ECE) per subgroup, as a secondary outcome.
- 95% patient-level bootstrap CIs, 1,000 resamples.

### What counts as a finding
Same rule as A1: a change is only called a finding if its 95% CI excludes zero.

---

## A3. Is the model's confidence equally honest for everyone? (subgroup calibration)

Small extra, no new training. For the Exp 1 and Exp 2 models, report ECE and calibration slope/intercept **per subgroup** on BRSET test and mBRSET test, with bootstrap CIs. The protocol already lists overall calibration as secondary; this only breaks it down by subgroup.

---

## Limitations specific to this addendum
1. All limitations in protocol section 10 still apply.
2. The abstention threshold (A1) is one fixed choice; other thresholds could give different gaps. The coverage curve is reported to show this.
3. Subgroups that are already underpowered (insured, age < 50) become even smaller after abstention or budget sampling; results for them are exploratory only.
4. M2 and M3 are simple, standard versions of each method family, not the best possible version.
5. Many comparisons are made. No correction for multiple testing is planned, so A1 to A3 results are treated as secondary and hypothesis-generating.

---

## Small code additions needed later (additive only)
These are **new** additions. Existing functions, configs, outputs and tests must keep working unchanged.
- Save per-image predictions for every evaluation run to a new file, for example `results/<run>/predictions.csv` (image id, patient id, true label, predicted probability, subgroup columns). The existing outputs in protocol section 11 stay as they are.
- A new, separate analysis script for A1 and A3 that reads `predictions.csv` (for example `scripts/analyse_abstention.py`).
- New config files for A2 (for example `configs/adapt_m1_budget100.yaml`), leaving `configs/brset_mbrset.yaml` untouched.
- A new script to create and save the adaptation-train / adaptation-val split.
- Keep saved prediction files local and out of git and out of any AI tool, because they contain patient-level rows covered by the PhysioNet data use agreement.
