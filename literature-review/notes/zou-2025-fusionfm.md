# FusionFM: Fusing Eye-specific Foundational Models for Optimized Ophthalmic Diagnosis

**Citation:** Zou K, Goh JHL, Zhou Y, Lin T, Yew SME, Srinivasan S, Wang M, Santos R, Somfai GM, Fu H, Chen H, Keane PA, Cheng CY, Tham YC. FusionFM: Fusing Eye-specific Foundational Models for Optimized Ophthalmic Diagnosis. arXiv:2508.11721; posted 15 August 2025. Venue: arXiv. **Preprint.**
**Year:** 2025
**Dataset(s) used:** Ophthalmic imaging datasets across several diagnostic tasks
**Model(s)/method(s):** Combining several eye-specific foundation models, namely RETFound, VisionFM, RetiZero and DINORET, rather than choosing one

## Summary (plain English)
If different eye foundation models are each good at different things, why pick one? This paper tries fusing them, meaning it combines their outputs or features so the strengths add up. The authors first lay out how the four main models differ: RETFound learns from unlabelled retinal images, VisionFM was pre-trained across many imaging types and devices, RetiZero adds knowledge from ophthalmology literature and online sources, and DINORET adapts a general-purpose model while avoiding catastrophic forgetting, which is when new learning erases old learning.

## Key finding (plain English)
The authors point out that systematic head-to-head comparison of eye foundation models is still scarce, and propose fusing several models rather than relying on any single one.

## Relevance to my research (plain English)
**Supports my gap.** Its direct statement that systematic benchmarking of these models remains scarce is a useful, quotable justification for comparative work like mine. The fusion idea is also a possible recommendation for my company: if no single model is reliable on our device's images, an ensemble of several might be steadier than any one. As a preprint from the same group as RetBench and Yew et al., I should treat it as part of one ongoing effort rather than independent confirmation.
