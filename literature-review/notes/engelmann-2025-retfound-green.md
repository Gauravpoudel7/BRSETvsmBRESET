# Training a high-performance retinal foundation model with half-the-data and 400 times less compute (RETFound-Green)

**Citation:** Engelmann J, Bernabeu MO. Training a high-performance retinal foundation model with half-the-data and 400 times less compute. Nature Communications. 2025;16(1):6862. doi: 10.1038/s41467-025-62123-z. Venue: Nature Communications. **Peer reviewed.**
**Year:** 2025
**Dataset(s) used:** Open retinal image data for pre-training, with downstream evaluation on six public datasets
**Model(s)/method(s):** RETFound-Green, trained with a new self-supervised objective the authors call Token Reconstruction. Compared against RETFound-MEH and DERETFound, using both linear probing and full fine-tuning.

## Summary (plain English)
The complaint behind this paper is that foundation models are expensive to build. The authors invented a cheaper training objective that focuses on higher-level, abstract picture features instead of exact pixels. With it they trained a retinal foundation model using half the data and 400 times less computing power than earlier models needed. They then compared it fairly across six public datasets, counting how often each model won by a statistically meaningful margin. "Linear probing" means freezing the model and training only a simple layer on top, which is the cheapest way to reuse it.

## Key finding (plain English)
RETFound-Green achieved more than twice as many statistically significant wins as the next best model, despite being far cheaper to train. Even with only linear probing it matched a fully fine-tuned RETFound-MEH.

## Relevance to my research (plain English)
**Supports my gap and is practically important for my company.** It shows that the newest retinal foundation models are getting smaller and cheaper, which matters if we ever want to run or retrain a model on or near a portable device. The linear probing result is the most useful part for me: if a frozen model plus a simple layer is enough, then adapting to our own camera is cheap. I should include RETFound-Green as a candidate model, and it also means my review should not treat "RETFound" as one fixed thing, since several variants now exist.
