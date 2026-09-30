# Study protocol: fairness of cross-camera DR model performance

**Status:** Locked before data access (2026-09-02). Do not change analysis rules after seeing results.

**Primary contribution:** When an off-the-shelf retinal foundation model moves from clinic-grade to handheld fundus images, does the accuracy loss fall unevenly across patient subgroups?

**Reference overlap:** Li et al. 2026 (medRxiv) reports the overall cross-camera drop on BRSET/mBRSET. This study adds subgroup and fairness analysis plus a within-BRSET camera control. Fernandes et al. 2025 reports fairness on mBRSET only (no cross-camera, no foundation models).

---

## 1. Research questions

### Primary
When a foundation model is trained on clinic-grade fundus images (BRSET) and evaluated on handheld images (mBRSET) without retraining, does the performance drop differ across age, sex, education, and insurance subgroups?

### Secondary
1. How much of the BRSET-to-mBRSET drop is plausibly camera-related versus population-related? (Canon vs Nikon within BRSET as a camera-only control.)
2. Does fine-tuning on mBRSET (optional Experiment 3) reduce subgroup gaps as well as overall AUROC?
3. Do mild versus moderate+ referable cases show different drop patterns? (Screening-relevant severity breakdown.)

---

## 2. Datasets

| Dataset | Role | Camera | N (approx.) | DR prevalence (approx.) |
| --- | --- | --- | --- | --- |
| BRSET | Training (+ internal validation/test) | Canon CR2 (65%), Nikon NF5050 (35%) | 16,266 images | ~7% any DR |
| mBRSET | External test (primary); optional fine-tune | Phelcom Eyer handheld | 5,164 images | ~23% any DR |

**Confounds (state upfront):** Datasets are not paired. They differ in region, screening setting, diabetes rate (16% vs 97%), DR prevalence, and grading protocol. Cross-dataset comparisons are **domain shift**, not pure camera shift.

**Mitigations:**
- Primary training set: BRSET restricted to **diabetic patients only** (reduces diabetes-rate confound).
- Optional sensitivity: reweight or match DR prevalence when comparing subgroup gaps.
- Camera control: Canon vs Nikon on **same patients, same grader** within BRSET.

**Stand-in phase (plumbing only):** APTOS 2019 (train) and MESSIDOR-2 (external test). Results from stand-in runs are **not** thesis findings.

---

## 3. Task definitions

### Primary task (binary DR)
- **Label:** Normal (ICDR 0) vs any retinopathy (ICDR 1–4). Matches Li et al. binary setup.
- **Image input:** 224×224 RGB, foundation-model default normalization unless RETFound-specific weights require dataset statistics (follow Li et al. / RETFound repo for BRSET runs).

### Secondary task (3-class DR)
- Normal (0) vs non-proliferative (1–3) vs proliferative (4). Report if time allows; not primary endpoint.

### Severity breakdown (exploratory)
- Mild referable (ICDR 1) vs moderate+ (ICDR 2–4) sensitivity/specificity separately, following MAILOR and Poyrazer patterns.

---

## 4. Models

Minimum two backbones (do not test only RETFound):

| Model | Type | Rationale |
| --- | --- | --- |
| RETFound (ViT-L/16) | Eye-specific foundation | Li et al. baseline; product-relevant |
| DINOv3 ViT-L/16 | General-purpose vision | Beat eye models on cross-domain in Li et al. |

Optional if time: VisionFM.

**Fine-tuning modes (match Li et al. for comparability):**
- **Head only (`eval` backbone):** Freeze encoder, train classification head.
- **Full fine-tune (`fine_tune`):** Unfreeze encoder + head. Primary for Experiment 1.

Default for main experiments: **full fine-tune on BRSET**, evaluate frozen weights on mBRSET (Experiment 2).

---

## 5. Splits and experiments

Align with Li et al. / `hulmanlab/brset_mlcp` (see `docs/li-et-al-alignment.md`):

| Experiment | Train | Val | Test | Notes |
| --- | --- | --- | --- | --- |
| **Exp 1** | BRSET train split | BRSET val | BRSET test | Patient-level, no overlap across splits |
| **Exp 2** | (model from Exp 1) | — | mBRSET test | No retraining; main external validation |
| **Exp 3** (optional) | Exp 1 model → fine-tune on mBRSET train | mBRSET val | mBRSET test | Only if time allows |

