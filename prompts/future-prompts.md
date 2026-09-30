# Prompt log

A dated record of every time this literature review is run or extended. The point is that a future session, mine or an AI assistant's, can pick up here without re-reading everything.

---

## 2026-09-01, Initial literature review

**Prompt used (Task section as given):**

> Conduct a structured literature review covering the following themes. For each theme, find the most relevant and most recent (prioritize 2023-2026) papers, and summarize them in plain English following the writing style above.
>
> 1. **Domain/camera generalization in retinal image AI**: models trained on one dataset or camera type losing performance on another (cross-dataset DR grading, camera-type generalization studies e.g. on EyePACS).
> 2. **Retinal foundation models**: RETFound, VisionFM, DINORET, FLAIR, RETFound-Green, and any others, including what they were pretrained on and how they've been evaluated for generalization/external validation.
> 3. **Fairness and demographic bias in retinal/diabetic retinopathy AI**: studies that break down model performance by patient subgroup (age, sex, ethnicity, socioeconomic proxies).
> 4. **BRSET and mBRSET specifically**: the original dataset papers, and any subsequent papers that have used either dataset (especially any that already test a foundation model on BRSET and/or mBRSET, since this directly affects how novel my angle is).
> 5. **Handheld/portable fundus camera AI screening**: studies evaluating AI performance specifically on portable/smartphone-based retinal cameras, and diabetic retinopathy screening deployment in low-resource/LMIC settings generally.
>
> For each paper found, capture: full citation, a 3-5 sentence plain-English summary, what dataset(s)/model(s) it used, its key finding (in plain English), and how it relates to my research question (supports the gap / partially overlaps / directly conflicts, explained simply).

**Covered:** All five themes, 39 papers, notes written for each, `index.md` and `synthesis.md` drafted, `references.bib` built.

**Method note:** Citation metadata (author lists, venues, volumes, pages, years) was pulled programmatically from the Crossref API, the arXiv API, PMLR and PhysioNet rather than typed from memory, so author lists and venues are verified rather than reconstructed. Two papers were checked by reading their full text: Li et al. 2026 and Men et al. 2025.

**Most important thing found:** [Li et al. 2026](../literature-review/notes/li-2026-brset-mbrset-foundation-models.md), a medRxiv preprint posted 20 April 2026, already trains RETFound, VisionFM and DINOv3 on BRSET and tests them on mBRSET. AUROC fell from 0.90 to 0.98 down to 0.70 to 0.85. That is the original research question, already answered. They did **no** demographic subgroup analysis, which is where the remaining novelty sits.

**Second most important:** [Fernandes et al. 2025](../literature-review/notes/fernandes-2025-disentanglement-shortcuts.md) (arXiv:2507.09640) already does subgroup fairness on mBRSET across age, sex, education, insurance and obesity, but only within mBRSET and without any foundation model like RETFound. Listed as under review, so a peer-reviewed version may appear soon.

**Reframing decision made during this session, and why:** Because the plain cross-camera question is closed, the research question was reframed. The fairness question became primary ("does the accuracy loss fall evenly across patients, or hardest on older, less educated and uninsured patients") and the camera-versus-population confound became secondary. Reason: the two halves exist separately in the literature but nobody has joined them, and Li et al. explicitly name the confound as their own unresolved limitation.

**Design constraints discovered (full detail in `synthesis.md`):**
- BRSET and mBRSET are not paired. No patient appears in both. They differ in region, setting, camera, diabetes rate (16% vs 97%), DR rate (about 7% vs about 23%) and grading procedure. A raw drop cannot be called a camera effect.
- BRSET has no education or insurance fields. Those exist only in mBRSET, so change-in-gap analysis is possible for age and sex only.
- About 92.3% of mBRSET patients are uninsured, leaving roughly 100 insured patients. That subgroup will be underpowered.
- mBRSET v1.0 has no race or ethnicity labels, so that axis cannot be studied.
- BRSET's two internal cameras (Canon CR2 at 65.1%, Nikon NF5050 at 34.9%) can serve as a clean within-dataset camera control. No paper in the review does this.

