# Waits for the MCCV queue to finish, then saves validation predictions for every run
# (for temperature scaling) and rebuilds the full summary.
Set-Location C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
$py = ".\.venv312\Scripts\python.exe"
$root = "C:\data\mccv"; $status = "$root\mccv_status.txt"
while (-not (Select-String -Path $status -Pattern "MCCV all done" -Quiet)) { Start-Sleep 120 }
foreach ($cfg in Get-ChildItem configs\mccv\mccv_r*.yaml | Sort-Object Name) {
  & $py scripts\predict_val.py --config $cfg.FullName *>&1 | Out-File -Append -Encoding utf8 "$root\predict_val.log"
}
& $py scripts\summarize_mccv.py *>&1 | Out-File -Encoding utf8 "$root\summary.log"
"POST (val preds + calibration summary) done $(Get-Date)" | Out-File -Append $status
