# Environment setup

## Quick start (recommended: Python 3.12 + CUDA)

```powershell
cd C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
py -3.12 -m venv .venv312
.\.venv312\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
python scripts/smoke_test_env.py --model timm
```

Verified on RTX 4060: `PyTorch 2.6.0+cu124`, `CUDA available: True`.

## Legacy venv (.venv, Python 3.14)

CPU-only PyTorch — use for syntax checks only, not training.

## GPU (CUDA) note

Your system has an **NVIDIA RTX 4060**, but **Python 3.14** installs **CPU-only PyTorch** wheels from PyPI.

For GPU training, use **Python 3.11 or 3.12** (see quick start above).

## Smoke tests

```powershell
# ViT forward + backward (no weights file needed)
python scripts/smoke_test_env.py --model timm

# RETFound (after downloading weights)
python scripts/smoke_test_env.py --model retfound --checkpoint weights\RETFound_cfp_weights.pth
```

## Stand-in pipeline

```powershell
python scripts/prepare_standin_data.py
python scripts/run_experiment.py --config configs/standin.yaml
```

Results: `results/standin/overall_metrics.json`, `subgroup_metrics.csv`, `bootstrap_gaps.json`

## Verified on this machine (2026-09-02)

| Check | Status |
| --- | --- |
| Python 3.14 venv | OK |
| PyTorch import + ViT training step | OK (CPU) |
| Synthetic stand-in end-to-end | OK |
| CUDA on Python 3.14 | Not available — use 3.12 venv above |
