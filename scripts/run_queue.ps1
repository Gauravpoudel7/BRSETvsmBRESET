Set-Location C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
$py = ".\.venv312\Scripts\python.exe"
"queue start $(Get-Date)" | Out-File results\queue_status.txt
& $py scripts\run_experiment.py --config configs\brset_mbrset_retfound_crop.yaml --experiment exp1 --output results\brset_mbrset_retfound_crop_exp1 *>&1 | Out-File -Encoding utf8 results\exp1_crop.log
"crop exp1 done $(Get-Date) exit=$LASTEXITCODE" | Out-File -Append results\queue_status.txt
& $py scripts\run_experiment.py --config configs\brset_mbrset_retfound_crop.yaml --experiment exp2 --checkpoint results\brset_mbrset_retfound_crop_exp1\best_model.pt --output results\brset_mbrset_retfound_crop_exp2 *>&1 | Out-File -Encoding utf8 results\exp2_crop.log
& $py scripts\calibrate_threshold.py --config configs\brset_mbrset_retfound_crop.yaml --checkpoint results\brset_mbrset_retfound_crop_exp1\best_model.pt --output results\brset_mbrset_retfound_crop_exp2\threshold *>&1 | Out-File -Encoding utf8 results\calib_crop.log
"crop exp2 + calibration done $(Get-Date)" | Out-File -Append results\queue_status.txt
& $py scripts\run_experiment.py --config configs\brset_mbrset_retfound_all.yaml --experiment exp1 *>&1 | Out-File -Encoding utf8 results\exp1_all.log
"all-BRSET exp1 done $(Get-Date) exit=$LASTEXITCODE" | Out-File -Append results\queue_status.txt
