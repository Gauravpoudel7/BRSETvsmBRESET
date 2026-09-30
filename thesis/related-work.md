# Related Work

*Draft chapter — expand before submission. Citations from `literature-review/references.bib`.*

## Diabetic retinopathy screening and the device gap

Diabetic retinopathy (DR) is a leading cause of preventable blindness. Screening programmes photograph the fundus and classify disease severity so referable cases reach treatment before vision loss. In high-resource settings, mydriatic table-top fundus cameras produce standardized images. In low- and middle-income settings and community campaigns, handheld smartphone-attached cameras improve access but change image appearance: field of view, illumination, focus, and artefact profiles differ from clinic-grade systems.

The deployment literature shows that models trained on one device often underperform on another. Wang et al. (2025) meta-analysed regulator-approved DR AI systems and found that fewer than half of studies used genuinely external test data. Onyeze et al. (2025) and Grace et al. (2026) highlight data generalisability as a barrier in LMIC screening. Duggal et al. (2025) invited vendors to test on low-cost cameras in Indian public clinics; specificity ranged from 14% to 96%, showing that published accuracy rarely transfers unchanged.

## Camera and domain generalisation

Cross-camera fundus generalisation has been studied with adaptation methods (CycleGAN, residual adaptation), severity-aware architectures (DRStageNet), and frozen foundation-model probes (Poyrazer et al., 2026). Zhang et al. (2024) and He et al. (2023) report measurable drops when moving between camera types. Duhaim et al. (2026) propose unified evaluation frameworks for cross-domain fundus AI.

For the Brazilian datasets central to this thesis, Li et al. (2026) train RETFound, VisionFM, and DINOv3 on BRSET (clinic Canon/Nikon cameras) and evaluate on mBRSET (Phelcom Eyer handheld) without retraining. AUROC falls from roughly 0.90–0.98 to 0.70–0.85. They report calibration degradation and partial recovery after fine-tuning on mBRSET, but do not analyse patient subgroups or isolate camera effects from population differences. Restrepo et al. (2026) release precomputed embeddings for both datasets, enabling faster downstream analysis but not replacing full-image fairness evaluation.

## Retinal foundation models

RETFound (Zhou et al., 2023), VisionFM (Qiu et al., 2024), FLAIR (Silva-Rodriguez et al., 2025), and general-purpose models such as DINOv3 have become default backbones for fundus tasks. RetBench (Zou et al., 2025) and Xiong et al. (2025) show that no single foundation model wins on every task and domain. Li et al. (2026) found DINOv3 competitive or superior to eye-specific models on cross-dataset BRSET→mBRSET transfer. Yew et al. (2025) and Bolo et al. (2026) report task-dependent advantages for RETFound versus CNNs.

Fairness implications of medical foundation models remain active: Khan et al. (2023), Jin et al. (2024), and Burlina et al. (2021) document subgroup gaps; Queiroz et al. (2024) show age gaps widen under data-scarce fine-tuning of RETFound on BRSET alone.

## Fairness in DR AI

Fairness research in ophthalmic AI spans pigmentation and anatomy (Burlina et al.), adaptive thresholding (Shi et al., 2025 EyeCLIP), and disentanglement (Fernandes et al., 2025). Fernandes et al. evaluate ConvNeXt V2, DINOv2, and Swin V2 on mBRSET macula images, reporting AUROC gaps by age (up to ~10 points for DINOv2) and mixed effects of disentanglement mitigation. Their work is within-handheld only and does not address cross-camera domain shift or foundation models used in Li et al.

Wu et al. (2025) document that models can predict insurance status from mBRSET fundus images, implying socially loaded shortcuts that may interact with domain shift when models fail on unfamiliar image statistics.

## Handheld and LMIC screening

Phelcom Eyer studies (Malerbi et al., 2022, 2024; Penha et al., 2023) consistently fine-tune on device-specific images rather than deploying borrowed clinic models unchanged. MAILOR (Rogers et al., 2021) shows mild DR is harder than moderate+ disease on handheld systems. Moya-Sanchez et al. (2025) integrate handheld screening into Brazilian public workflows.

Together, these lines justify two claims for the present work: (1) cross-device performance drop on BRSET/mBRSET is established at the aggregate level; (2) whether that drop is equitable across patient groups—and how much is camera versus population—remains open.

## Gap addressed by this thesis

| Prior work | What it shows | What it omits |
| --- | --- | --- |
| Li et al. 2026 | Foundation models drop on mBRSET; calibration matters | Subgroups; camera-only control |
| Fernandes et al. 2025 | Fairness on mBRSET | Cross-camera; RETFound/DINOv3 |
| Queiroz et al. 2024 | Age/sex gaps on BRSET with RETFound | Handheld domain; education/insurance |

This thesis joins the cross-camera experimental design of Li et al. with the subgroup lens of Fernandes et al., and adds within-BRSET Canon versus Nikon analysis to bound camera-only effects.

## Planned figures and tables

**Figures:** (1) Pipeline diagram: train BRSET → test mBRSET with subgroup reporting; (2) Subgroup AUROC gap bar chart; (3) Canon vs Nikon control chart.

**Tables:** (1) BRSET vs mBRSET dataset characteristics (from Nakayama 2024, Wu 2025); (2) Planned metrics and subgroup definitions; (3) Results placeholders in `results.md`.
