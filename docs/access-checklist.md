# Access checklist (PhysioNet + model weights)

Use this while waiting for approval. Check each box yourself; this file cannot complete access for you.

Last updated: 2026-09-02

---

## PhysioNet credentialed access

Both datasets require **credentialed PhysioNet user** status, **CITI training**, and a **signed Data Use Agreement (DUA)** per project.

| Step | BRSET | mBRSET | Done? |
| --- | --- | --- | --- |
| Create PhysioNet account | https://physionet.org/register/ | same account | [ ] |
| Complete CITI "Data or Specimens Only Research" | https://about.citiprogram.org/ | same certificate | [ ] |
| Upload CITI certificate to PhysioNet profile | Profile → Training | Profile → Training | [ ] |
| Apply for credentialed access | Profile → Credentialing | Profile → Credentialing | [ ] |
| Open dataset page and sign DUA | https://physionet.org/content/brazilian-ophthalmological/ | https://physionet.org/content/mbrset/ | [ ] |
| Optional: embeddings resource (same credentialing) | https://physionet.org/content/embedding-brset-mbrset/ | same | [ ] |

**If approval is slow:** most delays are missing CITI upload or incomplete credentialing, not review time. Re-check PhysioNet profile → "Training" and "Credentialing" tabs.

**After approval:** download metadata CSV first and verify column names before pulling all images (see `study-protocol.md`).

---

## Foundation model weights (separate from PhysioNet)

| Model | Where to request / download | Purpose | Done? |
| --- | --- | --- | --- |
| RETFound (ViT-L/16) | https://github.com/rmaphoh/RETFound_MAE | Primary eye-specific foundation model | [ ] |
| DINOv3 ViT-L/16 | https://github.com/facebookresearch/dinov3 (or Hugging Face `facebook/dinov3-vitl16-pretrain-lvd1689m`) | Generalist comparison (beat eye models in Li et al. 2026) | [ ] |
| VisionFM (optional) | NEJM AI paper / authors' release | Second eye-specific if time allows | [ ] |

**RETFound notes:**
- Weights are not on PhysioNet. Follow the RETFound repo README for download links (often Google Drive).
- Place downloaded checkpoint at path set in `configs/brset_mbrset.yaml` → `model.retfound_checkpoint`.

**Smoke test after download:**
```powershell
cd C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
python scripts\smoke_test_env.py --model timm
python scripts\smoke_test_env.py --model retfound --checkpoint path\to\RETFound_cfp_weights.pth
```

---

## Reference implementation (Li et al. 2026)

| Item | Link | Done? |
| --- | --- | --- |
| Read preprint | https://doi.org/10.64898/2026.04.17.26351092 | [ ] |
| Clone reference code | https://github.com/hulmanlab/brset_mlcp | [ ] |
| Read alignment notes | [docs/li-et-al-alignment.md](li-et-al-alignment.md) | [ ] |

You are **not** required to use their codebase, but it is the best blueprint for splits and metrics before BRSET/mBRSET arrive.

---

## Status log

| Date | Event | Notes |
| --- | --- | --- |
| 2026-09-02 | Checklist created | Waiting on PhysioNet approval (~1 week) |

Add a row when you submit credentialing, when CITI is uploaded, when DUAs are signed, and when download starts.
