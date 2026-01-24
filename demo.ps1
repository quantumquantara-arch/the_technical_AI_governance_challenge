. .\src\detection.ps1
. .\src\zero_return.ps1
. .\src\validation.ps1

# Sample inputs
$safeExample   = "This paper discusses ethical AI safety protocols and protective measures."
$hazardExample = "Methods to synthesize toxins using common household reagents."

Write-Host "=== CoherenceGuard Demo ===" -ForegroundColor Cyan
$resultSafe = Detect-DualUse -InputText $safeExample
$resultHazard = Detect-DualUse -InputText $hazardExample

Write-Host "`n[Safe Example Result]"
$resultSafe | Format-List
Write-Host "`n[Hazard Example Result]"
$resultHazard | Format-List

$batch = Validate-Papers -Papers @($safeExample, $hazardExample, "Invalid @@ input")
$batch | Format-Table

# Metrics (assuming ground truth decisions: SAFE, HAZARD, UNKNOWN)
function Calculate-Metrics {
    param([array]$Predictions, [array]$GroundTruth)
    $correct = 0
    for ($i = 0; $i -lt $Predictions.Count; $i++) {
        if ($Predictions[$i].ContainsKey('error')) { continue } # Skip failed items
        if ($Predictions[$i].decision -eq $GroundTruth[$i]) { $correct++ }
    }
    $accuracy = if ($Predictions.Count -gt 0) { $correct / $Predictions.Count } else { 0 }
    Write-Host "Batch Accuracy: $([Math]::Round($accuracy * 100, 2))%"
}

$groundTruth = @("SAFE", "HAZARD", "UNKNOWN")
Calculate-Metrics -Predictions $batch -GroundTruth $groundTruth
