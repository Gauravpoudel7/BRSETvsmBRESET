# Synthesis: what the literature says, and whether my question is still open

39 papers reviewed. Written in plain English. Technical terms are explained the first time they appear.

A few words I use throughout:
- **Fundus photo**: a picture of the back of the eye.
- **Diabetic retinopathy**: eye damage caused by diabetes. I shorten it to DR.
- **AUROC** (or AUC): a score for how well a model separates sick from healthy. 1.0 is perfect, 0.5 is a coin flip. A drop of 0.10 is a big deal.
- **Domain shift**: when the pictures a model meets in real life look different from the pictures it learned on. Like training a robot on clear photos, then testing it on blurry ones.
- **Foundation model**: a model trained once on a huge pile of unlabelled pictures, then cheaply adapted to specific jobs.
- **Fine-tuning**: giving an already-trained model extra training on new data.
- **Calibration**: whether a model's stated percentage risk is honest. A model can rank patients well and still quote wildly wrong percentages.

---

## READ THIS FIRST: someone has already run most of my planned experiment

**Yes. I found a paper that does the BRSET to mBRSET generalization test.**

[Li et al. 2026](notes/li-2026-brset-mbrset-foundation-models.md), a medRxiv preprint posted on 20 April 2026 by a group at Aarhus University in Denmark. A preprint is a paper shared publicly before other scientists have formally checked it, so it is not peer reviewed yet.

Here is exactly what they did, next to what I planned to do:

| What I planned | What Li et al. already did |
| --- | --- |
| Train on BRSET, the clinic camera dataset | Yes, all 16,266 images |
| Test on mBRSET, the handheld camera dataset, with no extra training | Yes, all 5,164 images |
| Use pretrained retinal foundation models | Yes: RETFound, VisionFM, DINOv3, plus two RETFound-DINOv2 variants |
| Measure how much performance drops | Yes: AUROC 0.90 to 0.98 on BRSET, falling to 0.70 to 0.85 on mBRSET |
| Split that drop by patient age, sex, education, insurance | **No. They did not do this at all.** |

Their extra findings worth knowing:
- Fine-tuning on mBRSET afterwards won back 0.04 to 0.10 of AUROC. So the problem is fixable with target data.
- DINOv3, a model trained on ordinary everyday photographs, beat both eye-specific models in every setting.
- Every model gave dishonest risk numbers, almost always overstating risk.
- They visualised the models' internal features and found they clustered by camera type, which is direct evidence that the model "sees" which camera took the picture.

**A second paper covers my other half.** [Fernandes et al. 2025](notes/fernandes-2025-disentanglement-shortcuts.md), an arXiv preprint, measures fairness on mBRSET across exactly the traits I care about: age, sex, education, insurance and obesity. It found roughly a 10 percentage point AUROC gap between age groups for one model.

**So the honest position is this.** The two halves of my question have each been answered separately. The camera half is done. The fairness half is done. **Joining them has not been done.** Nobody has asked whether the accuracy lost when you switch cameras is lost evenly across patient groups. That join is what is left of my novelty, and the rest of this document explains why it is still worth doing.

---

## Theme 1: Do models survive a change of camera or dataset?

**Short answer: usually no, and the drop is often large.**

The clearest single number comes from [Rogers et al. 2021](notes/rogers-2021-mailor-handheld.md), the MAILOR study. They took one commercial AI system and ran it on real handheld camera images from a Mexican screening programme, then on a tidy public dataset from a desktop camera. For referable disease, meaning bad enough to need a specialist, it scored 89.4% on handheld versus 98.5% on the desktop benchmark. That gap was statistically real, meaning unlikely to be chance.

The most interesting part of that result is what did **not** drop. Advanced disease, where fragile new blood vessels grow, was detected just as well on handheld images. Only the milder referable cases suffered. [Poyrazer et al. 2026](notes/poyrazer-2026-frozen-foundation-model-transfer.md) found the same pattern much more starkly: moving from Indian to French eye photos, all three models they tested completely failed on mild disease, with two scoring an F1 of exactly 0.000.

This matters practically. A model can look "mostly fine" on an overall score while having quietly lost the ability to catch early disease, which is the entire point of screening.

Why does this happen? [Yang et al. 2020](notes/yang-2020-residual-cyclegan-camera-adaptation.md) showed the camera brand alone is enough to hurt a DR model, even with the same patients and the same disease. Different cameras produce different colour, brightness and sharpness, and the model latches onto those differences.

