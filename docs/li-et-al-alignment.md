# Li et al. 2026 alignment notes

**Paper:** Li LY et al. Comparison of foundation models and transfer learning strategies for diabetic retinopathy classification. medRxiv 2026.04.17.26351092 (preprint, not peer-reviewed as of 2026-09-02).

**Code:** https://github.com/hulmanlab/brset_mlcp (cloned to `.reference/brset_mlcp/`).

This document locks what we copy (plumbing) versus what we add (fairness).

---

## What Li et al. already did

| Item | Their choice |
| --- | --- |
| Datasets | BRSET (clinic), mBRSET (Phelcom Eyer handheld) |
| Models | DINOv3 ViT-L, RETFound, VisionFM (+ RETFound-DINOv2 variants) |
| Exp 1 | Fine-tune on BRSET |
| Exp 2 | External validation on mBRSET (no retrain) |
| Exp 3 | Fine-tune BRSET-trained model on mBRSET |
| Image size | 224×224 |
| Splits | Patient-level CSVs in `data/*_nooverlap.csv` |
| Metrics | AUROC, Brier, ECE, calibration curves, DCA, bootstrap CIs (1000 samples) |
| Key result | AUROC 0.90–0.98 on BRSET → 0.70–0.85 on mBRSET; partial recovery after Exp 3 |

**Not done:** Subgroup/fairness analysis; Canon vs Nikon control; separation of camera vs population confound.

---

## Split files to reuse

When PhysioNet data arrive, copy or symlink these from brset_mlcp (or regenerate with same patient IDs):

| File | Purpose |
| --- | --- |
| `train_brset_nooverlap.csv` | BRSET training |
| `val_brset_nooverlap.csv` | BRSET validation |
| `test_brset_nooverlap.csv` | BRSET test |
| `test_mbrset_nooverlap.csv` | mBRSET external test (Exp 2) |
| `train_mbrset_nooverlap.csv` | mBRSET train (Exp 3 only) |

Columns include: `image_id`, `patient_id`, `camera`, `patient_age`, `patient_sex`, `DR_ICDR`, `diabetes`, etc.

**Label column:** `DR_ICDR` (0 = normal; 1–4 = DR). Binary mapping in templates:

```python
# Normal if ICDR == 0 else Diabetic Retinopathy
```

3-class mapping: 0 / 1–3 / 4.

---

## Training hyperparameters (from `template_2class_DR.py`)

| Parameter | Value |
| --- | --- |
| `SHAPE` | (224, 224) |
| `BATCH_SIZE` | 16 |
| `NUM_WORKERS` | 4 |
| `num_epochs` | 50 |
| `learning_rate` | 1e-5 |
| `OPTIMIZER` | Adam |
| `HIDDEN` | [128] (MLP head) |
| `TEST_SIZE` | 0.3 (when generating splits; published splits override) |

**Backbone modes:**
- `fine_tune`: full model fine-tuning
- `eval`: freeze backbone, train head only

**CLI example (their repo):**
```bash
python template_2class_DR.py -b dinov3_large -bm fine_tune
python template_3class_DR_mBRSET_EXEVAL.py -b retfound -bm fine_tune  # Exp 2
```

---

## Model weight paths (their layout)

Place under `src/Weights/` in their repo or set paths in our `configs/brset_mbrset.yaml`:

| Backbone | Weight file |
| --- | --- |
| `retfound` | `RETFound_cfp_weights.pth` |
| `dinov3_large` | `dinov3_vitl16_pretrain_lvd1689m-8aa4cbdd.pth` |
| `visionfm` | `VFM_Fundus_weights.pth` |

---

## Normalization

Their templates default to **ImageNet** mean/std (`None` → no custom transform mean in snippet; ImageNet used when specified). RETFound repo may use dataset-specific stats for BRSET. For comparability with Li et al., start with ImageNet normalization; sensitivity analysis with BRSET-specific stats optional.

Dataset-specific BRSET stats (commented in template):
```
mean = [0.5896, 0.2989, 0.1108]
std  = [0.2854, 0.1591, 0.0701]
```

---

## Our pipeline mapping

| Li et al. | Our config / module |
| --- | --- |
| Exp 1 | `configs/brset_mbrset.yaml` → `experiment: exp1` |
| Exp 2 | `experiment: exp2` |
| Exp 3 | `experiment: exp3` |
| Splits | `data.splits_dir` pointing to brset_mlcp CSVs |
| Evaluation | `src/evaluate.py` (AUROC) + `src/subgroups.py` + `src/bootstrap.py` |
| Calibration | Future: port `evaluation/calibration_*.R` if needed for thesis parity |

---

## Sanity checks after data download

1. Row counts match brset_mlcp split CSVs.
2. Overall AUROC on BRSET test within ~0.02 of Li et al. tables for same backbone/mode.
3. mBRSET external AUROC in 0.70–0.85 range before claiming new findings.
4. Then run subgroup module (our contribution).

---

## Dependencies (their `requirements.txt`)

Python 3.12.5, PyTorch 2.5.0, scikit-learn 1.7.1, torchmetrics 1.8.1. Our `requirements.txt` targets compatible versions for local RTX 4060 (8 GB VRAM).
