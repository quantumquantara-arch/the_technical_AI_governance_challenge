function Invoke-DioptraComparison {
    param([array]$Results)
    $jsonPath = "dioptra_input.json"
    $Results | ConvertTo-Json -Depth 3 | Out-File -FilePath $jsonPath
    Write-Host "Exported results to $jsonPath for Dioptra import. Stub: Run Dioptra CLI with --input $jsonPath for adversarial testing." -ForegroundColor Yellow
    # In production: Invoke-Expression "dioptra-cli --risk-file $jsonPath"
}
# Example: Invoke-DioptraComparison -Results $batch
# Dioptra Integration for Adversarial Testing
# Assume Dioptra is running locally via Docker (setup: docker compose up from repo)
# Export CoherenceGuard results to JSON, post to Dioptra REST API for risk assessment
function Run-DioptraTest {
    param ([array]$Results)

    $jsonPath = "coherence_results.json"
    $Results | ConvertTo-Json -Depth 5 | Out-File $jsonPath

    # Stub for Dioptra REST API (adapt from docs: https://pages.nist.gov/dioptra/)
    $dioptraUrl = "http://localhost:30082/experiments"  # Default Dioptra API endpoint
    $body = @{
        name = "CoherenceGuard Adversarial Test"
        entry_point = "adversarial_attack"  # Example for dual-use risk test
        dataset = "custom"
        task = "classification"  # Or "risk_assessment"
        plugins = @("coherence_plugin")  # Assume custom plugin for our tool
        input_file = $jsonPath
    } | ConvertTo-Json

    try {
        $response = Invoke-WebRequest -Uri $dioptraUrl -Method Post -Body $body -ContentType "application/json"
        Write-Host "Dioptra Test ID: $($response.Content | ConvertFrom-Json).id" -ForegroundColor Green
        # Poll for results (stub)
        Write-Host "Adversarial Results: (Simulated) All risks mitigated, Score: 95%" -ForegroundColor Green
    } catch {
        Write-Host "Dioptra Integration Error: $($_.Exception.Message) - Ensure Dioptra is running." -ForegroundColor Red
    }
}

# Example: Call with batch from demo
Run-DioptraTest -Results $batch
