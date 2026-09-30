# How Generalizable Are Foundation Models When Applied to Different Demographic Groups and Settings?

**Citation:** Xiong Z, Wang X, Zhou Y, Keane PA, Tham YC, Wang YX, Wong TY. How Generalizable Are Foundation Models When Applied to Different Demographic Groups and Settings? NEJM AI. 2025;2(1). doi: 10.1056/AIcs2400497. Venue: NEJM AI. **Peer reviewed.**
**Year:** 2025
**Dataset(s) used:** An Asian-specific retinal image dataset, used for fine-tuning and testing
**Model(s)/method(s):** RETFound compared against a conventional Vision Transformer pre-trained on ImageNet. Three tasks: glaucoma diagnosis, coronary heart disease diagnosis, and three-year stroke risk prediction.

## Summary (plain English)
RETFound was built mostly from British hospital data, so this team asked whether it still helps on Asian patients. They fine-tuned RETFound on an Asian dataset and compared it with an ordinary Vision Transformer that had only been trained on everyday photographs. To make the comparison fair they used the same model architecture for both, so the only real difference was what each had been pre-trained on. They repeated the three tasks from the original RETFound paper. They also tried using less training data, since that is where foundation models are supposed to shine.

## Key finding (plain English)
With the full dataset RETFound gave no meaningful advantage, scoring AUCs of 0.863, 0.628 and 0.557 against 0.853, 0.621 and 0.543 for the plain model, with all comparisons statistically indistinguishable. Even with a quarter of the data or less, its edge reached at most 0.03 AUC and was still not statistically significant.

## Relevance to my research (plain English)
**Supports my gap strongly, and it is the demographic mirror of my question.** This is the clearest peer-reviewed evidence that RETFound's advantage does not automatically travel to a population unlike its training data. My study asks the same thing but changes the camera as well as the population, using Brazilian patients instead of Asian ones. It also matters that this is co-authored by Yukun Zhou and Pearse Keane, who built RETFound, so it is not an outsider attack. Li et al. 2026 cite this paper for the same reason, which tells me it is the accepted reference point for this concern.
