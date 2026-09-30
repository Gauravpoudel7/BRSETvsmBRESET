# Are Traditional Deep Learning Model Approaches as Effective as a Retinal-Specific Foundation Model for Ocular and Systemic Disease Detection?

**Citation:** Yew SME, Lei X, Goh JHL, Chen Y, Srinivasan S, Chee M, Pushpanathan K, Zou K, Hou Q, Soh ZD, et al., Zhou Y, Keane PA, Liu Y, Cheng CY, Tham YC. Are Traditional Deep Learning Model Approaches as Effective as a Retinal-Specific Foundation Model for Ocular and Systemic Disease Detection? arXiv:2501.12016; posted 21 January 2025. Venue: arXiv. **Preprint.**
**Year:** 2025
**Dataset(s) used:** SEED and SP2 (Singapore), BES (China), UKBB (United Kingdom), APTOS-2019 and IDRID (India), MESSIDOR-2 (France), ODIR-5k and GAMMA (China), PAPILA (Spain)
**Model(s)/method(s):** RETFound compared against traditional deep learning approaches including supervised ResNet50 and Vision Transformer. Assessed for accuracy, label efficiency, computing cost and generalisability.

## Summary (plain English)
This is a broad head-to-head test of RETFound against ordinary deep learning models across many tasks and many countries. Label efficiency means how well a model does when you only have a small number of labelled examples, which is the main selling point of foundation models. The clever part of the design is the choice of external test sets: they deliberately picked some that match the training population's ethnicity and some that do not, so any drop can be linked to that mismatch.

## Key finding (plain English)
RETFound did beat traditional models for whole-body disease detection, especially with small amounts of fine-tuning data, but it still failed to close the gap when tested across ethnic groups. For diabetic retinopathy, a model fine-tuned on Indian data dropped more on French data (MESSIDOR-2) than on other Indian data (IDRID), and the same pattern appeared for glaucoma with Spanish versus Chinese test sets.

## Relevance to my research (plain English)
**Supports my gap and gives me my expected mechanism.** It is the cleanest published demonstration that the size of a foundation model's performance drop tracks how different the test population is from the training population. That is exactly the logic behind my study, since Brazilian patients in Bahia are very unlike London hospital patients. It also gives me a fair prediction to test: RETFound should help most when I have little mBRSET data to fine-tune with, but it should not fully remove the drop. Note this is a preprint and shares authors with RetBench and FusionFM, so these are related efforts from one Singapore-based group.
