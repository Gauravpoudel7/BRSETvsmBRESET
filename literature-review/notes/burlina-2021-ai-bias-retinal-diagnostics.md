# Addressing Artificial Intelligence Bias in Retinal Diagnostics

**Citation:** Burlina P, Joshi N, Paul W, Pacheco KD, Bressler NM. Addressing Artificial Intelligence Bias in Retinal Diagnostics. Translational Vision Science and Technology. 2021;10(2):13. doi: 10.1167/tvst.10.2.13. Earlier preprint: arXiv:2004.13515. Venue: Translational Vision Science and Technology. **Peer reviewed.**
**Year:** 2021
**Dataset(s) used:** Retinal fundus images split by lighter and darker skin pigmentation, used as a proxy for ethnicity
**Model(s)/method(s):** A baseline diagnostic deep learning system compared against systems whose training data was augmented using generative models to fill in the missing subgroup

## Summary (plain English)
This team created an unfairness problem on purpose so they could measure it. They removed all training images of referable diabetic retinopathy from people with darker skin, while still testing on those people. Referable means bad enough that the patient should see a specialist. The reason skin pigmentation matters is that it changes how pigmented the retina looks in a photo. They then used generative models, which invent realistic synthetic images, to manufacture the missing training examples and see if that closed the gap.

## Key finding (plain English)
The baseline model was 73.0% accurate for lighter-skinned individuals but only 60.5% for darker-skinned ones, a 12.5 percentage point gap that was statistically significant (P = .008). After filling in the missing group with generated images, the two groups came out at 72.0% and 71.5%, a gap of just 0.5 points and no longer significant (P = .912).

## Relevance to my research (plain English)
**Supports my gap and is the historical anchor for retinal AI fairness.** It is the paper to cite for the basic claim that unequal training data produces unequal accuracy in retinal AI, with a clean, large, quantified gap. It matters for my study because mBRSET comes from Bahia, a region with a high proportion of Afro-Brazilian and mixed-ancestry people, while RETFound's training data was mostly British. That is exactly the pigmentation-related mismatch this paper warns about. The frustrating limit is that mBRSET version 1.0 has no race or ethnicity labels, so I cannot test this axis directly and will have to say so plainly.
