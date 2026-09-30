# Master list of papers reviewed

39 papers. Grouped by theme, then newest year first. Where a year has several papers, the most relevant to my question comes first. Some papers appear under more than one theme, but each has only one note file.

My question, in one line: when an AI model trained on clinic-grade fundus camera images is used on portable handheld camera images, how much accuracy is lost, and does that loss fall harder on some patient groups than others?

Reading key:
- **Overlaps** means the paper already does part of what I planned.
- **Supports gap** means it strengthens the case that my question is open.
- **Conflicts** means it points the other way and I must deal with it honestly.

---

## Theme 1: Domain and camera generalization in retinal image AI

- **2026** [Li et al., foundation models on BRSET and mBRSET](notes/li-2026-brset-mbrset-foundation-models.md). Trained models on the clinic-camera dataset and tested on the handheld one. Accuracy fell a lot, from 0.90 to 0.98 down to 0.70 to 0.85. **Overlaps my question directly. Read this one first.**
- **2026** [Poyrazer et al., how well do frozen foundation models transfer](notes/poyrazer-2026-frozen-foundation-model-transfer.md). Moving from Indian to French eye photos, RETFound crashed from 0.980 to 0.697 while a general-purpose model held at 0.915. **Supports gap.**
- **2026** [Duhaim and Al-Bakry, cross-domain fundus framework](notes/duhaim-2026-cross-domain-fundus-framework.md). A strong model fell to 72% accuracy on outside data, but fine-tuning on just 2,000 outside images fixed much of it. **Supports gap.**
- **2025** [Men et al., DRStageNet generalization](notes/men-2025-drstagenet-generalization.md). Tested across six datasets including BRSET. A general-purpose model beat the retina-specific RETFound, which came last in five of six datasets. **Supports gap, partly overlaps because it already uses BRSET.**
- **2025** [Joseph et al., universal cross-camera image adaptation](notes/joseph-2025-universal-cross-camera-adaptation.md). Repainting incoming photos into one house style before the AI sees them reduces the loss from switching cameras. **Supports gap and suggests a cheap fix.**
- **2024** [Zhang et al., cross-camera adaptation for heart risk](notes/zhang-2024-cross-camera-cvd-risk.md). Same camera problem, different task. Forces the model to give the same answer on clinic and portable images. **Supports gap.**
- **2024** [Xia et al., DECO for unseen domains](notes/xia-2024-deco-unseen-domains.md). Separates disease signals from source signals, and explicitly counts age, sex and ethnicity as part of that source noise. **Supports gap and links my two halves.**
- **2023** [He et al., cross-camera performance including a portable camera](notes/he-2023-cross-camera-portable-cameras.md). Concludes portable cameras are workable with existing AI. **Conflicts with my expected result, so worth keeping.**
- **2020** [Yang et al., residual-CycleGAN camera adaptation](notes/yang-2020-residual-cyclegan-camera-adaptation.md). The early paper proving camera brand alone can break a diabetic retinopathy model. **Supports gap, useful as history.**

## Theme 2: Retinal foundation models

- **2026** [Bolo et al., RETFound versus a supervised CNN for glaucoma](notes/bolo-2026-retfound-vs-cnn-glaucoma.md). Here RETFound was the most robust model when the camera changed, and cropping the image hurt it. **Conflicts with my expected result. Important.**
- **2025** [Xiong et al., how generalizable are foundation models](notes/xiong-2025-foundation-model-generalizability.md). On Asian patients, RETFound gave no real advantage over a plain ImageNet model. Co-authored by RETFound's own creators. **Supports gap strongly.**
- **2025** [Yew et al., traditional deep learning versus a retinal foundation model](notes/yew-2025-traditional-versus-foundation.md). RETFound helps most when data is scarce, but still drops more when the test population differs ethnically. **Supports gap.**
- **2025** [Chen et al., independent evaluation of RETFound on the optic nerve](notes/chen-2025-retfound-optic-nerve.md). RETFound transfers to tasks it was never trained for, but the authors warn their images came mostly from one machine and may not generalise to other devices. **Supports gap through its own stated limitation.**
- **2025** [Engelmann and Bernabeu, RETFound-Green](notes/engelmann-2025-retfound-green.md). A retinal foundation model trained with half the data and 400 times less computing power, matching bigger models. **Supports gap, and cheap enough for a device company.**
- **2025** [Silva-Rodriguez et al., FLAIR](notes/silva-rodriguez-2025-flair.md). Learns from images plus expert written descriptions, and claims strong results when test data looks different. **Supports gap, a robustness claim I can test.**
- **2025** [Zou et al., RetBench](notes/zou-2025-retbench.md). Standard head-to-head test of four eye foundation models. No single winner, so testing only one model would be weak. **Supports gap.**
- **2025** [Zou et al., FusionFM](notes/zou-2025-fusionfm.md). Combines several eye foundation models instead of picking one, and states plainly that systematic comparison is still scarce. **Supports gap.**
- **2025** [Shi et al., EyeCLIP](notes/shi-2025-eyeclip.md). Learns from eye images paired with clinical text, so written patient context can feed the prediction. **Supports gap, a future extension.**
- **2024** [Qiu et al., VisionFM](notes/qiu-2024-visionfm.md). Pre-trained on 3.4 million eye images across many devices and patient groups, which is meant to make it more robust. **Foundational, and a fair test of the varied-data idea.**
- **2024** [Zoellin et al., Block Expanded DINORET](notes/zoellin-2024-block-expanded-dinoret.md). Adapts a general-purpose photo model to eyes by adding new layers rather than overwriting old ones. **Supports gap.**
- **2023** [Zhou et al., RETFound](notes/zhou-2023-retfound.md). The original retinal foundation model, trained on 1.6 million unlabelled retinal images, mostly from one London hospital. **Foundational. Explains why Brazilian handheld photos are doubly unfamiliar to it.**

