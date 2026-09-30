# A Foundation Language-Image Model of the Retina (FLAIR): encoding expert knowledge in text supervision

**Citation:** Silva-Rodriguez J, Chakor H, Kobbi R, Dolz J, Ben Ayed I. A Foundation Language-Image Model of the Retina (FLAIR): encoding expert knowledge in text supervision. Medical Image Analysis. 2025;99:103357. doi: 10.1016/j.media.2024.103357. Also arXiv:2308.07898. Venue: Medical Image Analysis. **Peer reviewed.**
**Year:** 2025
**Dataset(s) used:** 38 open-access fundus imaging datasets, 288,307 images, covering up to 101 different target conditions
**Model(s)/method(s):** FLAIR, a vision-language model. Descriptive text prompts written from clinical literature are used during both pre-training and zero-shot inference. Evaluated with linear probing and few-shot settings.

## Summary (plain English)
FLAIR takes a different route from RETFound. Instead of learning only from pictures, it learns from pictures paired with written descriptions. Those descriptions are not simple labels but expert sentences describing what a condition looks like, and how conditions relate to each other. This lets the model do "zero-shot" work, meaning it can be asked about a condition it was never explicitly trained to classify, just by describing that condition in words. "Few-shot" means learning from only a handful of labelled examples.

## Key finding (plain English)
Adding expert written knowledge produced strong performance when the test data looked different from the training data or contained unseen categories. With only a simple layer trained on top, FLAIR beat fully trained dataset-specific models, and beat both bigger general-purpose image-language models and retina-specific self-supervised models.

## Relevance to my research (plain English)
**Supports my gap and offers a third model type to test.** This is the strongest published claim I found that a retinal foundation model holds up under domain shift, which is the mismatch between training data and deployment data. That makes it a direct test case for my question: if FLAIR really is more robust, it should lose less accuracy on mBRSET than RETFound does. Its use of 38 assembled public datasets is also relevant, because varied sources may be what buys robustness. One caution: because it absorbed 38 public datasets, I must check whether any overlap with my test data before claiming a clean external validation.
