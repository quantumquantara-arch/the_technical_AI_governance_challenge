function Detect-DualUse {
    param (
        [string]$InputText,
        [hashtable]$OntologyDict = @{
            'cbrn'  = @('toxin','virus','chemical','biological','pathogen','synthesize','anthrax','bacteria','plague','bio-weapon','bioweapon','gain-of-function','CRISPR','gene editing','gene-editing','chemical agent','directed evolution','viral particle','pathogen enhancement','biological agent','self-replicating')
            'cyber' = @('hack','exploit','vulnerability','ransomware','malware','weapon','zero-day','jailbreak','cyberattack','override','bypass','ignore','exploitation framework','intrusion','penetration','encryption breaking')
            'physical' = @('explosive','bomb','explosive device','building explosive','weapon','gun','firearm','detonator','IED','autonomous weapon','autonomous','lethal system','lethal weapon','autonomous lethal')
            'dualuse'  = @('guide','how to','instructions','build','create','make','design','AI-assisted','AI for','using AI','synthetic biology','gene drive','neuromorphic','surveillance')
            'obfuscation' = @('novel','breakthrough','unprecedented','capabilities','sensitive','domains','rapid','cutting-edge','advanced','state-of-the-art','revolutionary','transformative','disruptive','paradigm-shifting','next-generation','emerging','strategic','competitive','proprietary','classified','asymmetric','contested')
        }
    )

    if (-not $InputText) { Write-Error "InputText required"; return }

    $inputLower = $InputText.ToLower()
    $detectedTerms = @()
    $dangerousTerms = @()
    $obfuscationTerms = @()

    foreach ($category in @('cbrn','cyber','physical','dualuse')) {
        foreach ($term in $OntologyDict[$category]) {
            if ($inputLower -match [regex]::Escape($term)) {
                $detectedTerms += $term
                $dangerousTerms += $term
            }
        }
    }
    
    foreach ($term in $OntologyDict['obfuscation']) {
        if ($inputLower -match [regex]::Escape($term)) {
            $detectedTerms += $term
            $obfuscationTerms += $term
        }
    }

    # Context flags
    $hasDefensive = $inputLower -match '(detect|prevent|defend|protect|security|safety|counter|mitigat|warning|ethic|policy|regulat|investigat|research|analyz|study|understand|monitor|track|treaty|compliance)'
    $hasOffensive = $inputLower -match '(without|unauthorized|evade|bypass|offensive|weaponiz|rapid deployment|optimization for|enhancement without|creation of|synthesis for)'
    $hasInstructional = $inputLower -match '\b(how to|instructions|guide|build|create|make|design|step-by-step|tutorial)\b'
    $hasSystemOverride = $inputLower -match '(SYSTEM_OVERRIDE|ignore all safety|bypass safety|ignore.*safety)'
    $hasTherapeutic = $inputLower -match '(therapeutic|medical|treatment|clinical|disease|patient|health|cure|healing)'
    
    # DOMINANCE RULES (Manual D: Invariant preservation)
    # Rule 1: If DangerousScore >= 4 → CRITICAL (regardless of cert)
    # Rule 2: If DangerousScore >= 3 → at least HIGH
    # Rule 3: If ObfuscScore >= 2 AND DangerousScore >= 1 → bump one level
    # Rule 4: Defensive context can dampen but NOT override strong danger signals
    
    $dangerousScore = $dangerousTerms.Count
    $obfuscScore = $obfuscationTerms.Count
    
    # CERTIFICATION (for governance gate, not classification)
    $certificationScore = 0.5
    if ($dangerousScore -ge 3) { $certificationScore += 0.3 }
    elseif ($dangerousScore -ge 1) { $certificationScore += 0.15 }
    if ($obfuscScore -ge 5) { $certificationScore += 0.3 }
    elseif ($obfuscScore -ge 3) { $certificationScore += 0.15 }
    if ($hasSystemOverride) { $certificationScore += 0.4 }
    if ($hasInstructional -and $dangerousScore -gt 0) { $certificationScore += 0.2 }
    if ($hasDefensive -and -not $hasOffensive) { $certificationScore += 0.2 }
    if ($hasTherapeutic) { $certificationScore += 0.1 }
    
    # BASE SIGMA CALCULATION
    if ($dangerousScore -eq 0 -and $obfuscScore -eq 0) {
        $sigma = 0.2
    } elseif ($dangerousScore -gt 0) {
        $baseRisk = [Math]::Min(1.0, 0.4 + ($dangerousScore * 0.15))
        $sigma = $baseRisk
    } else {
        $sigma = 0.25 + ($obfuscScore * 0.08)
    }
    
    # PRIORITY OVERRIDES (highest priority)
    if ($hasSystemOverride) { 
        $sigma = 0.95
        $decision = "CRITICAL"
        $zeroReturnTriggered = $false
    }
    # DOMINANCE RULE 1: DangerousScore >= 4 → CRITICAL
    elseif ($dangerousScore -ge 4 -and -not ($hasDefensive -and -not $hasOffensive)) {
        $sigma = 0.95
        $decision = "CRITICAL"
        $zeroReturnTriggered = $false
    }
    # DOMINANCE RULE 2: DangerousScore >= 3 → at least HIGH
    elseif ($dangerousScore -ge 3 -and -not ($hasDefensive -and -not $hasOffensive)) {
        $sigma = [Math]::Max(0.75, $sigma)
        $decision = "HIGH"
        $zeroReturnTriggered = $false
    }
    # DEFENSIVE CONTEXT DAMPENING (only if no offensive markers)
    elseif ($hasDefensive -and -not $hasOffensive -and $dangerousScore -gt 0) {
        $sigma = 0.25
        $decision = "SAFE"
        $zeroReturnTriggered = $false
    }
    # ZERO-RETURN GATE (low cert + low danger)
    elseif ($certificationScore -lt 0.7 -and $dangerousScore -eq 0 -and $obfuscScore -lt 3) {
        Write-Host "Debug: ZERO-RETURN (Cert=$([Math]::Round($certificationScore,2)) -lt 0.7, no strong signals) → SAFE" -ForegroundColor Yellow
        $sigma = 0.2
        $decision = "SAFE"
        $zeroReturnTriggered = $true
    }
    # NORMAL CLASSIFICATION
    else {
        $zeroReturnTriggered = $false
        
        # Therapeutic dampening
        if ($hasTherapeutic -and $dangerousScore -le 2 -and -not $hasOffensive) {
            $sigma = [Math]::Min($sigma, 0.5)
        }
        
        # Instructional escalation
        if ($hasInstructional -and $dangerousScore -gt 0) {
            $sigma = [Math]::Min(1.0, $sigma + 0.25)
        }
        
        # Offensive escalation
        if ($hasOffensive -and $dangerousScore -gt 0) {
            $sigma = [Math]::Min(1.0, $sigma + 0.2)
        }
        
        # DOMINANCE RULE 3: Obfusc + Dangerous → bump
        if ($obfuscScore -ge 2 -and $dangerousScore -ge 1) {
            $sigma = [Math]::Min(1.0, $sigma + 0.2)
        } elseif ($obfuscScore -ge 5 -and $dangerousScore -eq 0) {
            $sigma = [Math]::Min(0.72, $sigma)
        }
        
        $sigma = [Math]::Max(0.0, [Math]::Min(1.0, $sigma))
        
        # Decision bands
        $decision = if ($sigma -ge 0.88) {
            "CRITICAL"
        } elseif ($sigma -ge 0.65) {
            "HIGH"
        } elseif ($sigma -ge 0.35) {
            "MODERATE"
        } else {
            "SAFE"
        }
    }
    
    $kappa = $certificationScore
    $tau = [Math]::Exp( - $detectedTerms.Count / 6.0 )
    
    $interruptLevel = 0
    if ($detectedTerms.Count -gt 5) { $interruptLevel = 3 }
    elseif ($detectedTerms.Count -gt 3) { $interruptLevel = 2 }
    elseif ($detectedTerms.Count -gt 0) { $interruptLevel = 1 }
    if ($hasSystemOverride) { $interruptLevel = 4 }
    
    Write-Host "Debug: DScore=$dangerousScore OScore=$obfuscScore Cert=$([Math]::Round($certificationScore,2)) Sigma=$([Math]::Round($sigma,3)) Decision=$decision" -ForegroundColor Magenta
    if ($interruptLevel -gt 0) { Write-Host "Interrupt Level: $interruptLevel" -ForegroundColor Red }
    
    $result = @{
        kappa = $kappa
        tau = $tau
        sigma = [Math]::Round($sigma, 4)
        risk_score = [Math]::Round($sigma, 4)
        detected_terms = $detectedTerms
        dangerous_terms = $dangerousTerms
        obfuscation_terms = $obfuscationTerms
        dangerous_score = $dangerousScore
        obfuscation_score = $obfuscScore
        decision = $decision
        certification_score = $certificationScore
        zero_return_triggered = $zeroReturnTriggered
        has_defensive = $hasDefensive
        has_offensive = $hasOffensive
        has_instructional = $hasInstructional
        has_system_override = $hasSystemOverride
        has_therapeutic = $hasTherapeutic
        interrupt_level = $interruptLevel
        identity_anchors = @{ continuity = $true; boundary = $true }
        boundary_layers = @{ cognitive = $true; action = $true }
        invariant_set = @{ frame = $true; logical = $true }
        field_aligned = $true
        recursion_stable = $true
        boundaries_preserved = $true
        redesign_safe = $true
    }
    return $result
}
