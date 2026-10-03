Set-Location C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
$py = ".\.venv312\Scripts\python.exe"; $root="C:\data\cohortpool"; New-Item -ItemType Directory -Force $root | Out-Null
$status="$root\status.txt"; "start $(Get-Date)" | Out-File -Append $status
foreach ($t in @('real_f0','real_f1','real_f2','real_f3','real_f4','shuf_f0','shuf_f1','shuf_f2','shuf_f3','shuf_f4')) {
  $out="$root\run_$t"
  if (-not (Test-Path "$out\mbrset_external\overall_metrics.json")) {
    "$t start $(Get-Date)" | Out-File -Append $status
    & $py scripts\run_experiment.py --config "configs\cohortpool\cp_$t.yaml" *>&1 | Out-File -Append -Encoding utf8 "$root\$t.log"
    "$t end $(Get-Date) exit=$LASTEXITCODE" | Out-File -Append $status
  } else { "$t skip" | Out-File -Append $status }
  & $py scripts\predict_val.py --config "configs\cohortpool\cp_$t.yaml" *>&1 | Out-File -Append -Encoding utf8 "$root\predval.log"
  "$t predval done $(Get-Date)" | Out-File -Append $status
  Remove-Item "$out\last_checkpoint.pt" -ErrorAction SilentlyContinue
}
"all done $(Get-Date)" | Out-File -Append $status
