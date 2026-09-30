# Automated Identification of Different Severity Levels of Diabetic Retinopathy Using a Handheld Fundus Camera and Single-Image Protocol

**Citation:** Malerbi FK, Nakayama LF, Melo GB, Stuchi JA, Lencione D, Prado PV, Ribeiro LZ, Dib SA, Regatieri CV. Automated Identification of Different Severity Levels of Diabetic Retinopathy Using a Handheld Fundus Camera and Single-Image Protocol. Ophthalmology Science. 2024;4(4):100481. doi: 10.1016/j.xops.2024.100481. Venue: Ophthalmology Science. **Peer reviewed.**
**Year:** 2024
**Dataset(s) used:** 327 analysed patients, of whom 307 completed the protocol. Mean age 57.0 years, mean diabetes duration 16.3 years. Handheld portable camera images, with the AI fine-tuned on portable device image datasets.
**Model(s)/method(s):** An AI system on a portable retinal camera, using one macula-centred image per eye. Ground truth was adjudicated reading by three certified ophthalmologists, against a reference standard of reading centre grading of a two-field protocol using the international diabetic retinopathy severity scale.

## Summary (plain English)
This study raises the bar on evidence quality for handheld screening. Rather than comparing the AI against a single grader, three certified ophthalmologists adjudicated the ground truth, and the reference standard came from a reading centre using the fuller two-field imaging protocol. The AI still only received one image per eye. Unlike most screening studies, they did not stop at "disease or no disease" but looked at different severity levels. The authors state the AI was fine-tuned using datasets of portable device images.

## Key finding (plain English)
The AI detected any diabetic retinopathy with 90.48% sensitivity and 90.65% specificity, and more than mild disease with 90.23% sensitivity and 85.06% specificity. AUROC was 0.95 for any disease and 0.89 for more than mild disease.

## Relevance to my research (plain English)
**Directly relevant, and it sets the performance bar I should compare against.** This is the strongest handheld-camera result I found, with both sensitivity and specificity around 90% under a rigorous reference standard. That is important context: if a borrowed foundation model only reaches 0.70 to 0.85 AUROC on mBRSET, as Li et al. found, then a purpose-built and device-fine-tuned system is clearly better on the same kind of images. Note again that the model was fine-tuned on portable device images, reinforcing the pattern across all the Phelcom-linked papers. Several authors have commercial ties to Phelcom, which I should disclose when citing it, and Nakayama and Ribeiro also appear, tying it back to the BRSET group.
