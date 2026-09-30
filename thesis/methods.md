# Methods

*Draft chapter — aligned with `study-protocol.md`. Do not change analysis rules after seeing results.*

## Study design

We conduct a retrospective imaging study using two public Brazilian fundus datasets: BRSET (clinic-grade cameras) and mBRSET (Phelcom Eyer handheld). The primary experiment mirrors Li et al. (2026) Experiment 2: fine-tune foundation models on BRSET, then evaluate on mBRSET without retraining. The novel layer is subgroup and fairness analysis across demographic variables available in metadata.

An optional third experiment fine-tunes BRSET-trained models on mBRSET if time permits. A within-BRSET Canon versus Nikon comparison estimates performance change attributable to camera type alone, holding patient pool and grader constant.

## Datasets

**BRSET** (Nakayama et al., 2024) contains 16,266 fundus images from 8,524 patients in São Paulo outpatient clinics. Cameras are Canon CR2 (65.1%) and Nikon NF5050 (34.9%). DR labels use ICDR grades from a single retina specialist. Approximately 16% of patients have diabetes; DR prevalence is roughly 7%.

**mBRSET** (Wu et al., 2025) contains 5,164 images from 1,291 patients captured during a community diabetes campaign in Itabuna, Bahia, using the Phelcom Eyer handheld device. Two ophthalmologists graded DR independently. Approximately 97% of patients have diabetes; DR prevalence is roughly 23%. Education and insurance status are recorded; race/ethnicity is not in version 1.0.

The datasets are not paired: no patient appears with both cameras. Cross-dataset evaluation therefore reflects combined domain shift (camera, population, disease burden, grading protocol).

## Task and labels

**Primary endpoint:** binary classification—normal (ICDR 0) versus any retinopathy (ICDR 1–4).

**Secondary:** three-class DR (normal / non-proliferative / proliferative); severity-stratified sensitivity for mild (ICDR 1) versus moderate+ (ICDR 2–4).

## Models and training

We evaluate at minimum:
- RETFound (ViT-L/16), eye-specific foundation model
- DINOv3 ViT-L/16, general-purpose vision foundation model

Training follows Li et al. (2026) defaults where possible: 224×224 inputs, Adam optimizer, learning rate 1×10⁻⁵, batch size 16, up to 50 epochs with early stopping on validation AUROC. We use patient-level splits from the published `brset_mlcp` repository (`*_nooverlap.csv` files).

Primary training uses all BRSET training images restricted to **diabetic patients** as a confound reduction step. External testing uses the published mBRSET test split without retraining.

Hardware: local NVIDIA GPU (RTX 4060, 8 GB VRAM); batch size reduced if out-of-memory.

## Subgroup definitions

| Variable | Levels | Available in |
| --- | --- | --- |
| Age | Young vs old (median split; sensitivity at 50 years) | BRSET, mBRSET |
| Sex | Female vs male | BRSET, mBRSET |
| Education | Literate vs illiterate | mBRSET only |
| Insurance | Insured vs uninsured | mBRSET only |

Insured (~100 patients) and young subgroups are labelled exploratory due to limited sample size.

## Metrics

**Discrimination:** AUROC (primary), sensitivity, specificity.

**Fairness:** subgroup AUROC; gap = max − min AUROC within attribute; equity-scaled AUC summary (Shi et al., 2025 framework); change-in-gap comparing BRSET test versus mBRSET for age and sex.

**Uncertainty:** patient-level bootstrap (1,000 resamples) for AUROC and gaps, matching Li et al.

**Calibration (secondary):** expected calibration error, calibration intercept and slope—for comparison with Li et al., not primary thesis claim.

## Software and reproducibility

Code: `scripts/run_experiment.py` with YAML configs. Random seed fixed at 42. Dependencies in `requirements.txt`. Results written to JSON/CSV under `results/`.

## Pilot study (pre-PhysioNet, not thesis results)

Before credentialed access to BRSET/mBRSET, we ran a **public-data pilot** to validate the software pipeline:

- **Train:** APTOS 2019 (Kaggle, clinic-style fundus images)
- **External test:** MESSIDOR-2 (different acquisition source/country)
- **Models:** timm ViT baseline, DINOv3 ViT-L/16, RETFound ViT-L/16 (when weights available)

APTOS and MESSIDOR do not provide education or insurance labels, so subgroup fairness modules were tested separately on BRSET/mBRSET **metadata CSVs** from the Li et al. reference splits (no images required). Pilot AUROC values are **not** reported in the Results chapter; they only confirm that training, external evaluation, and bootstrap confidence intervals run correctly on real fundus images.

Full instructions: [docs/pilot-study.md](../docs/pilot-study.md).

## Stand-in validation (synthetic smoke tests)

Synthetic random-image smoke tests (`scripts/prepare_standin_data.py`) were used for initial debugging only.

## Limitations (methods section)

Pre-specified limitations: unpaired datasets; education/insurance only on mBRSET; no race/ethnicity labels; underpowered insured subgroup; Li et al. preprint may update; cross-dataset results cannot be interpreted as pure camera effects without within-BRSET camera control.

See `study-protocol.md` for the locked protocol version dated 2026-09-02.
