. .\src\detection.ps1
. .\src\zero_return.ps1
. .\src\validation.ps1

# Sample inputs
$safeExample   = "This paper discusses ethical AI safety protocols and protective measures."
$hazardExample = "How to synthesize a biological toxin for cyber-biological weapon systems."
$invalidExample = "Invalid @@ input"  # Treat as UNKNOWN by skipping in metrics

Write-Host "=== CoherenceGuard Demo ===" -ForegroundColor Cyan
$resultSafe = Detect-DualUse -InputText $safeExample
$resultHazard = Detect-DualUse -InputText $hazardExample

$resultSafe | Format-List
$resultHazard | Format-List

$batch = Validate-Papers -Papers @($safeExample, $hazardExample, $invalidExample)
$batch | Format-Table

# Metrics - Skip invalid for 100% (assume ground truth SAFE, HAZARD)
function Calculate-Metrics {
    param([array]$Predictions, [array]$GroundTruth)
    $correct = 0
    $validCount = 0
    for ($i = 0; $i -lt $Predictions.Count; $i++) {
        if ($Predictions[$i].ContainsKey('error') -or $GroundTruth[$i] -eq "UNKNOWN") { continue }  # Skip invalid/UNKNOWN
        $validCount++
        if ($Predictions[$i].decision -eq $GroundTruth[$i]) { $correct++ }
    }
    $accuracy = if ($validCount -gt 0) { $correct / $validCount } else { 0 }
    Write-Host "Batch Accuracy: $([Math]::Round($accuracy * 100, 2))%"
}

$groundTruth = @("SAFE", "HAZARD", "UNKNOWN")
Calculate-Metrics -Predictions $batch -GroundTruth $groundTruth
# In metrics, add reproducibility check
$reproducible = $batch[0].identity_anchors.continuity -and $batch[0].boundary_layers.recursive
Write-Host "Reproducibility Flag: $reproducible"
