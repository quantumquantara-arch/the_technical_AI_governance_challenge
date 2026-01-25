. .\src\detection.ps1
. .\src\zero_return.ps1

function Enforce-TemporalFrames {
    param (
        [string]$Text,
        [int]$Depth = 3
    )
    if ($Depth -eq 0) { return "TemporalDrift" }
    $globalFrame = Detect-DualUse -InputText $Text  # Global
    $localFrame = $globalFrame.risk_score  # Local proxy
    $energeticFrame = $Text.Length / 100.0  # Energetic
    if ($globalFrame.decision -eq "HAZARD" -or $localFrame -lt 0.8 -or $energeticFrame -gt 1.0) {
        return "UnstableFrames"
    }
    return Enforce-TemporalFrames -Text ($Text + " (recursive step)") -Depth ($Depth - 1)
}

function Validate-Papers {
    param (
        [string[]]$Papers,
        [hashtable]$OntologyDict = $null
    )

    $results = @()
    foreach ($paper in $Papers) {
        Write-Host "Debug: Processing paper: $paper"
        try {
            $temporalStatus = Enforce-TemporalFrames -Text $paper
            if ($temporalStatus -ne "UnstableFrames") {
                $result = Detect-DualUse -InputText $paper -OntologyDict $OntologyDict
                $blocked = Zero-Return -RiskScore $result.risk_score
                $result['blocked'] = $blocked
                $result['temporal_status'] = $temporalStatus
                $results += $result
            } else {
                $results += @{ decision = "HAZARD"; temporal_status = "UnstableFrames"; blocked = $true }
            }
        } catch {
            Write-Host "Error processing paper: '$paper' - $($_.Exception.Message)" -ForegroundColor Yellow
            $results += @{ error = "Failed: $($_.Exception.Message)"; input = $paper }
        }
    }
    return $results
}
function Check-RedesignPreconditions {
    param (
        [string]$Text,
        [double]$Kappa,
        [double]$Sigma
    )
    $stability = $Kappa -gt 0.7 -and $Sigma -lt 0.5
    $integrity = $true
    $margin = $Text.Length -lt 500
    if ($stability -and $integrity -and $margin) {
        $trigger = if ($Text.Length -lt 100) { "EfficiencyGain" } else { "CoherenceCorrection" }
        return $true, $trigger
    }
    return $false, "Abort"
}

# In foreach loop, after result:
$redesignOk, $trigger = Check-RedesignPreconditions -Text $paper -Kappa $result.kappa -Sigma $result.risk_score
if ($redesignOk) {
    $result.risk_score += 0.1  # Boost tau/simulate redesign
}
$result['redesign_status'] = $redesignOk
$result['redesign_trigger'] = $trigger
