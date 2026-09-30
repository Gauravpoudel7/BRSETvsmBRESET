# A multimodal visual-language foundation model for computational ophthalmology (EyeCLIP)

**Citation:** Shi D, Zhang W, Yang J, Huang S, Chen X, Xu P, Jin K, Lin S, Wei J, Yusufu M, Liu S, Zhang Q, Ge Z, Xu X, He M. A multimodal visual-language foundation model for computational ophthalmology. npj Digital Medicine. 2025;8(1):381. doi: 10.1038/s41746-025-01772-2. Venue: npj Digital Medicine. **Peer reviewed.**
**Year:** 2025
**Dataset(s) used:** Multimodal ophthalmic imaging data paired with text
**Model(s)/method(s):** EyeCLIP, a vision-language foundation model using multimodal contrastive learning

## Summary (plain English)
EyeCLIP learns from eye images together with written clinical text. Contrastive learning means the model is shown matching and mismatching image-text pairs, and it learns by pulling matching pairs together and pushing mismatched ones apart. Because it understands words as well as pictures, it can take written context into account when making a prediction, rather than working from the image alone. It covers several imaging types rather than just one.

## Key finding (plain English)
Combining images with text during training produces a model that can be used flexibly across eye care tasks, and opens the door to predictions that use written clinical information alongside the picture.

## Relevance to my research (plain English)
**Supports my gap and suggests a future extension.** It is the newest branch of the retinal foundation model family and worth naming in my review so the model landscape looks complete. Its real interest for my question is that both BRSET and mBRSET carry rich patient details such as age, diabetes duration and insurance status. A model that can take text alongside the image could in principle use that context, which is a natural follow-up to my study. It also raises a fairness worry I should flag: if a model is fed socioeconomic context directly, it may start relying on it rather than on the actual eye damage.
