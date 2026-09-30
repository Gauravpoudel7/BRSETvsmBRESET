# Results

*Placeholders — to be completed upon BRSET/mBRSET data access.*

## Experiment 1: BRSET internal validation

| Model | Fine-tune mode | Test AUROC | 95% CI |
| --- | --- | --- | --- |
| RETFound | Full | TBD | TBD |
| DINOv3 | Full | TBD | TBD |

## Experiment 2: External validation on mBRSET (primary)

| Model | mBRSET AUROC | Δ vs BRSET test | 95% CI |
| --- | --- | --- | --- |
| RETFound | TBD | TBD | TBD |
| DINOv3 | TBD | TBD | TBD |

*Sanity check: compare overall mBRSET AUROC to Li et al. 2026 (expected ~0.70–0.85).*

## Subgroup analysis (main contribution)

### Age

| Model | Subgroup | N | AUROC | Gap |
| --- | --- | --- | --- | --- |
| RETFound | Young | TBD | TBD | TBD |
| RETFound | Old | TBD | TBD | |
| DINOv3 | Young | TBD | TBD | TBD |
| DINOv3 | Old | TBD | TBD | |

### Sex

| Model | Subgroup | N | AUROC | Gap |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

### Education (mBRSET only)

| Model | Subgroup | N | AUROC | Gap |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

### Insurance (mBRSET only, exploratory)

| Model | Subgroup | N | AUROC | Gap |
| --- | --- | --- | --- | --- |
| TBD | Insured | ~100 | TBD | TBD |
| TBD | Uninsured | TBD | TBD | |

## Change-in-gap (BRSET test → mBRSET)

| Attribute | Model | Gap BRSET | Gap mBRSET | Δ gap |
| --- | --- | --- | --- | --- |
| Age | RETFound | TBD | TBD | TBD |
| Sex | RETFound | TBD | TBD | TBD |

## Camera control: Canon vs Nikon (within BRSET)

| Model | Camera | AUROC | Subgroup gap (age) |
| --- | --- | --- | --- |
| RETFound | Canon CR2 | TBD | TBD |
| RETFound | Nikon NF5050 | TBD | TBD |

## Severity breakdown

| Model | Severity | Sensitivity | Specificity |
| --- | --- | --- | --- |
| RETFound | Mild (ICDR 1) | TBD | TBD |
| RETFound | Moderate+ (ICDR 2–4) | TBD | TBD |

## Optional Experiment 3: Fine-tune on mBRSET

*If completed:* TBD

---

**Note:** Stand-in pipeline results (`results/standin/`) are for code validation only and must not appear in this chapter.
