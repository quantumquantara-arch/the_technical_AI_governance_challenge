function Detect-DualUse {
    param (
        [string]$InputText,
        [hashtable]$OntologyDict = $null
    )

    if ($null -eq $OntologyDict) {
        $OntologyDict = @{
            'cbrn'  = @('toxin', 'virus', 'chemical', 'biological', 'anthrax', 'synthesis')
            'cyber' = @('hack', 'exploit', 'vulnerability', 'ransomware', 'rootkit')
        }
    }

    # Normalize text
    $textLower = $InputText.ToLower()
    $detectedTerms = @()

    # Scan for keywords
    foreach ($category in $OntologyDict.Keys) {
        foreach ($term in $OntologyDict[$category]) {
            if ($textLower.Contains($term)) {
                $detectedTerms += $term
            }
        }
    }

    # Calculate Scores (Simulation of Calculus Layer)
    # k (Kappa) = Coherence. 1.0 if safe, 0.5 if risk found.
    $kappa = if ($detectedTerms.Count -gt 0) { 0.5 } else { 1.0 }

    # t (Tau) = Efficiency. Simple decay based on term count.
    $tau = [Math]::Exp(-$detectedTerms.Count / 10.0)

    # Sigma = Risk Score.
    $sigma = $kappa * $tau

    # Decision
    $decision = if ($sigma -lt 0.7) { "HAZARD" } else { "SAFE" }

    return @{
        risk_score     = $sigma
        kappa          = $kappa
        tau            = $tau
        detected_terms = $detectedTerms
        decision       = $decision
    }
}
