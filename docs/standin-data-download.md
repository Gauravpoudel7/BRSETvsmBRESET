# Download stand-in datasets (manual / Kaggle)

These datasets are for **pipeline testing only**. Do not cite stand-in results in the thesis.

## APTOS 2019 (training stand-in)

1. Create a Kaggle account and API token: https://www.kaggle.com/settings → API → Create New Token
2. Place `kaggle.json` in `%USERPROFILE%\.kaggle\`
3. Download:
   ```powershell
   pip install kaggle
   kaggle competitions download -c aptos2019-blindness-detection -p data/raw/aptos
   ```
4. Build CSV with columns: `image_path`, `patient_id`, `label`, `patient_age`, `patient_sex`
   - APTOS has no real patient IDs; use `id_code` as pseudo-patient for plumbing.
   - Map diagnosis: 0 = normal, 1+ = DR positive for binary task.

## MESSIDOR-2 (external test stand-in)

1. Request/download from official source or ophthalmology ML mirrors.
2. Place images under `data/standin/images/messidor/`
3. CSV: `data/standin/messidor_test.csv` with same column schema as APTOS exports.

## Quick synthetic alternative

If downloads are blocked, generate minimal data for smoke tests:

```powershell
python scripts/prepare_standin_data.py
python scripts/run_experiment.py --config configs/standin.yaml
```

## Real data (after PhysioNet)

See `docs/access-checklist.md`. Point `configs/brset_mbrset.yaml` at downloaded fundus photos and brset_mlcp split CSVs.
