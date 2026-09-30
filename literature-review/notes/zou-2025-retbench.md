# RetBench: Which Ophthalmic Foundation Model Performs Best and Why?

**Citation:** Zou K, Goh JHL, Zhou Y, Yew SME, Wang M, Fu H, Cheng CY, Tham YC. RetBench: Which Ophthalmic Foundation Model Performs Best and Why? In: Ophthalmic Medical Image Analysis (OMIA 2025), 12th International Workshop held with MICCAI 2025, Daejeon, South Korea. Lecture Notes in Computer Science. Springer; 2025:75-84. doi: 10.1007/978-3-032-10351-2_8. Venue: OMIA workshop at MICCAI 2025. **Peer reviewed workshop paper.**
**Year:** 2025
**Dataset(s) used:** Standardised datasets from multiple countries, including external validation sets
**Model(s)/method(s):** RETFound, VisionFM, RetiZero and DINORET, benchmarked on glaucoma, diabetic retinopathy and age-related macular degeneration detection, plus diabetes and hypertension prediction

## Summary (plain English)
Lots of eye foundation models have appeared, all claiming to be good, but they were each tested differently so nobody could compare them. This paper builds one standard test suite and runs four of them through it. They cover eye diseases and also whole-body conditions that show up in the retina, such as diabetes and high blood pressure. Crucially they include external validation, which means testing on data from a country the model was not tuned on.

## Key finding (plain English)
There is no single winner. DINORET, RetiZero and RETFound performed similarly on most tasks, with DINORET recommended specifically for glaucoma. For whole-body disease prediction on external data, RetiZero averaged 0.92 AUC against 0.88 for the next best model.

## Relevance to my research (plain English)
**Supports my gap and shapes my model choice.** Its most useful message for me is that picking the "best" retinal foundation model is task-dependent, so testing only RETFound would be a weak design. That argues for me running at least two or three models, which is also what Li et al. 2026 did. It also introduces RetiZero as a model I had not considered, with the best external validation numbers in this benchmark. What RetBench does not do is break results down by patient subgroup, so it strengthens rather than threatens my fairness angle.
