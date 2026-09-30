# Diabetic Retinopathy Screening Using Artificial Intelligence and Handheld Smartphone-Based Retinal Camera

**Citation:** Malerbi FK, Andrade RE, Morales PH, Stuchi JA, Lencione D, de Paulo JV, Carvalho MP, Nunes FS, Rocha RM, Ferraz DA, Belfort R. Diabetic Retinopathy Screening Using Artificial Intelligence and Handheld Smartphone-Based Retinal Camera. Journal of Diabetes Science and Technology. 2022;16(3):716-723. doi: 10.1177/1932296820985567. Venue: Journal of Diabetes Science and Technology. **Peer reviewed.**
**Year:** 2022
**Dataset(s) used:** 824 individuals with type 2 diabetes enrolled at the Itabuna Diabetes Campaign, of whom 679 (82.4%) could be fully assessed. Images taken with the Phelcom Eyer handheld camera. The AI was trained on 10,569 fundus images captured between 2019 and 2020 exclusively with the Eyer device.
**Model(s)/method(s):** PhelcomNet, a convolutional neural network trained only on portable-device images, compared against human reading. AUC, sensitivity and specificity for more than mild disease.

## Summary (plain English)
This is the study that ran at the same Itabuna Diabetes Campaign that later produced mBRSET, using the same camera. The key design choice is the opposite of mine: instead of borrowing a model trained on clinic cameras, they trained their model from scratch using only Eyer images. That removes the camera mismatch problem by construction. They then compared the AI against a human grader on a large, mixed, real-world group of people with type 2 diabetes.

## Key finding (plain English)
The model reached 97.8% sensitivity but only 61.4% specificity, with an AUC of 0.89 for more than mild disease. Every case it missed turned out to be moderate non-proliferative disease, and over 80% of people produced images of good enough quality.

## Relevance to my research (plain English)
**Directly relevant to the product decision, and it partly answers it already.** This is essentially the counterfactual to my study. It shows what you get when a device maker trains on its own camera's images instead of reusing someone else's model: strong sensitivity in a real screening setting. That is evidence for the "build our own" option my company is weighing. It is also the closest ancestor of mBRSET, sharing the campaign, the device and several authors including Malerbi and Stuchi, so it gives me the clinical context for where my target images came from. The low specificity of 61.4% is worth carrying forward, because it means many healthy people were sent for review.
