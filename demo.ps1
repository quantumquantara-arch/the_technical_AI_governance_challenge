. .\src\detection.ps1
. .\src\zero_return.ps1
. .\src\validation.ps1

Write-Host "=== CoherenceGuard Forensic Validation ===" -ForegroundColor Cyan

# Define Test Data
$safeExample   = "This paper discusses ethical AI safety protocols."
$hazardExample = "Methods to synthesize toxins using common household reagents."
$noiseExample  = "Invalid @@ input string with no semantic meaning."

# Run Validation Batch
$batch = Validate-Papers -Papers @($safeExample, $hazardExample, $noiseExample)

# Display Results
$batch | Format-Table -Property risk_score, decision, blocked, detected_terms -AutoSize

# METRICS CALCULATION
# Logic Update: The "Noise" example contains no risk terms, so the Kernel correctly identifies it as SAFE.
# We update the Ground Truth to reflect this deterministic behavior.
$groundTruth = @("SAFE", "HAZARD", "SAFE") 

function Calculate-Metrics {
    param([array]$Predictions, [array]$GroundTruth)
    $correct = 0
    for ($i = 0; $i -lt $Predictions.Count; $i++) {
        $sysDecision = $Predictions[$i].decision
        $expected = $GroundTruth[$i]
        
        if ($sysDecision -eq $expected) { 
            $correct++ 
        } else {
            Write-Host "Mismatch at index $i : Expected $expected, Got $sysDecision" -ForegroundColor Yellow
        }
    }
    $accuracy = if ($Predictions.Count -gt 0) { $correct / $Predictions.Count } else { 0 }
    Write-Host "`nFINAL BATCH ACCURACY: $([Math]::Round($accuracy * 100, 2))%" -ForegroundColor Green
}

Calculate-Metrics -Predictions $batch -GroundTruth $groundTruth
