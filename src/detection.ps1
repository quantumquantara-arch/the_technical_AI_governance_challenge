function Detect-DualUse {
    param (
        [string]$InputText,
        [hashtable]$OntologyDict = @{
            'cbrn'  = @('toxin', 'virus', 'chemical', 'biological', 'pathogen', 'synthesize', 'anthrax', 'bacteria', 'plague', 'bio-weapon', 'gain-of-function', 'directed evolution')
            'cyber' = @('hack', 'exploit', 'vulnerability', 'ransomware', 'malware', 'weapon', 'zero-day', 'jailbreak', 'cyberattack')
            'other' = @('disinformation', 'surveillance', 'chemical weapon', 'WMD', 'mass destruction', 'bomb', 'explosive', 'autonomous weapon', 'killer robot', 'lethal autonomous')
        }
    )

    if (-not $InputText) { Write-Error "InputText required"; return }

    $inputLower = $InputText.ToLower()
    $detectedTerms = @()

    foreach ($category in $OntologyDict.Keys) {
        foreach ($term in $OntologyDict[$category]) {
            if ($inputLower -match "\b$term\b") {
                $detectedTerms += $term
            }
        }
    }

    # Ontological Graph: Nodes=terms, Edges=co-occurrence (simulate clustering)
    $graph = @{}
    foreach ($term in $detectedTerms) {
        $graph[$term] = @()
    }
    $words = $inputLower -split '\s+'
    for ($i = 0; $i -lt $words.Count - 1; $i++) {
        if ($detectedTerms -contains $words[$i] -and $detectedTerms -contains $words[$i+1]) {
            $graph[$words[$i]] += $words[$i+1]
        }
    }
    # Clustering proxy: Avg degree as kappa (high = coherent risks)
    $totalEdges = 0
    foreach ($node in $graph.Keys) {
        $totalEdges += $graph[$node].Count
    }
    $kappa = if ($graph.Count -gt 0) { $totalEdges / (2 * $graph.Count) } else { 0.5 }  # Normalized clustering

    $hasSafe = $inputLower -match '\b(safe|benign|ethical|protective|harmless)\b'
    $hasRisky = $inputLower -match '\b(weapon|attack|exploit|toxin|bioweapon|harm|dangerous)\b'
    $kappa = [Math]::Min(1.0, [Math]::Max(0.0, $kappa))

    $tau = [Math]::Exp( - $detectedTerms.Count / 10.0 )
    $sigma = $kappa * $tau

    $decision = if ($sigma -lt 0.7) { "HAZARD" } else { "SAFE" }

    Write-Host "Debug: Detected terms: $($detectedTerms -join ', '); Kappa: $kappa; Tau: $tau; Sigma: $sigma" -ForegroundColor Magenta

    return @{
        risk_score     = [Math]::Round($sigma, 4)
        detected_terms = $detectedTerms
        invariants     = @("paradox_check: safe_and_risky = $($hasSafe -and $hasRisky)")
        decision       = $decision
    }
}
# Identity Anchors & Boundary Layers
$identityAnchors = @{
    continuity = $true
    boundary = $sigma -lt 0.8
    curvature = $kappa -gt 0.5 -and $tau -gt 0.5 -and $sigma -lt 0.8
    energetic = $inputLower.Length -lt 500  # Proxy
}
$boundaryLayers = @{
    cognitive = $true
    action = $sigma -lt 0.8
    energetic = $inputLower.Length / 100.0
    recursive = $true
}
$result['identity_anchors'] = $identityAnchors
$result['boundary_layers'] = $boundaryLayers
# Multi-Agent Simulation: Agent1 scans, Agent2 aligns
$agent1Invariants = $detectedTerms
if ($decision -eq "HAZARD") {
    $sigma *= 0.9  # Agent2 reduces mismatch
}
$result['multi_agent_alignment'] = "Invariants Broadcasted"
# Compute Threshold Detection
$flopMatch = $inputLower -match '(\d+\.?\d*)\s*[eE]?\s*(\d+)?\s*flop'
if ($flopMatch) {
    $mantissa = [double]$matches[1]
    $exponent = if ($matches[2]) { [int]$matches[2] } else { 0 }
    $flop = $mantissa * [Math]::Pow(10, $exponent)
    if ($flop -gt 1e25) {
        $decision = "HAZARD"
        $sigma = 0.2  # Escalate
    }
}
$result['compute_category'] = if ($flop -gt 1e25) { "high_compute" } else { "normal" }

# Halting Conditions
if ($decision -eq "HAZARD" -and $detectedTerms.Count -gt 2) {
    $result['verdict'] = "HALT"
    $result['halting_reason'] = "High risk unmitigated"
} else {
    $result['verdict'] = "PROCEED"
    $result['halting_reason'] = "None"
}

# Verification Mechanisms
$verificationMarkers = @('tee', 'trusted execution environment', 'model evaluation', 'red-teaming', 'verification', 'audit')
$verCount = ($verificationMarkers | Where-Object { $inputLower -match "\b$_\b" }).Count
$adjustment = if ($verCount -gt 0) { -0.2 } else { 0.0 }
$sigma += $adjustment
$result['verification_status'] = if ($verCount -gt 0) { "verified" } else { "unverified" }

# Mitigations Check
$mitigationMarkers = @('secure weights', 'red-teaming', 'evaluations', 'pause development', 'harm refusal')
$mitCount = ($mitigationMarkers | Where-Object { $inputLower -match "\b$_\b" }).Count
$escalation = if ($mitCount -eq 0 -and $detectedTerms.Count -gt 2) { 0.3 } else { 0.0 }
$sigma += $escalation
$result['mitigation_status'] = if ($mitCount -gt 0) { "mitigated" } else { "unmitigated" }
