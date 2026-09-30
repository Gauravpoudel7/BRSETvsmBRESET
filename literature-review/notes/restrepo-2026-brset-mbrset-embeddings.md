# Embedding-Based Representations for BRSET and mBRSET

**Citation:** Restrepo D, Wu C, Morley M, Celi LA, Nakayama LF. Embedding-Based Representations for BRSET and mBRSET, version 1.0.0. PhysioNet; published 30 March 2026. doi: 10.13026/1h4p-vz70. Venue: PhysioNet. **Data resource, credentialed access. Not a peer-reviewed article.**
**Year:** 2026
**Dataset(s) used:** BRSET and mBRSET
**Model(s)/method(s):** Precomputed image embeddings produced with modern vision backbones including DINOv3 and ConvNeXt, using a standardised preprocessing pipeline

## Summary (plain English)
This is not a study, it is a released resource. An "embedding" is a list of numbers that stands in for a picture. The idea is that instead of downloading heavy image files, you download the number lists and train small models on those. The team ran every BRSET and mBRSET image through several strong vision models and published the resulting number lists. They did this because training on full-size images needs a lot of computing power, and because privacy rules often block sharing of real eye photos. The release includes advice on how to use the embeddings properly.

## Key finding (plain English)
Working with these two Brazilian datasets no longer requires heavy computing power, because the image processing has already been done and shared. The authors advise users to apply domain adaptation or calibration when moving between datasets or devices, and to check performance across demographic subgroups.

## Relevance to my research (plain English)
**Supports my gap, and is directly useful to me practically.** The published guidance explicitly tells users to expect trouble when applying these embeddings across different devices, and to evaluate across demographic subgroups and imaging devices. That is essentially a public statement from the dataset creators that my question has not been settled. It also lowers my cost: if I use these embeddings I can run subgroup analyses on a laptop instead of a GPU cluster. The trade-off is that I would be locked into whichever backbones they used, so if I want RETFound specifically I still need to run the images myself.
