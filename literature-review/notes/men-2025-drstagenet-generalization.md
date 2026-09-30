# Deep learning generalization for diabetic retinopathy staging from fundus images (DRStageNet)

**Citation:** Men Y, Fhima J, Celi LA, Ribeiro LZ, Nakayama LF, Behar JA. Deep learning generalization for diabetic retinopathy staging from fundus images. Physiological Measurement. 2025;46(1):015001. doi: 10.1088/1361-6579/ada86a. Venue: Physiological Measurement. **Peer reviewed.**
**Year:** 2025
**Dataset(s) used:** Six public datasets with 91,984 images: EyePACS, DDR (China), APTOS (India), **BRSET (Brazil, diabetic subset of 2,489 images from 1,301 patients)**, MESSIDOR-2 (France), IDRiD (India)
**Model(s)/method(s):** Five pre-trained self-supervised Vision Transformers benchmarked, including DINOv2 and RETFound. Best one trained further with multi-source domain fine-tuning. Linearly weighted Cohen's kappa, multiclass accuracy, error analysis, attention heatmaps.

## Summary (plain English)
This team built a model to grade how severe diabetic retinopathy is, and they cared mainly about whether it keeps working on unfamiliar data. Diabetic retinopathy is eye damage caused by diabetes, and grading means saying how advanced it is rather than just yes or no. They gathered six public datasets from different countries with different cameras. They first compared five pre-trained models, then took the best one and trained it on several datasets at once, holding one dataset out each time to test on. They also checked why the model made mistakes.

## Key finding (plain English)
DINOv2, a model pre-trained on ordinary everyday photos, beat the others by 9.1% to 27.4% on most held-out datasets, while RETFound, the retina-specific model, came last in five of the six datasets. Training on several datasets at once improved results on four of five unfamiliar datasets, and 60% of the model's remaining "errors" were actually cases where the human label was wrong.

## Relevance to my research (plain English)
**Supports my gap, and is a partial overlap I must cite carefully.** This study already uses BRSET as one of its test domains, which means BRSET is established as an external validation set in this literature. It is a second independent finding that RETFound generalises poorly compared to general-purpose models, which is a real challenge to the idea that retinal foundation models are automatically the safe choice for a new device. It also gives me a strong method idea: training on several sources at once helped, so that is a fix I could recommend to my company. Note that BRSET is also co-authored by Nakayama, Ribeiro and Celi, who appear here too, so this is the same research network.