There are three known fixes, and each is a candidate recommendation for my company:
1. **Repaint the images first.** [Joseph et al. 2025](notes/joseph-2025-universal-cross-camera-adaptation.md) built a step that converts any incoming photo into one consistent style before the AI sees it, with no retraining needed per camera.
2. **Fine-tune on a small batch of your own images.** [Duhaim and Al-Bakry 2026](notes/duhaim-2026-cross-domain-fundus-framework.md) recovered most of a large loss using just 500 labelled images per disease class. That is an affordable amount of data.
3. **Train on many sources at once.** [Men et al. 2025](notes/men-2025-drstagenet-generalization.md) trained across six datasets and improved results on four of five unfamiliar ones.

One paper pushes the other way. [He et al. 2023](notes/he-2023-cross-camera-portable-cameras.md) concluded that using portable cameras with existing algorithms is feasible. I should keep it, because it stops my write-up from being one-sided, but it predates the current generation of models.

## Theme 2: Retinal foundation models, and do they actually generalize better?

**Short answer: this is genuinely contested, and that surprised me.**

[RETFound](notes/zhou-2023-retfound.md), published in Nature in 2023, started this whole field. It learned from 1.6 million unlabelled retinal images by having random patches hidden and guessing what was behind them. Do that millions of times and the model learns what retinas look like without anyone labelling anything.

The critical detail for my study is where those images came from. Overwhelmingly one London hospital, plus one American public dataset. There are no South American images and no handheld camera images in there. So Brazilian handheld photos are unfamiliar to RETFound in two ways at once: the people are different and the device is different.

Since then the family has grown: [VisionFM](notes/qiu-2024-visionfm.md) trained on 3.4 million images across many devices, [FLAIR](notes/silva-rodriguez-2025-flair.md) learned from images plus expert written descriptions, [DINORET](notes/zoellin-2024-block-expanded-dinoret.md) adapted a general-purpose photo model without erasing what it knew, [RETFound-Green](notes/engelmann-2025-retfound-green.md) matched the originals using half the data and 400 times less computing power, and [EyeCLIP](notes/shi-2025-eyeclip.md) added clinical text.

Now the contested part. Does specialising a model on retinas make it more robust, or less?

**Evidence that eye-specific models do NOT help:**
- [Xiong et al. 2025](notes/xiong-2025-foundation-model-generalizability.md) fine-tuned RETFound on Asian patients and found no meaningful advantage over a plain model trained on everyday photographs. This one is co-authored by RETFound's own creators, so it is not an outsider attack.
- [Men et al. 2025](notes/men-2025-drstagenet-generalization.md) ranked RETFound **last** in five of six datasets.
- [Poyrazer et al. 2026](notes/poyrazer-2026-frozen-foundation-model-transfer.md) found RETFound performed below an ordinary ImageNet baseline on external data.
- [Li et al. 2026](notes/li-2026-brset-mbrset-foundation-models.md) found DINOv3, a general-purpose model, beat both eye-specific models on my exact datasets.

**Evidence that they DO help:**
- [Bolo et al. 2026](notes/bolo-2026-retfound-vs-cnn-glaucoma.md) deliberately tested across different cameras and found uncropped RETFound was the **most** robust model, holding its scores while others degraded.
- [Yew et al. 2025](notes/yew-2025-traditional-versus-foundation.md) found RETFound better than traditional models when fine-tuning data was scarce, though it still did not close the ethnic generalisation gap.
- [FLAIR](notes/silva-rodriguez-2025-flair.md) claims strong performance under domain shift, beating both bigger generalist models and retina-specific ones.

Reading this honestly: the answer depends on the task, and on how you preprocess the images. Bolo et al. found something I should take seriously, which is that cropping images helped a conventional model but **hurt** RETFound, because cropping threw away the whole-image patterns RETFound relies on. That means my preprocessing choices could change my conclusion. [RetBench](notes/zou-2025-retbench.md) reached a similar overall verdict: there is no single best eye foundation model, so testing only one would be a weak design.

## Theme 3: Does model performance differ by patient group?

**Short answer: often yes, and specialised medical models may be worse at this, not better.**

The historical anchor is [Burlina et al. 2021](notes/burlina-2021-ai-bias-retinal-diagnostics.md). They deliberately removed all referable-DR training images from darker-skinned patients while still testing on those patients. Accuracy came out at 73.0% for lighter-skinned versus 60.5% for darker-skinned people, a 12.5 point gap. When they filled in the missing group with computer-generated images, the gap fell to 0.5 points. Unequal data produces unequal accuracy, and fixing the data fixes the gap.

