# A trustworthy cross-domain AI framework for fundus disease classification using hybrid CNN fusion and supervised domain adaptation

**Citation:** Duhaim AM, Al-Bakry AM. A trustworthy cross-domain AI framework for fundus disease classification using hybrid CNN fusion and supervised domain adaptation. Discover Artificial Intelligence. 2026;6(1):967. doi: 10.1007/s44163-026-02067-5. Venue: Discover Artificial Intelligence (Springer). **Peer reviewed.**
**Year:** 2026
**Dataset(s) used:** Multi-centre fundus image pool, with an external test set of 4,640 images and a separate adaptation budget of 2,000 external images (500 per disease class)
**Model(s)/method(s):** FusionEye-Net, combining EfficientNet-B3 and ResNet-50. Preprocessing to reduce device differences. Lightweight supervised domain adaptation. Explainability methods.

## Summary (plain English)
This team built a model that merges two different network designs, one good at tiny details like microscopic bleeds and one good at overall structure. They deliberately designed the study "external validation first," meaning they always tested on data from other centres rather than only reporting home-turf results. When performance dropped on outside data, they applied a small fix: fine-tuning on just 2,000 outside images instead of retraining everything. "Domain shift" is their term for the mismatch between the data a model learned from and the data it later meets.

## Key finding (plain English)
Even a strong model fell to 72.05% accuracy on outside data because of differences in devices, conditions and patients. Fine-tuning on a small, cheap batch of target images recovered much of the loss without full retraining.

## Relevance to my research (plain English)
**Supports my gap and is highly relevant to the product decision.** It states the general scale of the problem, noting prior work where models above 95% internal accuracy fall by 20 to 40% externally, which matches what I expect between BRSET and mBRSET. Its practical value for my company is the "small adaptation budget" idea: if 500 labelled images per class is enough to recover performance, that is a realistic amount of data for a device maker to collect. I should quantify a similar minimum-data curve for mBRSET. One caution: this is a lower-profile journal than my other sources, so I should lean on it for the method idea rather than as headline evidence.