**Follow-up needed:**
1. **Recheck theme 4 before submitting anything.** The Nakayama and Celi network authored BRSET, mBRSET, Fernandes et al., Queiroz et al. and Men et al. They are working steadily through this space and may publish the combined cross-camera fairness study first.
2. **Watch Li et al. 2026.** Check whether it passes peer review and whether the published version adds a subgroup analysis. If it does, the remaining novelty shrinks sharply.
3. **Watch Fernandes et al. 2025.** Check whether the peer-reviewed version extends to cross-camera evaluation.
4. **Check for mBRSET version 2.** The authors said future releases may add self-declared race and more patients. That would open the ethnicity axis.
5. **Not yet reviewed, deliberately deferred:** RetiZero (named as strongest in RetBench external validation but not reviewed here), MedSigLIP (best transfer in Poyrazer et al. but not reviewed), and the RETFound-DINOv2 variants used by Li et al. Add these if the model comparison becomes central.

---

## Reusable prompts for future sessions

### A. Re-run the novelty check only (fast, do this before submitting)

> Search for any paper published or preprinted since September 2026 that uses BOTH the BRSET and mBRSET datasets, or that evaluates a retinal foundation model (RETFound, VisionFM, DINORET, FLAIR, RETFound-Green, RetiZero, DINOv3) across two different fundus camera types AND reports results broken down by patient subgroup (age, sex, education, insurance, race). For each hit, tell me plainly whether it overlaps my reframed question: "when an off-the-shelf retinal model moves from clinic cameras to handheld cameras, does the accuracy loss fall evenly across patient groups?" Check the publication status of medRxiv 2026.04.17.26351092 (Li et al.) and arXiv:2507.09640 (Fernandes et al.), and say whether either has added a subgroup or cross-camera analysis. Do not fabricate. If you cannot verify a paper, say so.

### B. Extend a single theme

> Extend theme <N> of the literature review in `literature-review/`. Read `literature-review/index.md` and `literature-review/synthesis.md` first so you do not duplicate the 39 papers already covered. Add new papers as note files in `literature-review/notes/` using the existing template, add BibTeX entries to `references.bib` with keys matching the filenames, add one plain-English line each to `index.md` in the right theme and year position, and update the relevant theme section of `synthesis.md`. Writing style: short sentences, one idea per sentence, explain every technical term the first time it appears in a file, no em dashes, keep all numbers and names exact. Verify every citation against Crossref or the arXiv API rather than from memory.

### C. Turn the review into a study protocol

> Using `literature-review/synthesis.md`, especially the "What the two datasets can and cannot tell me" and "The reframed question" sections, draft a study protocol for the reframed question. It must include: which models to test and why, the patient-level train/validation/test split, how BRSET will be restricted to diabetic patients and matched on DR prevalence, how the Canon versus Nikon within-BRSET comparison will be used as a camera control, exactly which subgroups will be analysed and which are underpowered, the fairness metrics (subgroup AUROC, equity-scaled AUC, Disparate Impact, Equal Opportunity Difference), how confidence intervals will be computed, and a breakdown of the performance drop by DR severity grade. Same plain-English writing style. State every limitation plainly rather than hiding it.

### D. Convert the synthesis into a scholarship application narrative

> Using `literature-review/synthesis.md`, write a two-page research proposal narrative for a master's scholarship application. Lead with the equity framing (an AI model that fails on handheld cameras fails exactly where eye doctors are scarcest). Be explicit and unembarrassed that Li et al. 2026 already measured the overall drop, and position my contribution as the subgroup and confounding questions they left open. Cite from `references.bib`. Keep the plain-English style, no em dashes, and do not overstate novelty.