The most uncomfortable finding in this theme is from [Khan et al. 2023](notes/khan-2023-fair-medical-foundation-models.md). Models pre-trained on medical images scored **better overall but were consistently less fair** than models pre-trained on ordinary photographs, sometimes even less fair than a model trained from scratch. Every single model they tested underperformed on female patients. This is the fairness twin of the accuracy findings in theme 2, and together they undermine the comfortable assumption that a purpose-built medical model is automatically the responsible choice.

[FairMedFM](notes/jin-2024-fairmedfm.md) tested this at scale across 17 datasets and found bias present across all foundation models and all ways of using them. Worse, existing bias-reduction methods often failed, sometimes improving a fairness score only by sacrificing accuracy. [Fernandes et al. 2025](notes/fernandes-2025-disentanglement-shortcuts.md) saw the same thing on mBRSET, where their bias fix helped one model by 2% but hurt two others by 7% and 3%.

Two papers give me the tools I need:
- [Shi et al. 2025](notes/shi-2025-fair-adaptive-scaling.md) introduced **equity-scaled AUC**, one number that blends overall accuracy with how unequal the subgroups are. That is much easier to report than one overall score plus five subgroup scores.
- [Moya-Sanchez et al. 2025](notes/moya-sanchez-2025-rais-dr.md) used **Disparate Impact** (the ratio of positive decisions between groups, where 1 means equal) and **Equal Opportunity Difference** (the difference in how often disease is correctly caught, where 0 means equal).

That second paper is also a warning against assuming my hypothesis. It found almost no bias across sex and age, with Disparate Impact between 0.984 and 1.031. So "no gap" is a real possible answer for me.

One sobering calibration point from Shi et al.: a purpose-built fairness method only moved scores by about 0.01 to 0.05 AUC. If the gaps I am looking for are that size, I will need proper confidence intervals to say anything at all.

## Theme 4: What has been done with BRSET and mBRSET already?

**Short answer: more than I expected, and mostly by one connected research network.**

[BRSET](notes/nakayama-2024-brset.md) arrived in 2024 with 16,266 photos from 8,524 patients at three Sao Paulo clinics. [mBRSET](notes/wu-2025-mbrset.md) followed in 2025 with 5,164 photos from 1,291 patients, taken with a Phelcom Eyer, a camera that clips onto a Samsung phone, at a community diabetes event in Bahia.

Papers already using them:
- [Li et al. 2026](notes/li-2026-brset-mbrset-foundation-models.md) used **both**, for the cross-camera test described at the top.
- [Fernandes et al. 2025](notes/fernandes-2025-disentanglement-shortcuts.md) used **mBRSET** for subgroup fairness.
- [Queiroz et al. 2024](notes/queiroz-2024-data-efficient-bias.md) used **BRSET** with **RETFound** for a fairness study by age and sex.
- [FairMedFM](notes/jin-2024-fairmedfm.md) includes **BRSET** in a 17-dataset fairness benchmark.
- [Men et al. 2025](notes/men-2025-drstagenet-generalization.md) used the diabetic subset of **BRSET** as an external test domain.
- [Restrepo et al. 2026](notes/restrepo-2026-brset-mbrset-embeddings.md) released precomputed embeddings for **both**, which would let me do subgroup analyses on a laptop.

Two things stand out.

First, **Luis Filipe Nakayama appears as an author on almost all of these.** He is on BRSET, mBRSET, the Fernandes fairness paper, the Queiroz fairness paper, and the Men generalization paper. Joao Matos and Leo Anthony Celi recur too. This is one connected network working steadily through this exact space. The realistic risk is not that my question is uninteresting, it is that this group publishes the combined version before I do. Fernandes et al. is listed as under review, so a peer-reviewed and possibly expanded version may appear soon.

Second, **there is a finding in the mBRSET paper I should treat as a red flag, not a curiosity.** Models could predict a patient's insurance status from their retina photo with an F1 score up to 76.11, and their sex up to 84.38. A model that can read social background off an eye picture may be using that background as a shortcut instead of looking at actual disease. That is exactly the mechanism that would make a cross-camera drop land unevenly across social groups, and it is the strongest theoretical argument for my reframed question.

## Theme 5: Handheld cameras and screening where resources are short

**Short answer: handheld screening works well, but only when the model was trained or fine-tuned on that device's own images.**

This theme produced the most useful pattern in the whole review, and it comes from reading the methods sections rather than the abstracts.

