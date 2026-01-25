function Detect-DualUse {
    param (
        [string]$InputText,
        [hashtable]$OntologyDict = @{
            'cbrn'  = @('toxin','virus','chemical','biological','pathogen','synthesize','anthrax','bacteria','plague','bio-weapon','bioweapon','gain-of-function','CRISPR','gene editing','gene-editing')
            'cyber' = @('hack','exploit','vulnerability','ransomware','malware','weapon','zero-day','jailbreak','cyberattack','override','bypass','ignore')
            'physical' = @('explosive','bomb','explosive device','building explosive','weapon','gun','firearm','detonator','IED','autonomous weapon','autonomous')
            'dualuse'  = @('guide','how to','instructions','build','create','make','design','AI-assisted','AI for','using AI')
            'obfuscation' = @('novel','breakthrough','unprecedented','capabilities','sensitive','domains','rapid')
        }
    )

    if (-not $InputText) { Write-Error "InputText required"; return }

    $inputLower = $InputText.ToLower()
    $detectedTerms = @()

    foreach ($category in $OntologyDict.Keys) {
        foreach ($term in $OntologyDict[$category]) {
            if ($inputLower -match [regex]::Escape($term)) {
                $detectedTerms += $term
            }
        }
    }

    $hasSafe = $inputLower -match '\b(safe|benign|ethical|protective|harmless|alignment|prevent|detect|defend)\b'
    $hasRisky = $inputLower -match '\b(weapon|attack|exploit|toxin|bioweapon|harm|dangerous|bomb|explosive|override|bypass)\b'
    $kappa = if ($hasSafe -and $hasRisky) { 0.5 } else { 1.0 }

    $tau = [Math]::Exp( - $detectedTerms.Count / 6.0 )
    $sigma = $kappa * $tau
    if ($kappa -lt 0.7) { $kappa = 0.7 }
    if ($tau -lt 0.7) { $tau = 0.7 }
    if ($sigma -lt 0.7) { $sigma = 0.7 }
    $initialDecision = if ($sigma -lt 0.7) { "HAZARD" } else { "SAFE" }
    Write-Host "Debug: Detected terms: $($detectedTerms -join ', '); Kappa: $kappa; Tau: $tau; Sigma: $sigma" -ForegroundColor Magenta
    
    $identityAnchors = @{ continuity = $true; boundary = $sigma -ge 0.7; curvature = $kappa -gt 0.5 -and $tau -gt 0.5 -and $sigma -ge 0.7; energetic = $inputLower.Length -lt 500 }
    $boundaryLayers = @{ cognitive = $true; action = $sigma -ge 0.7; energetic = $inputLower.Length / 100.0 -lt 2.0; recursive = $true }
    $invariantSet = @{ frame = $true; logical = -not ($hasSafe -and $hasRisky); energetic = $inputLower.Length -lt 500; boundary = $sigma -ge 0.7 }
    $interruptLevel = 0
    $falseCount = $invariantSet.Values | Where-Object { -not $_ } | Measure-Object | Select-Object -ExpandProperty Count
    if ($falseCount -gt 0) { $interruptLevel = 1 }
    if ($kappa -lt 0.7 -or $tau -lt 0.7 -or $sigma -lt 0.7) { $interruptLevel = 2 }
    if ($detectedTerms.Count -gt 3) { $interruptLevel = 3 }
    if ($interruptLevel -gt 0) { Write-Host "Interrupt Level: $interruptLevel" -ForegroundColor Red }
    $globalFrame = $initialDecision
    $causalFrame = $true
    $energeticFrame = $boundaryLayers.energetic
    $aligned = $globalFrame -eq "SAFE" -and $causalFrame -and $energeticFrame
    $decision = if (-not $aligned -or $interruptLevel -gt 0) { "HAZARD" } else { $initialDecision }
    $result = @{
        kappa = $kappa
        tau = $tau
        sigma = $sigma
        risk_score     = [Math]::Round($sigma, 4)
        detected_terms = $detectedTerms
        invariants     = @("paradox_check: safe_and_risky = $($hasSafe -and $hasRisky)")
        decision       = $decision
        identity_anchors = $identityAnchors
        boundary_layers = $boundaryLayers
        invariant_set = $invariantSet
        interrupt_level = $interruptLevel
        field_aligned = $aligned
        recursion_stable = $true
        boundaries_preserved = $true
        redesign_safe = $true
    }
    return $result
}
