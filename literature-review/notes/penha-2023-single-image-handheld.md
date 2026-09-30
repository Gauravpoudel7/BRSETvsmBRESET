# Single retinal image for diabetic retinopathy screening: performance of a handheld device with embedded artificial intelligence

**Citation:** Penha FM, Priotto BM, Hennig F, Przysiezny B, Wiethorn BA, Orsi J, Nagel IBF, Wiggers B, Stuchi JA, Lencione D, de Souza Prado PV, Yamanaka F, Lojudice F, Malerbi FK. Single retinal image for diabetic retinopathy screening: performance of a handheld device with embedded artificial intelligence. International Journal of Retina and Vitreous. 2023;9(1):41. doi: 10.1186/s40942-023-00477-6. Venue: International Journal of Retina and Vitreous. **Peer reviewed.**
**Year:** 2023
**Dataset(s) used:** 686 individuals from a mass screening programme in Blumenau, southern Brazil. Average age 59.2 years, 56.7% women, average diabetes duration 12.1 years. 82.5% used only the public health system and 43.4% were illiterate or had not finished elementary school.
**Model(s)/method(s):** EyerMaps AI on the Phelcom Eyer handheld camera. A modified Xception convolutional neural network trained on the Kaggle EyePACS dataset and then transfer-learned on roughly 16,000 Eyer images. One macula-centred image per eye, compared against a retinal specialist using two images per eye.

## Summary (plain English)
The question here is whether one photo per eye is enough, instead of the usual two. Fewer photos means faster screening and more people seen. The AI judged a single macula-centred image while the human expert had two images per eye, so the AI was working with less information on purpose. "Transfer learning" means the model first learned from a big public dataset and was then retrained on images from this specific device. The screened population was poor and largely dependent on public healthcare.

## Key finding (plain English)
Using one image per eye, the AI reached 93.6% sensitivity but only about 72% specificity, with an AUC of 0.86 and a negative predictive value of 98.0%. So it rarely missed disease but often flagged healthy people.

## Relevance to my research (plain English)
**Directly relevant to the product decision, and it quietly answers part of my question.** The most important detail is buried in the methods: this system was first trained on a large public clinic-camera dataset (EyePACS) and then retrained on about 16,000 images from the actual handheld device. In other words, the team that builds this camera did not trust a borrowed model on its own, they fine-tuned on their own device's images. That is real-world evidence for the "we need our own fine-tuning" answer my company is looking for. The population details are also useful, because 43.4% had little formal education, which is the kind of subgroup my fairness analysis targets. Note the authors include Phelcom staff and the paper had only one human evaluator.
