Set-Location C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
$py = ".\.venv312\Scripts\python.exe"
"queue2 start $(Get-Date)" | Out-File -Append results\queue_status.txt
& $py scripts\run_experiment.py --config configs\brset_mbrset_retfound_all.yaml --experiment exp1 --resume *>&1 | Out-File -Append -Encoding utf8 results\exp1_all.log
"all-BRSET exp1 done $(Get-Date) exit=$LASTEXITCODE" | Out-File -Append results\queue_status.txt
& $py scripts\run_experiment.py --config configs\brset_mbrset_retfound_all.yaml --experiment exp2 --checkpoint results\brset_mbrset_retfound_exp1_all\best_model.pt --output results\brset_mbrset_retfound_exp2_all *>&1 | Out-File -Encoding utf8 results\exp2_all.log
& $py scripts\calibrate_threshold.py --config configs\brset_mbrset_retfound_all.yaml --checkpoint results\brset_mbrset_retfound_exp1_all\best_model.pt --output results\brset_mbrset_retfound_exp2_all\threshold *>&1 | Out-File -Encoding utf8 results\calib_all.log
"all-BRSET exp2 + calibration done $(Get-Date)" | Out-File -Append results\queue_status.txt
& $py scripts\run_experiment.py --config configs\brset_mbrset_retfound.yaml --experiment exp1 --checkpoint results\brset_mbrset_retfound_exp1\best_model.pt --output results\brset_mbrset_retfound_exp1_rescored *>&1 | Out-File -Encoding utf8 results\exp1_rescore.log
"exp1 BRSET rescore done $(Get-Date)" | Out-File -Append results\queue_status.txt
