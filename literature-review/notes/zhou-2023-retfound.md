# A foundation model for generalizable disease detection from retinal images (RETFound)

**Citation:** Zhou Y, Chia MA, Wagner SK, Ayhan MS, Williamson DJ, Struyven RR, Liu T, Xu M, Lozano MG, Woodward-Court P, Kihara Y, et al.; UK Biobank Eye and Vision Consortium; Keane PA. A foundation model for generalizable disease detection from retinal images. Nature. 2023;622(7981):156-163. doi: 10.1038/s41586-023-06555-x. Venue: Nature. **Peer reviewed.**
**Year:** 2023
**Dataset(s) used:** 1.6 million unlabelled retinal images for pre-training, made up of colour fundus photographs and optical coherence tomography scans, drawn mainly from Moorfields Eye Hospital data plus public sources. Downstream evaluation on multiple public disease datasets.
**Model(s)/method(s):** Self-supervised learning with a masked autoencoder on a Vision Transformer backbone, then fine-tuning for specific tasks

## Summary (plain English)
This is the paper that introduced RETFound, the model at the centre of my study. A "foundation model" is trained once on a huge pile of unlabelled pictures, then adapted cheaply to many specific jobs. The training trick was masked autoencoding: hide random patches of an eye photo and make the model guess what was hidden. Doing that millions of times forces it to learn what healthy and unhealthy retinas generally look like, without anyone labelling anything. After that, a small amount of labelled data is enough to fine-tune it for a task like grading diabetic retinopathy, which is eye damage caused by diabetes.

## Key finding (plain English)
Pre-training on a large pile of unlabelled retinal images produced a model that adapts to many eye and body-wide disease tasks using far fewer labels than training from scratch would need.

## Relevance to my research (plain English)
**Foundational.** This defines what I am testing. The critical detail for my question is where the pre-training images came from: overwhelmingly a London hospital, plus a US public dataset. As other papers note, the colour fundus portion was 904,170 images with about 90% from the Moorfields dataset and the rest from Kaggle EyePACS. There are no South American images and no handheld camera images in there. So Brazilian handheld photos are doubly unfamiliar to this model, in both population and device. That is the exact reason my study is worth running, and it is also why I should not be shocked if RETFound underperforms.