## Theme 3: Fairness and demographic bias in retinal and diabetic retinopathy AI

- **2025** [Shi et al., Fair Adaptive Scaling](notes/shi-2025-fair-adaptive-scaling.md). Adjusts training to help struggling subgroups, and introduces equity-scaled AUC, one number combining accuracy and fairness. **Supports gap and gives me my metric.**
- **2025** [Moya-Sanchez et al., RAIS-DR](notes/moya-sanchez-2025-rais-dr.md). A referral system that beat the approved EyeArt product and found almost no bias across sex and age. **Conflicts with my expectation, and supplies fairness measures.**
- **2024** [Queiroz et al., does data-efficient generalization exacerbate bias](notes/queiroz-2024-data-efficient-bias.md). RETFound fine-tuned on BRSET was fairer than ordinary training, but the age gap widened when training data shrank. **Overlaps my fairness half. Closest methodological guide.**
- **2024** [Jin et al., FairMedFM](notes/jin-2024-fairmedfm.md). A 17-dataset fairness benchmark that already includes BRSET. Bias was everywhere and existing fixes often failed. **Supports gap, partly overlaps.**
- **2023** [Khan et al., how fair are medical imaging foundation models](notes/khan-2023-fair-medical-foundation-models.md). Medical-image pre-training gave better accuracy but consistently worse fairness than everyday-photo pre-training. **Supports gap, challenges my assumptions.**
- **2021** [Burlina et al., addressing AI bias in retinal diagnostics](notes/burlina-2021-ai-bias-retinal-diagnostics.md). Missing darker-skinned training data caused a 12.5 point accuracy gap, which generated images almost erased. **Supports gap, the historical anchor.**

## Theme 4: BRSET and mBRSET specifically

- **2026** [Li et al., foundation models on BRSET and mBRSET](notes/li-2026-brset-mbrset-foundation-models.md). See theme 1. **The single most important paper for judging my novelty.**
- **2026** [Restrepo et al., embeddings for BRSET and mBRSET](notes/restrepo-2026-brset-mbrset-embeddings.md). Pre-computed number lists for both datasets, released with advice to adapt across devices and check subgroups. **Supports gap, and saves me computing power.**
- **2025** [Wu et al., mBRSET](notes/wu-2025-mbrset.md). The handheld dataset itself. 5,164 images, 1,291 patients, 92.3% uninsured, no race labels. Models could guess insurance status from an eye photo. **Foundational, and partly limits my novelty.**
- **2025** [Fernandes et al., disentanglement and shortcuts](notes/fernandes-2025-disentanglement-shortcuts.md). Subgroup fairness on mBRSET across age, sex, education, insurance and obesity. Roughly a 10 point age gap. **Overlaps my fairness half. Read this second.**
- **2025** [Men et al., DRStageNet generalization](notes/men-2025-drstagenet-generalization.md). See theme 1. Already uses BRSET as an external test set.
- **2024** [Nakayama et al., BRSET](notes/nakayama-2024-brset.md). The clinic-camera dataset itself. 16,266 images, 8,524 patients, two camera models, and no education or insurance fields. **Foundational.**
- **2024** [Queiroz et al., data-efficient generalization and bias](notes/queiroz-2024-data-efficient-bias.md). See theme 3. Already pairs RETFound with BRSET.
- **2024** [Jin et al., FairMedFM](notes/jin-2024-fairmedfm.md). See theme 3. Already includes BRSET.

## Theme 5: Handheld and portable camera AI screening, and low-resource deployment

- **2026** [Grace et al., AI for diabetic retinopathy in low-resource settings](notes/grace-2026-lmic-dr-screening-review.md). Reviews five deployed products and names data generalisability as one of four main barriers. **Supports gap, good for my introduction.**
- **2025** [Wang et al., meta-analysis of regulator-approved systems](notes/wang-2025-regulator-approved-meta-analysis.md). 82 studies, 887,244 exams. Pooled accuracy is high, but only 44% used a genuinely external test set. **Supports gap. My strongest framing statistic.**
- **2025** [Duggal et al., real-world screening in Indian public clinics](notes/duggal-2025-real-world-india.md). Commercial products scored specificity between 14% and 96% on low-cost camera images, and one vendor withdrew mid-study. **Supports gap. The most sobering paper here.**
- **2025** [Onyeze et al., systematic review of AI in low- and middle-income countries](notes/onyeze-2025-lmic-systematic-review.md). Ten years and six databases produced only a handful of qualifying studies. **Supports gap.**
- **2024** [Malerbi et al., severity levels from a handheld camera](notes/malerbi-2024-handheld-severity-levels.md). Around 90% sensitivity and specificity from one image per eye, judged against three ophthalmologists. **The performance bar I should compare against.**
- **2023** [Penha et al., single image handheld screening](notes/penha-2023-single-image-handheld.md). 93.6% sensitivity but only about 72% specificity. The model was fine-tuned on roughly 16,000 images from the actual device. **Real-world evidence for needing our own fine-tuning.**
- **2022** [Malerbi et al., PhelcomNet on a handheld camera](notes/malerbi-2022-phelcomnet-handheld.md). Ran at the same Itabuna campaign that produced mBRSET, with a model trained only on Eyer images. 97.8% sensitivity, 61.4% specificity. **The direct counterfactual to my study.**
- **2021** [Rogers et al., MAILOR AI study](notes/rogers-2021-mailor-handheld.md). The same AI scored 89.4% on real handheld images versus 98.5% on a desktop-camera benchmark. Advanced disease survived the change, mild disease did not. **Supports gap. Closest published match to my question.**
