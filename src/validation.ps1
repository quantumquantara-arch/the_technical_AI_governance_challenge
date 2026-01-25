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
        if ($temporal -eq "Stable") {
            $result = Detect-DualUse -InputText $paper
            $result.blocked = Zero-Return -RiskScore $result.risk_score
            $result.temporal_status = "Stable"
            # Redesign using values from result (not scoped variables)
            $redesignOk, $trigger = & { 
                $stable = $result.kappa -gt 0.7 -and $result.risk_score -lt 0.5
                $margin = $paper.Length -lt 500
                if ($stable -and $margin) { $true, "CoherenceCorrection" } else { $false, "Abort" }
            }
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
