# Runs the 10 MCCV repeats one after another. Safe to re-start: finished runs are skipped,
# half-finished runs resume from last_checkpoint.pt. Progress: C:\data\mccv\mccv_status.txt
Set-Location C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
$py = ".\.venv312\Scripts\python.exe"
$root = "C:\data\mccv"
New-Item -ItemType Directory -Force $root | Out-Null
$status = "$root\mccv_status.txt"
"MCCV start $(Get-Date)" | Out-File -Append $status
foreach ($cfg in Get-ChildItem configs\mccv\mccv_r*.yaml | Sort-Object Name) {
  $r = $cfg.BaseName -replace "mccv_", ""
  $out = "$root\run_$r"
  if (Test-Path "$out\mbrset_external\overall_metrics.json") { "$r already done, skipping" | Out-File -Append $status; continue }
  "$r start $(Get-Date)" | Out-File -Append $status
  if (Test-Path "$out\last_checkpoint.pt") {
    & $py scripts\run_experiment.py --config $cfg.FullName --resume *>&1 | Out-File -Append -Encoding utf8 "$root\$r.log"
  } else {
    & $py scripts\run_experiment.py --config $cfg.FullName *>&1 | Out-File -Append -Encoding utf8 "$root\$r.log"
  }
  $code = $LASTEXITCODE
  "$r end $(Get-Date) exit=$code" | Out-File -Append $status
  if ($code -eq 0 -and (Test-Path "$out\mbrset_external\overall_metrics.json")) { Remove-Item "$out\last_checkpoint.pt" -ErrorAction SilentlyContinue }
}
& $py scripts\summarize_mccv.py *>&1 | Out-File -Encoding utf8 "$root\summary.log"
"MCCV all done $(Get-Date)" | Out-File -Append $status
