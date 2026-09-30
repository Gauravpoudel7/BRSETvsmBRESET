# How well do frozen foundation models transfer? A calibration-focused benchmark for diabetic retinopathy grading

**Citation:** Poyrazer M, Yagci H, Erten R. How well do frozen foundation models transfer? A calibration-focused benchmark for diabetic retinopathy grading. Frontiers in Medicine. 2026;13:1815982. doi: 10.3389/fmed.2026.1815982. Venue: Frontiers in Medicine. **Peer reviewed.**
**Year:** 2026
**Dataset(s) used:** APTOS 2019 (India, mixed cameras) for development, MESSIDOR-2 (France, Topcon TRC NW6 camera) for external testing
**Model(s)/method(s):** MedSigLIP, RETFound and EfficientNet-B0, all with frozen encoders and an identical small trained head. AUC, Brier score, expected calibration error, macro F1, temperature scaling.

## Summary (plain English)
The authors froze three pre-trained models, meaning they did not change the models themselves and only trained a small classifier on top. This is the cheapest way to reuse a big model. They trained on Indian eye photos and then tested on French eye photos taken with a different camera. They looked at both ranking ability (AUC) and honesty of the risk numbers (calibration). They also ran a contamination audit, checking whether any test data had secretly been in the models' original training.

## Key finding (plain English)
On the home dataset all three models looked equally good, with AUC between 0.980 and 0.985. On the foreign dataset they split apart badly: MedSigLIP held at 0.915 but RETFound crashed to 0.697 and EfficientNet-B0 to 0.745. So the retina-specific model actually did worse than a plain general-purpose ImageNet model, and all three completely failed to detect mild disease externally.

## Relevance to my research (plain English)
**Strongly supports my gap, and gives me a warning.** It shows that a big AUC drop across cameras and countries is normal, not surprising, which backs up the general setup of my study. More importantly it undercuts a natural assumption I might have made, that a retina-specialised model like RETFound will transfer better than a general one. Here it transferred worse, and the paper adds a second finding I should copy: temperature scaling fixed the risk numbers at home (external calibration error stayed at 0.086 to 0.149 despite it) but did not fix them under a domain change. So I should report both ranking and calibration, and I should not assume RETFound is the best choice for my device.