Look at the three Phelcom Eyer studies in order:
- [Malerbi et al. 2022](notes/malerbi-2022-phelcomnet-handheld.md) trained a model **only** on 10,569 Eyer images. Result: 97.8% sensitivity, 61.4% specificity, AUC 0.89. This ran at the same Itabuna campaign that later produced mBRSET.
- [Penha et al. 2023](notes/penha-2023-single-image-handheld.md) trained on the large public EyePACS dataset, then **fine-tuned on about 16,000 Eyer images**. Result: 93.6% sensitivity, about 72% specificity, AUC 0.86.
- [Malerbi et al. 2024](notes/malerbi-2024-handheld-severity-levels.md) again **fine-tuned on portable device images**. Result: about 90% sensitivity and 90% specificity, AUC 0.95 for any DR, judged against three ophthalmologists.

In every case, the people who actually build and sell this camera fine-tuned on their own device's images. None of them trusted a borrowed clinic-camera model as-is. That is real-world behavioural evidence for the answer my company is looking for.

Now compare those numbers with what a borrowed model achieves on the same kind of images. Li et al. got 0.70 to 0.85 AUROC on mBRSET. The device-fine-tuned systems reach 0.86 to 0.95. That gap is roughly the price of not fine-tuning.

The deployment literature says the same thing more bluntly. [Duggal et al. 2025](notes/duggal-2025-real-world-india.md) invited five AI companies to test their products on low-cost camera images in Indian public clinics. One declined, one withdrew partway through after interim results showed poor specificity, and the three that stayed produced specificity anywhere between 14% and 96%. A vendor's published accuracy told you almost nothing about performance on a different device in a different clinic.

The field-level view supports this too. [Wang et al. 2025](notes/wang-2025-regulator-approved-meta-analysis.md) pooled 82 studies covering 887,244 examinations of regulator-approved systems. Pooled accuracy was high, at 0.93 sensitivity and 0.90 specificity. But **only 44% of those studies used a genuinely external test set** from a different country or population. That single statistic is my strongest framing sentence: even approved products are mostly evaluated on data that resembles their training data. [Onyeze et al. 2025](notes/onyeze-2025-lmic-systematic-review.md) searched six databases over ten years for studies in poorer countries and found only a handful qualified. [Grace et al. 2026](notes/grace-2026-lmic-dr-screening-review.md) names data generalisability as one of four main barriers to deployment.

---

## What the two datasets can and cannot tell me

This is the part I would have discovered too late if I had jumped straight into coding. These are facts about BRSET and mBRSET that limit what any study using them can claim.

**1. The two datasets are not paired.** No patient appears in both with two different cameras. They differ in almost everything at once:

| | BRSET | mBRSET |
| --- | --- | --- |
| Where | Sao Paulo clinics, richer Southeast | Itabuna, Bahia, poorer Northeast |
| Setting | Routine eye outpatient visits | A community diabetes campaign |
| Camera | Canon CR2 (65.1%) and Nikon NF5050 (34.9%) | Phelcom Eyer handheld |
| Have diabetes | 16% | 97% |
| Images showing DR | about 7% | about 23% |
| Who graded | One retina specialist | Two ophthalmologists independently |

So if performance drops, **I cannot honestly call that a camera effect.** It could be the different patients, or the different amount of disease, or the different grading. Li et al. say plainly they could not separate these. If I build my thesis on "camera shift" without addressing this, a reviewer will take it apart.

Three ways to reduce the problem, which I should build in from the start:
- Restrict BRSET to its diabetic patients only, so the two groups are more alike. Men et al. already did exactly this, using a diabetic subset of 2,489 images from 1,301 patients.
- Reweight or match so DR prevalence is comparable across the two test sets.
- Use BRSET's **own two cameras** as a control. Comparing Canon against Nikon inside one dataset, with the same patients and the same grader, gives me a clean estimate of what a pure camera change costs. Nothing else in this review does that, and it would be a genuinely new contribution.

**2. The subgroup fields do not match across datasets.** BRSET records age, sex, nationality, insulin use and diabetes duration. Education and insurance exist **only in mBRSET**. So:
- For **age and sex** I can compare the gap in BRSET against the gap in mBRSET, which is the change-in-gap analysis I actually want.
- For **education and insurance** I can only look inside mBRSET. That is still worth doing, because the question "who does a borrowed model fail on in the field" is useful. But it is a different question, and Fernandes et al. have partly covered the within-mBRSET version already.

