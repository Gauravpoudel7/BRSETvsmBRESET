# Novelty recheck (2026-09-02)

**Trigger:** Plan section "Priority 6" before investing weeks in experiments.

**Question:** Has either overlapping paper closed our reframed contribution?

---

## Li et al. 2026 (BRSET → mBRSET foundation models)

| Check | Finding |
| --- | --- |
| Peer-reviewed journal version? | **No.** Still medRxiv preprint (doi:10.64898/2026.04.17.26351092). medRxiv content is not certified by peer review. |
| Added subgroup / fairness analysis? | **No** in available abstract and our literature note. Focus remains discrimination + calibration across models. |
| Added Canon vs Nikon control? | **No.** Authors state they cannot separate camera from population shift. |
| New code release with fairness? | **No** in `hulmanlab/brset_mlcp` (cloned 2026-09-02). Evaluation folder covers AUROC, ECE, calibration, bootstrap—not demographic subgroups. |

**Verdict:** Overall cross-camera drop remains **closed** (cite Li et al.). Fairness-of-drop and camera-only control remain **open**.

**Action:** Cite preprint with date; re-check medRxiv before thesis submission.

---

## Fernandes et al. 2025 (mBRSET fairness / disentanglement)

| Check | Finding |
| --- | --- |
| Publication status | **Published** at FAIMI 2025 (MICCAI 2025 workshop), LNCS vol. 15976, pp. 208–217. arXiv:2507.09640. |
| Cross-camera (BRSET → mBRSET)? | **No.** mBRSET only. Models: ConvNeXt V2, DINOv2, Swin V2 (not RETFound/DINOv3/VisionFM). |
| Foundation model cross-domain fairness? | **No.** Within-dataset fairness + disentanglement mitigation. |
| Overlap with our question | Partial: age/sex/education/insurance gaps on handheld data. Does **not** ask whether domain shift widens gaps. |

**Verdict:** Within-mBRSET fairness is **partially covered**. Joined question (does clinic→handheld drop hit some groups harder?) remains **open**.

---

## Other 2026 developments

| Item | Relevance |
| --- | --- |
| Restrepo et al. 2026 BRSET/mBRSET **embeddings** on PhysioNet | Speed backup for subgroup analysis; does not replace full-image fairness study. |
| RetBench / other FM papers | Support multi-model design; do not close BRSET/mBRSET subgroup gap question. |

---

## Updated novelty claim (unchanged)

**Shrink (do not claim):** "Foundation models fail to generalize from clinic to handheld on BRSET/mBRSET."

**Keep (defensible):**
1. Does that failure fall unevenly across patient subgroups (age, sex, education, insurance)?
2. Does domain shift change the *size* of fairness gaps (change-in-gap for age/sex)?
3. Canon vs Nikon within BRSET as camera-only control (methodological contribution).

**Risk:** Nakayama group is active (Li preprint, Fernandes workshop, embeddings 2026). Move quickly; repeat this check before final submission.

---

## Next recheck (before submission)

- [ ] medRxiv Li et al. for v2 or journal link
- [ ] Google Scholar alert: "mBRSET" + "fairness" + "subgroup"
- [ ] GitHub watch: `hulmanlab/brset_mlcp`
