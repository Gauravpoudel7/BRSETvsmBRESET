# Comparison of foundation models and transfer learning strategies for diabetic retinopathy classification

**Citation:** Li LY, Lebiecka-Johansen B, Byberg S, Thambawita V, Hulman A. Comparison of foundation models and transfer learning strategies for diabetic retinopathy classification. medRxiv 2026.04.17.26351092; posted 20 April 2026. doi: 10.64898/2026.04.17.26351092. Venue: medRxiv. **Preprint, not peer reviewed.** Code: https://github.com/hulmanlab/brset_mlcp
**Year:** 2026
**Dataset(s) used:** BRSET (16,266 images, clinic-grade Canon and Nikon cameras) and mBRSET (5,164 images, Phelcom Eyer handheld camera)
**Model(s)/method(s):** DINOv3 (ViT-Large), RETFound, VisionFM, plus RETFound-DINOv2-SDPP and RETFound-DINOv2-MEH variants. Head fine-tuning and full fine-tuning. AUROC, calibration curves, expected calibration error, Platt scaling, temperature scaling, decision curve analysis.

## Summary (plain English)
This team took three big pre-trained AI models and taught each one to spot diabetic retinopathy using BRSET, the clinic-camera dataset. Diabetic retinopathy is eye damage caused by diabetes. "Pre-trained" means the model already learned general picture patterns from millions of images before this study started. They then ran those trained models on mBRSET, the handheld-camera dataset, without any extra training. Finally they re-trained the models on mBRSET to see if that fixed things. They measured two separate things: whether the model can rank sick eyes above healthy eyes (called AUROC, where 1.0 is perfect and 0.5 is a coin flip), and whether the model's stated percentage risk is honest (called calibration).

## Key finding (plain English)
Every model got clearly worse on the handheld images. AUROC was 0.90 to 0.98 on BRSET but only 0.70 to 0.85 on mBRSET, a fall of 0.12 to 0.25. Re-training on mBRSET won back 0.04 to 0.10 of that. All models also gave dishonest risk numbers, almost always claiming more risk than was really there.

## Relevance to my research (plain English)
**This directly overlaps my original question, and it is the single most important paper for me to know about.** It is my exact two datasets, my exact experiment, and one of my exact models (RETFound). So "does an off-the-shelf model still work on handheld images" is no longer an open question. Two things save my angle. First, they never split the results by patient group, so nothing here tells me whether the drop hurts older, poorer, or less educated patients more. Second, they say plainly that they cannot tell whether the drop came from the camera or from the fact that the two patient groups are very different (7% of BRSET images show diabetic retinopathy versus 23% in mBRSET). That unanswered question is a real opening for me.