**3. Some subgroups will be too small to conclude anything.** About 92.3% of mBRSET patients have no health insurance, leaving roughly 100 insured patients out of 1,291. Mean age is 61.4 years, so the under-50 group is also small. With around 1,100 DR-positive images in total, subgroup error bars will be wide. I must report confidence intervals and name the underpowered subgroups as underpowered. Saying so openly is a strength.

**4. There are no race or ethnicity labels.** mBRSET version 1.0 does not include them, and the authors say race may come in a future release. This is genuinely frustrating, because Bahia has a high proportion of Afro-Brazilian and mixed-ancestry people, and Burlina et al. showed pigmentation-related gaps are real. I cannot test that axis and should say so rather than gesture at it.

---

## The reframed question

Given all of the above, here is what I should actually be asking.

**Primary question.** When an off-the-shelf retinal foundation model is moved from clinic-grade fundus camera images to handheld field images, does the loss in accuracy fall evenly on all patients, or does it fall hardest on older, less educated, and uninsured patients?

**Secondary question.** How much of the measured drop is caused by the camera, and how much by the fact that the two patient groups are different? Nobody has separated these, including the paper that already ran the cross-camera test.

Why these two survive the literature:
- Li et al. did the cross-camera test and no fairness analysis.
- Fernandes et al. did the fairness analysis and no cross-camera test.
- Queiroz et al. did fairness with RETFound on BRSET only, by age and sex only.
- Nobody used BRSET's two internal cameras to isolate the camera effect.
- Nobody has asked whether a domain shift changes the size of a fairness gap, in this or any other retinal dataset I found.

That last point is the most defensible framing. The general question "does domain shift widen fairness gaps" appears nowhere in the 39 papers, and there is a clear reason to expect it might. Queiroz et al. showed that making conditions harder, in their case cutting the training data, widened the age gap specifically. Changing the camera is another way of making conditions harder. And the mBRSET paper showed models can read insurance status off a retina photo, which means the shortcuts a model might fall back on when the image looks unfamiliar are socially loaded.

---

## Verdict: is my research question still novel and open?

**My original question is roughly half closed. The reframed version is open.**

Being precise about it:

**Closed.** "Does an AI model trained on clinic-grade cameras generalize to portable handheld cameras, on BRSET and mBRSET, using retinal foundation models?" This is answered by Li et al. 2026. The answer is no, performance falls by 0.12 to 0.25 AUROC, and fine-tuning recovers part of it. I must cite this and cannot present it as my finding. The only softening factors are that it is a preprint, and that its calibration focus means it reported the drop rather than investigating it in depth.

**Open.** "Does that drop fall unevenly across patient subgroups?" I found no paper doing this, in these datasets or any others. This is a real gap with a plausible mechanism behind it.

**Open and under-appreciated.** "How much of the drop is the camera versus the population?" Li et al. named this as their own limitation. Using BRSET's two internal cameras as a control would be a modest but genuinely new methodological contribution.

**Risky.** The BRSET and mBRSET network, centred on Nakayama, is working steadily through this space and Fernandes et al. is under review. There is a real chance the combined study appears within months. I should move quickly and check theme 4 again before submitting anything.

**One expectation I should drop.** I assumed a retina-specialised model like RETFound would be the strong baseline. Four papers here found it transfers worse than general-purpose models, and one found medical pre-training actively harms fairness. Only Bolo et al. found it most robust to camera change. So RETFound should be one model among several in my design, not the centrepiece, and DINOv3 or DINORET may well beat it.

**What would make this hold up to review:**
1. Lead with the fairness question, cite Li et al. for the overall drop, and do not re-litigate it.
2. Control the confound. Restrict BRSET to diabetic patients, match on DR prevalence, and use the Canon versus Nikon comparison as a within-dataset camera control.
3. Test at least three models spanning general-purpose and eye-specific, since RetBench and Li et al. both show no single model wins.
4. Report subgroup results with confidence intervals, use equity-scaled AUC as the headline fairness number, and state plainly which subgroups are too small.
5. Analyse the drop by disease severity, not just overall. Rogers et al. and Poyrazer et al. both found mild disease is where models fail, and mild disease is what screening exists to catch.
6. Say clearly what I cannot study: race and ethnicity are not recorded, and education and insurance are recorded only on the mBRSET side.

Done this way, the study is smaller in headline ambition than I first imagined but much harder to dismiss. It also still answers the product question at work, because the pattern across every handheld study in theme 5 is consistent: the people who build these cameras fine-tune on their own device's images, and the borrowed-model numbers on mBRSET are 0.10 to 0.15 AUROC below the device-fine-tuned ones.
