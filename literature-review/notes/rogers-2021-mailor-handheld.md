# Evaluation of an AI system for the detection of diabetic retinopathy from images captured with a handheld portable fundus camera: the MAILOR AI study

**Citation:** Rogers TW, Gonzalez-Bueno J, Garcia Franco R, Lopez Star E, Mendez Marin D, Vassallo J, Lansingh VC, Trikha S, Jaccard N. Evaluation of an AI system for the detection of diabetic retinopathy from images captured with a handheld portable fundus camera: the MAILOR AI study. Eye. 2021;35(2):632-638. doi: 10.1038/s41433-020-0927-8. Venue: Eye (Nature Portfolio). **Peer reviewed.**
**Year:** 2021
**Dataset(s) used:** 6,404 patients (about 80% with diabetes) screened at the Mexican Advanced Imaging Laboratory for Ocular Research using a handheld Pictor Plus camera (Volk Optical), compared against a publicly available desktop camera benchmark dataset
**Model(s)/method(s):** Pegasus, a commercial AI system (Visulytix). Graded by specialists using the Scottish diabetic retinopathy grading scheme. Assessed for referable and proliferative disease.

## Summary (plain English)
This is the closest published match to my question outside my own datasets. A commercial AI system was run on real handheld camera images from a Mexican screening programme, and the same system was also run on a curated public dataset taken with a traditional desktop camera. Comparing the two scores shows what changing to a handheld camera costs. Referable disease means bad enough to need a specialist. Proliferative disease means the advanced stage where fragile new blood vessels grow.

## Key finding (plain English)
For referable disease the AI scored 89.4% AUROC on the real handheld images versus 98.5% on the desktop benchmark, a large and statistically significant fall. For advanced proliferative disease there was no significant difference, with 94.3% on handheld versus 92.2% on the benchmark.

## Relevance to my research (plain English)
**Strongly supports my gap and predicts my likely result in detail.** It is the cleanest existing demonstration that moving an AI system from desktop-camera images to handheld images costs real accuracy. Its most valuable nuance is that the loss was not uniform across disease severity: obvious advanced disease survived the camera change, while the milder referable cases did not. That fits Poyrazer et al., where all models collapsed on mild disease externally. So I should analyse my drop by severity grade, not just as one overall number, since the practical risk is missing early disease. Its age, from 2021 and using pre-foundation-model AI, is the main limitation.
