# Does Data-Efficient Generalization Exacerbate Bias in Foundation Models?

**Citation:** Queiroz D, Carlos A, Fatoretto M, Nakayama LF, Anjos A, Berton L. Does Data-Efficient Generalization Exacerbate Bias in Foundation Models? arXiv:2408.16154; posted 28 August 2024. Presented at the Fairness and Ethics Towards Transparent AI (FAILED) workshop at ECCV 2024. Venue: arXiv preprint with workshop presentation.
**Year:** 2024
**Dataset(s) used:** **BRSET.** Patients missing age or sex were removed and classes were balanced to 50% with and 50% without diabetic retinopathy, leaving 1,097 patients and 1,416 images.
**Model(s)/method(s):** RETFound fine-tuned on BRSET, compared against supervised learning. Protected attributes were sex and age. Nationality was discarded because every patient is Brazilian. Fairness measured as the gap between the highest and lowest subgroup AUC.

## Summary (plain English)
This is the closest existing study to the fairness half of my question. They fine-tuned RETFound on BRSET, which is a Brazilian dataset quite unlike RETFound's mostly British training data. They then checked whether accuracy differed between men and women, and between age groups, comparing RETFound against ordinary supervised training. Then they repeated the whole thing with less and less training data, because using little labelled data is the main selling point of foundation models. "Protected attribute" just means a patient trait we do not want the model to treat people unequally on.

## Key finding (plain English)
RETFound was fairer than supervised learning, narrowing the gap between the best and worst performing subgroups for both sex and age. But when they cut the training data down, the gap widened again specifically for age, while sex stayed stable.

## Relevance to my research (plain English)
**This is a partial overlap and the single most useful methodological guide for my fairness analysis.** It already pairs RETFound with BRSET and already measures max-minus-min subgroup AUC gaps by age and sex, so I must not present that combination as new. What it does not do is touch mBRSET, handheld cameras, or education and insurance status, so my cross-camera question survives. Its result also gives me a sharp prediction to test: if reducing data widens the age gap, then changing the camera, which is another kind of harder condition, might widen it too. Note Nakayama is an author here as well, so this is again the BRSET group.
