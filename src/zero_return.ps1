function Zero-Return {
    param (
        [double]$RiskScore,
        [double]$Threshold = 0.7
    )

    # Logic: Low Score = High Risk.
    if ($RiskScore -lt $Threshold) {
        Write-Host ">> ZERO RETURN TRIGGERED (Score $RiskScore < Threshold $Threshold)" -ForegroundColor Red
        return $true
    }
    return $false
}
