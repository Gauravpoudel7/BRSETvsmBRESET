# Discussion: limitations and interpretation

*Draft — expand with actual results later.*

## Confounding between camera and population

BRSET and mBRSET differ simultaneously in camera hardware, geographic region, screening setting, diabetes prevalence, DR prevalence, and grading protocol. A performance drop on mBRSET therefore cannot be attributed to the handheld camera alone. We address this in three ways: (1) restricting BRSET to diabetic patients for training; (2) reporting within-BRSET Canon versus Nikon comparisons as a camera-only upper bound; (3) stating explicitly in all cross-dataset claims that results reflect domain shift, not isolated device effects.

Li et al. (2026) raised the same limitation; our camera control analysis is the main methodological extension on that point.

## Fairness versus overall accuracy

Subgroup gaps may widen, narrow, or remain stable when models move from clinic to handheld images. If gaps widen, deployment without device-specific adaptation risks systematically missing referable disease in already disadvantaged groups (older, less educated, uninsured patients in Bahia). If gaps narrow, overall AUROC loss might still hide compensating errors—we report both overall and subgroup metrics.

Fernandes et al. (2025) established baseline fairness gaps on mBRSET alone; our contribution is whether **cross-domain transfer** changes those gaps relative to clinic-domain performance.

## Underpowered subgroups

The insured subgroup (~8% of mBRSET) is too small for precise inference. We report point estimates and wide bootstrap intervals and label these analyses exploratory. Mean age ~61 years limits the young subgroup similarly.

## Missing race and ethnicity

mBRSET v1.0 does not include race/ethnicity labels despite Bahia's diverse population. Pigmentation-related bias documented by Burlina et al. cannot be tested here; this is a stated limitation, not a silent omission.

## Product implications

Handheld screening vendors in the literature consistently fine-tune on device-specific data (Malerbi et al., Penha et al.). Li et al. and our planned results quantify the cost of skipping that step. If subgroup gaps are large, product decisions may need both device fine-tuning **and** fairness monitoring stratified by accessible demographic fields.

## Future work

- Pairwise same-patient dual-camera capture (if such data become available)
- Race/ethnicity labels in future mBRSET releases
- Calibration-aware fairness metrics
- Embedding-based fast screening using Restrepo et al. (2026) resources as a secondary analysis path
