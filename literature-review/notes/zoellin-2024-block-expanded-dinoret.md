# Block Expanded DINORET: Adapting Natural Domain Foundation Models for Retinal Imaging Without Catastrophic Forgetting

**Citation:** Zoellin J, Merk C, Buob M, Saad A, Giesser S, Spitznagel T, Turgut F, Santos R, Zhou Y, Wagner S, Keane PA, Tham YC, Cabrera DeBuc D, Becker MD, Somfai GM. Block Expanded DINORET: Adapting Natural Domain Foundation Models for Retinal Imaging Without Catastrophic Forgetting. arXiv:2409.17332; posted 25 September 2024. Venue: arXiv. **Preprint.** Code: https://github.com/cm090999/dinoret
**Year:** 2024
**Dataset(s) used:** Colour fundus photograph datasets for pre-training and fine-tuning
**Model(s)/method(s):** DINORET and BE-DINORET, built by adapting DINOv2 Vision Transformers to retinal images. Block expansion is used to avoid catastrophic forgetting. Compared against DINOv2 and RETFound.

## Summary (plain English)
DINOv2 is a strong model trained on ordinary everyday photographs. This team adapted it to eye photos. The problem they had to solve is called catastrophic forgetting, which is when teaching a model something new makes it lose what it already knew. Their fix, block expansion, adds fresh layers for the new eye-specific knowledge while leaving the original layers untouched, so nothing gets overwritten. They then compared their models with DINOv2 and RETFound on fundus photograph tasks.

## Key finding (plain English)
You can turn a general-purpose photo model into a competitive retinal model by adding new capacity rather than overwriting old knowledge, and the result competes with purpose-built retinal foundation models.

## Relevance to my research (plain English)
**Supports my gap indirectly.** Its importance to me is that it sits exactly on the fault line running through this whole literature: is a general-purpose model or a retina-specific model better on unfamiliar data? Several papers I found say general-purpose wins, and DINORET is the attempt to get both at once. In the RetBench comparison DINORET performed among the best, so it deserves a place in my candidate model list. It is still a preprint, so I should describe it as such.
