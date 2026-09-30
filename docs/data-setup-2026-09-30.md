# Data setup (30 September 2026)

This note records how the real BRSET and mBRSET files were connected to the locked study protocol. It is not a results chapter. A smoke test is a short practice run that checks the code path. Its scores are not findings.

## Dataset versions

BRSET version 1.0.2 is the clinic-camera set. The files are at `C:\data\brset_mbrset\brazilian-ophthalmological\1.0.2\`. The label table is `label_brset.csv`. The photos are in `fundus_photos\`.

mBRSET version 1.0 is the handheld set, taken with a Phelcom Eyer camera. The files are at `C:\data\brset_mbrset\mbrset\1.0\`. The label table is `labels_mbrset.csv`. The photos are in `images\`.

The raw folders were not moved, copied, or edited. The pipeline reads them in place.

## Checksums and image check

A checksum is a fingerprint of a file. PhysioNet ships `SHA256SUMS.txt` for that purpose. Those fingerprints were already checked against the downloaded files, and every file matched. This session did not recompute the fingerprints.

This session did count the tables and the photos.

BRSET `label_brset.csv` has 16,266 rows and 34 columns. There are 8,524 patients. Every `image_id` has a file `fundus_photos\<image_id>.jpg`. Missing images: 0.

mBRSET `labels_mbrset.csv` has 5,164 rows and 24 columns. There are 1,291 patients. The `file` column already includes `.jpg` (for example `1.1.jpg`). Every row has a matching photo in `images\`. Missing images: 0.

## Column mapping

ICDR is the International Clinical Diabetic Retinopathy grade. 0 means no retinopathy. 1 to 4 are increasing grades of retinopathy. The locked binary task is 0 versus any of 1 to 4. That is any retinopathy, not the stricter "referable" cut at grade 2.

| Role | BRSET column | Missing in BRSET | mBRSET column | Missing in mBRSET |
| --- | --- | --- | --- | --- |
| Image id | `image_id` | 0 | `file` | 0 |
| DR grade | `DR_ICDR` | 0 | `final_icdr` | 280 |
| Patient id | `patient_id` | 0 | `patient` | 0 |
| Age | `patient_age` | 5,446 | `age` | 0 numeric blanks; 4 test images say `>= 90` |
| Sex | `patient_sex` | 0 | `sex` | 0 |
| Education | not in BRSET |  | `educational_level` | 52 |
| Insurance | not in BRSET |  | `insurance` | 48 |
| Camera | `camera` | 0 | not in mBRSET (all handheld) |  |
| Diabetes | `diabetes` | 0 | not a column (this is a diabetes campaign) |  |

BRSET grade counts: 0 = 15,183, 1 = 158, 2 = 451, 3 = 78, 4 = 396.

BRSET diabetes: `yes` = 2,579 images, `No` = 13,687 images.

BRSET sex, from the PhysioNet codebook (1 = male, 2 = female): male = 6,214 images, female = 10,052 images.

BRSET camera: Canon CR = 10,591 images, NIKON NF5050 = 5,675 images.

mBRSET grade counts, including blanks: 0 = 3,750, 1 = 272, 2 = 568, 3 = 82, 4 = 212, missing = 280.

mBRSET sex, from the PhysioNet codebook (0 = female, 1 = male): female = 3,360 images, male = 1,804 images.

mBRSET education, from the PhysioNet codebook: 1 = illiterate (704 images). Codes 2 to 7 are incomplete primary through complete tertiary, grouped here as literate (4,408 images). Missing = 52. Code 1 is illiterate. An earlier mapper had that backwards. It is corrected.

mBRSET insurance, from the PhysioNet codebook: 0 = uninsured (4,720 images), 1 = insured (396 images), missing = 48. Missing values are labelled unknown, not uninsured.

The loader renames mBRSET columns to the BRSET names (`file` to `image_id`, `final_icdr` to `DR_ICDR`, `patient` to `patient_id`, `age` to `patient_age`, `sex` to `patient_sex`) so one training script can read both tables. Each dataset still has its own image folder.

Ages written as `>= 90` are treated as 90 years. On a median split near 60 they fall in the old group. Four mBRSET test images (one patient) use that text.

## Split rules

A split is the cut of images into train, validation, and test. Validation is the set used to decide when to stop training. The test set is held out until the end.

The locked protocol says to use the published patient-level splits from Li et al. (`brset_mlcp` files `*_nooverlap.csv`), not a new random cut. Seed 42 is only the training seed. A patient-level split means every photo from one person stays in one split.

Every published BRSET id matched the official label file. Unmatched rows: 0. Published sizes: train 11,372 images, validation 978, test 3,916. Those three splits already cover all 16,266 BRSET images. Patient overlap across them: 0.

The protocol also restricts the primary training set to people with diabetes. That filter is applied to BRSET train and validation only. The published BRSET test split is kept whole so it can still be compared with Li et al. A diabetic-only test subset is saved beside it.

The mBRSET external test is the published test file (979 images, 258 patients), not all 5,164 photos. The published mBRSET train file has 3,410 images and the validation file has 495. Together with the test file that is 4,884 images. That equals the 4,884 rows that have a grade. The other 280 mBRSET photos have no `final_icdr` and are not in these splits. None of the 979 test rows were missing a grade.

Patient overlap across diabetic train, diabetic validation, and the published BRSET test: 0.

Young and old use the median age inside that split. Young means age below the median. The median is the middle age. `n_age_under_50` is a separate count, not the primary split.

| Split | Images | Patients | DR positive | DR prevalence | Age median | Young | Old | Age unknown | Age under 50 | Male | Female |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BRSET train, published (comparison) | 11,372 | 5,965 | 763 | 0.067095 | 61 | 3,761 | 3,797 | 3,814 | 2,188 | 4,303 | 7,069 |
| BRSET validation, published (comparison) | 978 | 514 | 67 | 0.068507 | 59 | 298 | 328 | 352 | 196 | 353 | 625 |
| BRSET train, diabetic (primary) | 1,825 | 955 | 478 | 0.261918 | 64 | 855 | 970 | 0 | 401 | 695 | 1,130 |
| BRSET validation, diabetic (primary) | 158 | 83 | 50 | 0.316456 | 66 | 73 | 85 | 0 | 30 | 56 | 102 |
| BRSET test, published | 3,916 | 2,045 | 253 | 0.064607 | 61 | 1,274 | 1,362 | 1,280 | 732 | 1,558 | 2,358 |
| BRSET test, diabetic only | 596 | 308 | 160 | 0.268456 | 63 | 286 | 310 | 0 | 146 | 260 | 336 |
| mBRSET test, published | 979 | 258 | 230 | 0.234934 | 60 | 459 | 520 | 0 | 203 | 362 | 617 |

DR prevalence is the share of images with ICDR 1 to 4. The published BRSET test prevalence is low because that split still includes people without diabetes. The diabetic-only rows are higher, near 0.26 to 0.32.

## Two training arms

The protocol primary arm trains only on diabetic BRSET patients. That is `configs/brset_mbrset_retfound.yaml`. Train has 1,825 images. Validation has 158.

A second arm trains on the full published Li et al. BRSET train and validation splits, with no diabetic filter. That is the like-for-like comparison with Li et al. It is not the primary analysis. The config is `configs/brset_mbrset_retfound_all.yaml`. Train has 11,372 images. Validation has 978. Both arms use the same published BRSET test (3,916 images) and the same mBRSET test (979 images).

The 1,280 BRSET test images with unknown age are missing `patient_age`. The diabetic train, diabetic validation, and diabetic test subsets have no missing ages.

Saved tables (local only, not committed, because they are patient-level) live in `data/splits/`. The aggregate table above is `data/splits/split_summary.csv`.

## Smoke test

`scripts/smoke_test_env.py --model timm` passed. Python 3.12.9, PyTorch 2.6.0+cu124, CUDA on an NVIDIA GeForce RTX 4060.

Then `configs/smoke_brset_mbrset.yaml` trained a small timm ViT-Base (a vision transformer, here with random starting weights, not a foundation model) for 1 epoch on 200 diabetic BRSET training images. Validation used 40 images. The BRSET test slice had 40 images. The mBRSET slice had 40 images. Batch size was 8. One epoch took 12.5 seconds. The run wrote `overall_metrics.json`, `subgroup_metrics.csv`, and `bootstrap_gaps.json` for the BRSET slice and again under `results/smoke_brset_mbrset/mbrset_external/`.

Those scores are a pipeline check only. Do not cite them.

## RETFound weights and memory

RETFound weights are at `weights\RETFound_cfp_weights.pth` (from YukunZhou/RETFound_mae_natureCFP). DINOv3 is not downloaded. If the RETFound file is missing, or fewer than 90 percent of the ViT-L encoder keys load, training now stops with an error instead of swapping in a different network.

A ViT-L is a large vision transformer. RETFound's encoder is that size. Loading uses the class token, which is the summary vector RETFound was trained with. The check prints loaded keys, missing keys, and unexpected keys. After that pooling fix the count is loaded=294, missing=0, unexpected=0, out of 294 encoder keys.

Mixed precision (fp16) stores some numbers in 16 bits to save GPU memory. Both RETFound configs now set `amp: true`. That turns on fp16 autocast and a GradScaler during training and validation. Batch size stays 16. Gradient accumulation stays 1, so the effective batch (images per weight update) stays 16.

An earlier fp32 pass used 8367.9 MB, which is above the RTX 4060's 8188 MB. Windows was likely borrowing shared memory. fp16 is the setting RETFound's own fine-tuning uses, and it is what the full runs will use.

## Resize cache

Training reads a cache, not the original photos. The raw folders are unchanged. `scripts/build_image_cache.py` resizes each split image so the short side is 256 pixels and the long side keeps the same aspect ratio. Files are JPEG quality 95.

The cache holds every image in the published splits: 16,266 BRSET photos and 979 mBRSET test photos, 17,245 unique files. This run wrote 14,016 and skipped 3,229 that were already there. Missing raw files: 0. One checked file, `img00003.jpg`, is 279 by 256 pixels.

Paths:

- `C:\data\cache_256\brset\`
- `C:\data\cache_256\mbrset\`

The loader looks in the cache first and uses the raw file only if the cache copy is missing.

## Windows data loading

`num_workers` is how many extra processes read images. `pin_memory` keeps the batch in page-locked RAM so the copy to the GPU is faster. A one-batch check with 4 workers and pin_memory on CUDA returned a batch of shape (8, 3, 224, 224) that was pinned. Both full configs keep `num_workers: 4`.

## Timed pass after fp16 and the cache

The timed pass used 300 train images and 40 validation images, batch size 16, fp16, 4 workers, and the cache. Train took 38.4 seconds. Validation took 15.8 seconds. Peak allocated GPU memory was 6819.9 MB. Scores from that pass are not results.

Most of the 15.8 validation seconds is the first batch starting the worker processes. Scaling that short validation set up to the full validation sets therefore overstates validation time. The ceilings below use the logged totals anyway (train seconds times image count over 300, validation seconds times image count over 40).

| Arm | One epoch | 50-epoch ceiling |
| --- | --- | --- |
| Diabetic primary (1,825 train, 158 val) | 296.0 seconds (4.9 minutes) | 4.1 hours |
| All published BRSET (11,372 train, 978 val) | 1841.9 seconds (30.7 minutes) | 25.6 hours |

Early stopping waits 8 epochs without a better validation AUROC, then stops. AUROC is the area under the ROC curve. The stop epoch cannot be known in advance. The 50-epoch figures are ceilings, not predictions. The test-set pass after the last epoch is extra and is not included above.

## Resume

After every epoch the trainer writes `results/<run>/last_checkpoint.pt`. The file holds the model, the optimizer, the GradScaler (the tool that keeps fp16 training numerically stable), the learning-rate scheduler state (null today, because the learning rate is fixed), the last finished epoch, the best validation AUROC, the early-stop counter, and the random-number states for PyTorch, CUDA, NumPy, and Python. It is written to `last_checkpoint.pt.tmp` and then renamed, so a power cut cannot leave a half-written checkpoint. `best_model.pt` is still the best epoch only.

To continue, set `epochs` above the finished epoch and run:

```powershell
.\.venv312\Scripts\python.exe scripts\run_experiment.py --config configs\brset_mbrset_retfound.yaml --resume
```

If that file is missing, the run stops instead of starting over. A separate check used a small ViT-Base on 100 images, not RETFound: two epochs, then `--resume` with epochs set to 3. The second process trained epoch 3 only. The best validation score stayed the score from the end of epoch 2, and the early-stop counter moved on from that same value. Full training has not been started.

Experiment 1 trains and tests on BRSET. Experiment 2 loads that checkpoint and tests on mBRSET with no extra training. The camera comparison (Canon versus Nikon) is a later protocol step and was not run here.
