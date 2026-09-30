# BRSET: A Brazilian Multilabel Ophthalmological Dataset of Retina Fundus Photos

**Citation:** Nakayama LF, Restrepo D, Matos J, Ribeiro LZ, Malerbi FK, Celi LA, Regatieri CS. BRSET: A Brazilian Multilabel Ophthalmological Dataset of Retina Fundus Photos. PLOS Digital Health. 2024;3(7):e0000454. doi: 10.1371/journal.pdig.0000454. Venue: PLOS Digital Health. **Peer reviewed.** Data: Nakayama LF, Goncalves M, Zago Ribeiro L, Santos H, Ferraz D, Malerbi F, Celi LA, Regatieri C. A Brazilian Multilabel Ophthalmological Dataset (BRSET), version 1.0.2. PhysioNet; 2026. doi: 10.13026/mysn-8b26
**Year:** 2024
**Dataset(s) used:** BRSET itself: 16,266 colour fundus photos from 8,524 patients, collected at three outpatient eye centres in Sao Paulo, Brazil, between 2010 and 2020
**Model(s)/method(s):** DINOv2 Base used as a feature extractor, then Support Vector Machines and Logistic Regression. A ConvNeXt V2 model was also trained. 70% training and 30% testing split. AUC and macro F1 score.

## Summary (plain English)
This is the paper that introduced BRSET, one of my two datasets. A fundus photo is a picture of the back of the eye. The team gathered 16,266 such photos from Brazilian eye clinics and had a retina specialist label each one. Labels cover parts of the eye (optic disc, blood vessels, macula), picture quality (focus, lighting, framing, artefacts), and diseases including diabetic retinopathy, which is eye damage caused by diabetes. They also attached patient details: nationality, age, sex, medical history, insulin use, and how long the person had known they had diabetes. They built simple test models to show the data is usable.

## Key finding (plain English)
BRSET works as a training and testing resource, and it is the first dataset of its kind from Brazil and Latin America. Because it carries patient details, it lets researchers check whether a model performs worse for some groups of people than others.

## Relevance to my research (plain English)
**Foundational.** This is the source dataset for my study, so I need its exact numbers and limits. Two details matter a lot for my design. First, the photos come from two different clinic cameras, 65.1% Canon CR2 and 34.9% Nikon NF5050, which gives me a way to measure what a plain camera swap costs inside a single dataset. Second, the patient details include age and sex but **not** education or insurance status. That means I cannot compare education or insurance gaps between BRSET and mBRSET, only inside mBRSET. The authors also flag that a single expert did the labelling, which is a source of noise I should mention.
