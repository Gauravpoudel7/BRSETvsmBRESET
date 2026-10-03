Set-Location C:\Users\gaura\OneDrive\Desktop\BRSETvsmBRSET
$py = ".\.venv312\Scripts\python.exe"; $root="C:\data\cohortpool"; $status="$root\status2.txt"
"waiting for baseline $(Get-Date)" | Out-File -Append $status
while (-not (Select-String -Path "$root\status.txt" -Pattern "all done" -Quiet)) { Start-Sleep 60 }
0..4 | % { Remove-Item -Recurse -Force "$root\run_shuf_f$_" -ErrorAction SilentlyContinue }
"baseline done, placeholders removed $(Get-Date)" | Out-File -Append $status
foreach ($t in @('rf_f0','rf_f1','rf_f2','rf_f3','rf_f4','rfw_f0','rfw_f1','rfw_f2','rfw_f3','rfw_f4')) {
  $out="$root\run_$t"
  if (-not (Test-Path "$out\mbrset_external\overall_metrics.json")) {
    "$t start $(Get-Date)" | Out-File -Append $status
    & $py scripts\run_experiment.py --config "configs\cohortpool\cp_$t.yaml" *>&1 | Out-File -Append -Encoding utf8 "$root\$t.log"
    "$t end $(Get-Date) exit=$LASTEXITCODE" | Out-File -Append $status
  }
  & $py scripts\predict_val.py --config "configs\cohortpool\cp_$t.yaml" *>&1 | Out-File -Append -Encoding utf8 "$root\predval2.log"
  "$t predval done $(Get-Date)" | Out-File -Append $status
}
"all done $(Get-Date)" | Out-File -Append $status
