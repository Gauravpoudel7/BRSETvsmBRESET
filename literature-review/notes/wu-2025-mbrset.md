# A portable retina fundus photos dataset for clinical, demographic, and diabetic retinopathy prediction (mBRSET)

**Citation:** Wu C, Restrepo D, Nakayama LF, Zago Ribeiro L, Shuai Z, Barboza NS, Sousa MLV, Fitterman RD, Pereira ADA, Regatieri CVS, Stuchi JA, Malerbi FK, Andrade RE. A portable retina fundus photos dataset for clinical, demographic, and diabetic retinopathy prediction. Scientific Data. 2025;12(1):323. doi: 10.1038/s41597-025-04627-3. Venue: Scientific Data (Nature Portfolio). **Peer reviewed.** Data: Nakayama LF, Zago Ribeiro L, Restrepo D, et al. mBRSET, a Mobile Brazilian Retinal Dataset, version 1.0. PhysioNet; 2024. doi: 10.13026/qxpd-1y65
**Year:** 2025
**Dataset(s) used:** mBRSET itself: 5,164 fundus photos from 1,291 patients with diabetes, taken with the Phelcom Eyer handheld camera at the Itabuna Diabetes Campaign in Bahia, Brazil, in November 2022
**Model(s)/method(s):** ConvNeXt V2, DINOv2 and Swin V2. Tasks were diabetic retinopathy (binary and three-class), macular edema, plus sex, education level and insurance status. F1 score and accuracy.

## Summary (plain English)
This is the paper that introduced mBRSET, my other dataset. The photos were taken with a Phelcom Eyer, which is a small camera that clips onto a Samsung Galaxy S10 phone. It shoots a 45 degree view at 1600 by 1600 pixels, and here it was used after eye drops widened the pupils. Trained non-medical staff took the pictures at a community diabetes event, not in a hospital. The dataset is the first public one of its kind using handheld cameras in a real, busy, low-resource setting. Alongside disease labels it records age, sex, education level, insurance status, diabetes duration, treatments and other conditions.

## Key finding (plain English)
Standard models reached good accuracy on these handheld pictures, with a best F1 score of 87.4 for telling healthy eyes from diabetic retinopathy, which the authors describe as comparable to tabletop cameras. More surprisingly, the models could also guess a patient's sex (F1 up to 84.38) and even their insurance status (F1 up to 76.11) just from the eye photo.

## Relevance to my research (plain English)
**Foundational, and it partly limits my claim of novelty.** This is my target dataset, so I need its numbers exactly. Note the cohort details that will shape my fairness analysis: 65.06% female, mean age 61.44 years, 92.3% with no health insurance, and the largest education group being incomplete primary school at 42.2%. Because so few people have insurance, that subgroup will be tiny and my error bars will be wide. Also important: version 1.0 has no race or ethnicity labels, so I cannot study that. Finally, the fact that models can read insurance status off a retina photo is a warning sign. It means the model may be picking up on social background instead of disease, which is exactly the sort of hidden shortcut my fairness analysis should look for.
