# Disentanglement and Assessment of Shortcuts in Ophthalmological Retinal Imaging Exams

**Citation:** Fernandes L, Goncalves T, Matos J, Nakayama LF, Cardoso JS. Disentanglement and Assessment of Shortcuts in Ophthalmological Retinal Imaging Exams. arXiv:2507.09640; posted 13 July 2025. Venue: arXiv. **Preprint, listed as under review.** Code: https://github.com/leofer99/disentanglement_retinal_images
**Year:** 2025
**Dataset(s) used:** mBRSET (handheld camera images), macula-centred images only
**Model(s)/method(s):** ConvNeXt V2, DINOv2 and Swin V2. Disentanglement used as a bias mitigation method. Group fairness measured with AUROC per subgroup, risk distribution plots, and decision curve analysis.

## Summary (plain English)
This team asked whether AI models judging eye photos treat all kinds of patients equally. They trained three models on mBRSET to spot diabetic retinopathy, which is eye damage caused by diabetes. They also trained the models to guess patient traits like age and sex, to see how much of that information is sitting in the images. Then they split accuracy by subgroup: age (50 and under versus over 50), sex, education (literate versus illiterate), insurance (none versus insured), and obesity. Finally they tried "disentanglement," which means trying to force the model to separate disease signals from patient-trait signals so it stops leaning on the wrong clues.

## Key finding (plain English)
The models were good at spotting disease, up to 94% AUROC, but they were not equally good for everyone, with roughly a 10 percentage point AUROC gap between age groups for DINOv2. Trying to fix this with disentanglement helped DINOv2 slightly (2% AUROC gain) but actually hurt ConvNeXt V2 and Swin V2 (7% and 3% drops).

## Relevance to my research (plain English)
**This is the closest existing work to my fairness half, so it also trims my novelty.** It already does subgroup fairness on mBRSET using the exact attributes I care about, including education and insurance. Three gaps keep my angle alive. First, it stays entirely inside mBRSET, so it never asks what happens when a model trained on clinic cameras is moved to handheld ones. Second, it does not test a retinal foundation model like RETFound, only general-purpose backbones. Third, it measures fairness of a model trained on the target data, not fairness of a transferred model. My question is about the *change* in the gap when the camera changes, which is different. Worth noting that Matos and Nakayama are also BRSET authors, so this group may well extend it to the cross-camera case next. I should recheck this paper before I submit anything.
