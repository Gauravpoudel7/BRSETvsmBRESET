# FairMedFM: Fairness Benchmarking for Medical Imaging Foundation Models

**Citation:** Jin R, Xu Z, Zhong Y, Yao Q, Dou Q, Zhou SK, Li X. FairMedFM: Fairness Benchmarking for Medical Imaging Foundation Models. arXiv:2407.00983; posted 1 July 2024. Venue: arXiv. **Preprint.**
**Year:** 2024
**Dataset(s) used:** 17 public medical imaging datasets, **including BRSET**, alongside CheXpert, MIMIC-CXR, HAM10000, FairVLMed10k, GF3300, PAPILA and others
**Model(s)/method(s):** Many foundation models evaluated for classification and segmentation. Sensitive attributes include sex, age, race, preferred language and skin tone. Mitigation methods tested include linear probing, LoRA, and group-based approaches.

## Summary (plain English)
This is a large fairness testbed rather than a single experiment. The authors assembled 17 public datasets covering many body parts and imaging types, from X-ray and CT to eye photos and skin images. They then ran a wide range of foundation models through the same fairness checks, using several ways of adapting each model. Finally they tested whether existing bias-reduction methods actually work on foundation models, since most of those methods were designed for ordinary neural networks.

## Key finding (plain English)
Unfairness showed up consistently across foundation models and across ways of using them, and it was not specific to any one model. Existing bias mitigation methods were not reliably effective, sometimes improving fairness scores while costing accuracy, and sometimes doing neither.

## Relevance to my research (plain English)
**Supports my gap and partly overlaps my datasets.** BRSET is already in this benchmark, so I should acknowledge that BRSET fairness has been examined at benchmark scale and not claim it is untouched. Two things keep my angle open. First, mBRSET is not in the 17 datasets, so the handheld side is unexamined here. Second, this benchmark measures fairness within each dataset, not the change in fairness when a model is moved between devices. The finding that mitigation methods often fail is also a useful expectation-setter: if I do find uneven drops, I should not promise an easy fix.
