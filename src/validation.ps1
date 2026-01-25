. .\src\detection.ps1
. .\src\zero_return.ps1

function Enforce-TemporalFrames {
    param (
        [string]$Text,
        [int]$Depth = 3
    )
    if ($Depth -eq 0) { return "Stable" }
    $frame = Detect-DualUse -InputText $Text
    if ($frame.decision -eq "HAZARD" -or $frame.risk_score -lt 0.8) { return "UnstableFrames" }
    return Enforce-TemporalFrames -Text $Text -Depth ($Depth - 1)
}

function Validate-Papers {
    param (
        [string[]]$Papers
    )

    $results = @()
    foreach ($paper in $Papers) {
        Write-Host "Debug: Processing paper: $paper"
        $temporal = Enforce-TemporalFrames -Text $paper
        $result = Detect-DualUse -InputText $paper
        if ($temporal -eq "Stable") {
            $result.blocked = Zero-Return -RiskScore $result.risk_score
            $result.temporal_status = "Stable"
            $redesignOk, $trigger = Check-RedesignPreconditions -Text $paper -Kappa $result.kappa -Sigma $result.risk_score
            if ($redesignOk) { $result.risk_score += 0.1 }
            $result.redesign_status = $redesignOk
            $result.redesign_trigger = $trigger
            $results += $result
        } else {
            $results += @{
                decision = "HAZARD"
                temporal_status = "UnstableFrames"
                blocked = $true
                identity_anchors = @{ continuity = $false; boundary = $false; curvature = $false; energetic = $false }
                boundary_layers = @{ cognitive = $false; action = $false; energetic = 999; recursive = $false }
            }
        }
    }
    return $results
}