**Split policy:** Use published `*_nooverlap.csv` splits from brset_mlcp when running on real data. Patient-level assignment; no patient in more than one split.

**Image size:** 224×224.

**Training defaults (starting point, tune only if OOM):**
- Batch size: 16 (reduce to 8 on 8 GB GPU if needed)
- Optimizer: Adam, lr 1e-5
- Epochs: up to 50 with early stopping on val AUROC
- Loss: cross-entropy (Li et al. also reports focal loss variants)

---

## 6. Subgroup definitions

### Both BRSET and mBRSET
| Attribute | Subgroups | Rule |
| --- | --- | --- |
| Age | Young vs old | Median split **or** fixed cutoff at 50 years (report both if feasible; pre-register median as primary) |
| Sex | Female vs male | Binary from metadata |

### mBRSET only
| Attribute | Subgroups | Rule |
| --- | --- | --- |
| Education | Literate vs illiterate | Per mBRSET coding |
| Insurance | Insured vs uninsured | Per mBRSET coding |

### Underpowered (exploratory only)
- **Insured:** ~100 patients (~8% of mBRSET). Report point estimates + wide CIs; label "exploratory."
- **Age < 50:** Small; same treatment.

### Not available
- **Race/ethnicity:** Not in mBRSET v1.0. Limitation section must state this explicitly.

### Stand-in pipeline
- Use age/sex from metadata where present; inject synthetic `subgroup_demo` column for code testing.

---

## 7. Metrics

### Discrimination (overall and per subgroup)
- **AUROC** (primary)
- Sensitivity, specificity at clinically motivated threshold(s)
- Optional: AUPRC if class imbalance distorts interpretation

### Fairness
- **Gap:** max subgroup AUROC − min subgroup AUROC (per attribute)
- **Equity-scaled AUC** (Shi et al. 2025 fair adaptive scaling framework) as headline fairness metric where applicable
- **Change in gap:** (subgroup gap on mBRSET) − (subgroup gap on BRSET test) for age/sex

### Uncertainty
- **Bootstrap 95% CIs:** 1,000 resamples at patient level (match Li et al.)
- Report CIs for AUROC, gaps, and difference in AUROC between domains

### Calibration (secondary, Li et al. parity)
- Expected calibration error (ECE)
- Calibration intercept and slope
- Not the thesis headline but useful for comparison

---

## 8. Camera control (within BRSET)

Train/evaluate on BRSET with camera as stratification variable:
- Compare AUROC and subgroup gaps: **Canon CR2 vs Nikon NF5050**
- Same patients can contribute both eyes; splits remain patient-level
- Interpret as upper bound on pure camera effect without population shift

---

## 9. Analysis order (when data arrive)

1. Verify metadata columns against this protocol.
2. Run Exp 2 (train BRSET → test mBRSET) for each model; compare overall AUROC to Li et al. (sanity check).
3. Run subgroup breakdowns on mBRSET (main contribution).
4. Run change-in-gap analysis for age/sex (BRSET test vs mBRSET).
5. Run Canon vs Nikon control on BRSET.
6. Optional: Exp 3, 3-class task, severity breakdown.
7. Optional: embedding-based analysis using PhysioNet embedding resource as speed backup.

---

## 10. Limitations (pre-registered)

1. BRSET and mBRSET are not paired; cross-dataset results confound camera, population, disease prevalence, and grading.
2. Education and insurance exist only in mBRSET; cannot compare education/insurance gaps across domains.
3. Insured and young subgroups are underpowered.
4. No race/ethnicity labels in mBRSET v1.0.
5. Li et al. may publish peer-reviewed updates; cite version and date.
6. Stand-in experiments (APTOS/MESSIDOR) validate code only.

---

## 11. Outputs

Each experiment run produces:
- `results/overall_metrics.json`
- `results/subgroup_metrics.csv`
- `results/bootstrap_gaps.json`
- Training log with GPU memory, batch size, seconds per epoch

---

## 12. Software

- Pipeline: `scripts/run_experiment.py` with YAML configs (`configs/standin.yaml`, `configs/brset_mbrset.yaml`)
- Random seed: 42 (fixed in config)
- Version log: `requirements.txt`
