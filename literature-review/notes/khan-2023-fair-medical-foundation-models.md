# How Fair are Medical Imaging Foundation Models?

**Citation:** Khan MO, Afzal MM, Mirza S, Fang Y. How Fair are Medical Imaging Foundation Models? In: Proceedings of the 3rd Machine Learning for Health Symposium. Proceedings of Machine Learning Research, volume 225. PMLR; 2023:217-231. Venue: ML4H 2023 Symposium. **Peer reviewed.**
**Year:** 2023
**Dataset(s) used:** Chest X-ray data, including CheXpert, described as having a 59/41 male-female split and a highly skewed 78/15/7 White, Asian, Black racial split
**Model(s)/method(s):** Six foundation models spanning different pre-training methods, pre-training data sources and architectures. Fine-tuning on balanced datasets used to separate pre-training bias from fine-tuning bias.

## Summary (plain English)
This study compares six foundation models and asks whether they treat patient subgroups equally. Its clever move is to fine-tune every model on a deliberately balanced dataset, one with equal numbers from each racial group. That way, any unfairness left over must have come from the original pre-training rather than from the fine-tuning data. They also tested whether more pre-training data and more pre-training rounds change the picture. The images here are chest X-rays, not eyes.

## Key finding (plain English)
Models pre-trained on medical images scored better overall but were consistently less fair than models pre-trained on ordinary everyday photographs, sometimes even less fair than a model trained from scratch. Fine-tuning on balanced data only partly fixed this, and every model consistently underperformed on female patients.

## Relevance to my research (plain English)
**Supports my gap, and it directly challenges an assumption I might have made.** The natural belief is that a specialised medical model like RETFound is the responsible, safe choice. This paper says medical pre-training bought accuracy at the cost of fairness. That is the fairness twin of the accuracy finding in Men et al. and Poyrazer et al., where retina-specific pre-training also transferred worse. It also gives me a method I can borrow: comparing a retina-specific model against a general-purpose one lets me attribute any unfairness to the pre-training choice. The main limit is that it uses chest X-rays, so I should present it as a cross-domain lesson rather than direct retinal evidence.
