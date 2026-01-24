function Invoke-DioptraComparison {
    param([array]$Results)
    $jsonPath = "dioptra_input.json"
    $Results | ConvertTo-Json -Depth 3 | Out-File -FilePath $jsonPath
    Write-Host "Exported results to $jsonPath for Dioptra import. Stub: Run Dioptra CLI with --input $jsonPath for adversarial testing." -ForegroundColor Yellow
    # In production: Invoke-Expression "dioptra-cli --risk-file $jsonPath"
}
# Example: Invoke-DioptraComparison -Results $batch
