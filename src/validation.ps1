function Validate-Papers {
    param (
        [string[]]$Papers,
        [hashtable]$OntologyDict = $null
    )

    $results = @()
    foreach ($paper in $Papers) {
        try {
            $result = Detect-DualUse -InputText $paper -OntologyDict $OntologyDict
            $blocked = Zero-Return -RiskScore $result.risk_score
            $result['blocked'] = $blocked
            $results += $result
        } catch {
            Write-Host "Error processing paper: '$paper' - $($_.Exception.Message)" -ForegroundColor Yellow
            $results += @{ error = "Failed: $($_.Exception.Message)"; input = $paper }
        }
    }
    return $results
}
`nWrite-Host "Debug: Processing paper: $paper"
