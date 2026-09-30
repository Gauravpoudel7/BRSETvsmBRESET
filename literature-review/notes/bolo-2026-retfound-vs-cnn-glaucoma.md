# Comparison of RETFound and a Supervised Convolutional Neural Network for Detection of Referable Glaucoma from Fundus Photographs

**Citation:** Bolo K, Nguyen TH, Iyengar S, Li Z, Nguyen V, Wong BJ, Do JL, Ambite JL, Kesselman C, Daskivich LP, Xu BY. Comparison of RETFound and a Supervised Convolutional Neural Network for Detection of Referable Glaucoma from Fundus Photographs. Ophthalmology Science. 2026;6(2):101008. doi: 10.1016/j.xops.2025.101008. Venue: Ophthalmology Science. **Peer reviewed.**
**Year:** 2026
**Dataset(s) used:** Los Angeles County Department of Health Services images as the internal set, University of Southern California images as the external set, chosen to vary camera type, magnification and field of view
**Model(s)/method(s):** RETFound compared against a supervised VGG-19 convolutional neural network, each trained on both uncropped images and images cropped to the optic nerve

## Summary (plain English)
This team tested glaucoma detection rather than diabetic retinopathy, but their design directly targets the camera question. They trained on images from one health system and tested on images from another, and they picked that second set specifically because it used different cameras with different magnification and framing. They also compared two input styles: the full eye photo, and a version cropped tightly around the optic nerve, which is the part of the eye glaucoma damages. Cropping is a common trick to remove irrelevant variation.

## Key finding (plain English)
The uncropped RETFound model was the most robust to the change in camera and setting, holding its scores on the external set while the other models degraded. Cropping helped the conventional VGG-19 model but hurt RETFound, because cropping removed the broad whole-image patterns RETFound had learned during pre-training.

## Relevance to my research (plain English)
**Partially conflicts with my expected result, which makes it essential.** Most of my other sources show RETFound transferring poorly. Here it transfers best, and the authors explicitly credit its pre-training on varied fundus images for handling different cameras. Their conclusion is that foundation models may be preferable exactly when training data is limited and domain shift is expected, which is my company's situation. It also hands me a concrete design warning: how I crop and preprocess mBRSET images could change my answer, so I should test more than one preprocessing choice rather than picking one and reporting a single number.
