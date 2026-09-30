# Development and Validation of a Multimodal Multitask Vision Foundation Model for Generalist Ophthalmic Artificial Intelligence (VisionFM)

**Citation:** Qiu J, Wu J, Wei H, Shi P, Zhang M, Sun Y, Li L, Liu H, Liu H, Hou S, et al., Tham YC, Wong TY, Wang N, Yuan W. Development and Validation of a Multimodal Multitask Vision Foundation Model for Generalist Ophthalmic Artificial Intelligence. NEJM AI. 2024;1(12). doi: 10.1056/aioa2300221. Venue: NEJM AI. **Peer reviewed.**
**Year:** 2024
**Dataset(s) used:** 3.4 million ophthalmic images for pre-training, covering many eye diseases, several imaging types, multiple devices and varied patient demographics
**Model(s)/method(s):** VisionFM, a self-supervised multimodal and multitask foundation model

## Summary (plain English)
VisionFM is a rival to RETFound. "Multimodal" means it learned from several kinds of eye pictures, not just one, and "multitask" means it was built to handle many jobs such as screening, diagnosis, predicting how a disease will progress, and sorting diseases into subtypes. Its pre-training pile of 3.4 million images was deliberately varied, including images from different devices and different patient groups. That variety is the main design difference from RETFound.

## Key finding (plain English)
A single self-supervised model trained on a large and deliberately varied set of eye images can serve as a general-purpose starting point across many eye care tasks and imaging types.

## Relevance to my research (plain English)
**Foundational and directly comparable.** VisionFM is a natural second model for my study, and the reason is its pre-training claim: it says it covered multiple devices and demographics. That makes it a fair test of a hypothesis I care about, namely that varied pre-training protects against camera change. Note that Li et al. 2026 already tested this and VisionFM did not come out on top on mBRSET, which is worth reporting honestly rather than assuming the varied-data claim translates into real robustness.
