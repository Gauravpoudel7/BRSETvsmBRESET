# Public pilot study (pre-PhysioNet)

**Purpose:** Validate training, evaluation, bootstrap CIs, and model loading on **public** data before BRSET/mBRSET access.

**This is not the thesis contribution.** Do not report pilot AUROC or fairness numbers as primary findings.

---

## Design

| Component | Stand-in | Thesis target |
| --- | --- | --- |
| Train | APTOS 2019 (Kaggle) | BRSET (clinic cameras) |
| External test | MESSIDOR-2 | mBRSET (Phelcom Eyer handheld) |
| Models | RETFound + DINOv3 (+ timm ViT baseline) | Same |
| Subgroups | Not available in APTOS/MESSIDOR CSVs | Age, sex, education, insurance |

APTOS→MESSIDOR approximates **domain shift** (different source/camera/country) but not Brazil handheld screening or education/insurance fairness.

---

## How to run

### 1. Environment (Python 3.12 + CUDA)

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
python scripts/smoke_test_env.py --model timm
```

### 2. Weights

```powershell
python scripts/download_weights.py --dinov3
python scripts/download_weights.py --retfound --hf-token YOUR_HF_TOKEN
```

RETFound is gated on Hugging Face: https://huggingface.co/YukunZhou/RETFound_mae_natureCFP

### 3. Data

**Recommended (no Kaggle / ADCIS form):**

```powershell
pip install datasets
python scripts/prepare_pilot_hf.py --aptos-max 800 --messidor-max 200
```

Sources: `sngsfydy/aptos_train` (APTOS), `OctoMed/Messidor2` (MESSIDOR, streaming).

**Alternative (Kaggle + ADCIS):**

```powershell
python scripts/download_pilot_data.py
python scripts/prepare_aptos_messidor.py --sample 800
```

### 4. Experiments

```powershell
python scripts/run_experiment.py --config configs/pilot_public_timm.yaml
python scripts/run_experiment.py --config configs/pilot_public_dinov3.yaml
python scripts/run_experiment.py --config configs/pilot_public_retfound.yaml
```

Results under `results/pilot/<model>/`.

---

## What “success” looks like

- Pipeline completes without errors on real fundus images
- External test AUROC computed with bootstrap 95% CIs
- GPU memory and epoch time logged in `run_info.json`
- RETFound/DINOv3 load paths verified (or documented fallback if gated)

---

## Limitations (state in thesis Methods)

1. No education/insurance subgroups in public pilot data
2. Not comparable to Li et al. 2026 numbers (different datasets)
3. Does not answer Phelcom Eyer or Brazil-specific product questions
4. Primary results remain blocked on PhysioNet credentialed access

---

## After PhysioNet approval

Swap to [configs/brset_mbrset.yaml](../configs/brset_mbrset.yaml) — no code rewrite expected.
