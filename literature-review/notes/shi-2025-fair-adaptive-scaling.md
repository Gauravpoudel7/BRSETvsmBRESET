# Equitable Deep Learning for Diabetic Retinopathy Detection Using Multidimensional Retinal Imaging With Fair Adaptive Scaling

**Citation:** Shi M, Afzal MM, Huang H, Wen C, Luo Y, Khan MO, Tian Y, Kim L, Fang Y, Wang M. Equitable Deep Learning for Diabetic Retinopathy Detection Using Multidimensional Retinal Imaging With Fair Adaptive Scaling. Translational Vision Science and Technology. 2025;14(7):1. doi: 10.1167/tvst.14.7.1. Venue: Translational Vision Science and Technology. **Peer reviewed.** Code: https://github.com/Harvard-Ophthalmology-AI-Lab/FairAdaptiveScaling
**Year:** 2025
**Dataset(s) used:** Two proprietary and two public datasets, covering wide-angle colour fundus images, scanning laser ophthalmoscopy fundus images and optical coherence tomography B-scans
**Model(s)/method(s):** Fair Adaptive Scaling added to EfficientNet and DenseNet121. Subgroups analysed by race, gender, ethnicity, marital status and preferred language. Measured with AUC and a new equity-scaled AUC.

## Summary (plain English)
This team measured unfair performance in diabetic retinopathy detection and then tried to fix it during training. Diabetic retinopathy is eye damage caused by diabetes. Their fix, Fair Adaptive Scaling, changes how much each training example counts as training goes along, so groups the model is struggling with get more attention. They also invented a single score, equity-scaled AUC, that blends overall accuracy with how unequal the results are across groups, so one number captures both. They tested on two image types, flat eye photos and cross-section scans.

## Key finding (plain English)
The fix produced real but modest gains. On colour fundus images, overall AUC and equity-scaled AUC rose from 0.88 and 0.83 to 0.90 and 0.84 by race, with Asian and White subgroup AUCs up 0.05 and 0.03. Gains for gender were about 0.01.

## Relevance to my research (plain English)
**Supports my gap and gives me the metric I should use.** Equity-scaled AUC solves a problem I will otherwise face: if I report an overall score plus five subgroup scores, my results become hard to read and easy to cherry-pick. One combined number that punishes large gaps is cleaner for a scholarship write-up. The paper is also a sobering benchmark on effect sizes, since a dedicated fairness method only moved things by about 0.01 to 0.05 AUC. If my subgroup gaps turn out to be around that size, I will need proper confidence intervals to say anything at all, which matters because some mBRSET subgroups are small. Note it uses race and language, which mBRSET does not record.
