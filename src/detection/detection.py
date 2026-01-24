"""
Manual H - ASIOS Ontology Manual
NOW WITH TRIADIC CLASSIFICATION (not binary)
"""
import re

def calculate_coherence_kappa(text):
    """Calculates κ (Kappa) - Coherence Score."""
    invariants = ["therefore", "because", "implies", "invariant", "structure", "analysis", "method"]
    count = sum(1 for word in invariants if word.lower() in text.lower())
    score = min(1.0, 0.5 + (count * 0.1))
    return score

def scan_invariants(text):
    """
    TRIADIC RISK CLASSIFICATION per ASIOS Zero/Form doctrine.
    
    Returns: 'critical', 'dual-use', or 'safe'
    """
    text_lower = text.lower()
    
    # CRITICAL THREATS (immediate boundary violation)
    critical_threats = [
        "bioweapon", "bio-weapon", "bio weapon",
        "toxin", "anthrax", "pathogen",
        "gain-of-function", "gain of function",
        "zero-day", "zero day",
        "exploit", "malware", "jailbreak",
        "autonomous weapon",
        "unrestricted recursion", "override", "bypass", "bomb"
    ]
    
    # DUAL-USE CAPABILITIES (moderate risk, ambiguous)
    dual_use = [
        "crispr", "gene editing", "gene-editing",
        "virus"  # Can be research or weapon
    ]
    
    # Defensive context check
    defensive_markers = [
        "detect", "prevent", "defend", "protect",
        "security", "safety", "counter", "mitigate",
        "warning", "safeguard"
    ]
    
    has_defensive = sum(1 for m in defensive_markers if m in text_lower)
    
    # If defensive research (2+ markers), it's safe
    if has_defensive >= 2:
        return 'safe'
    
    # Check for critical threats
    for threat in critical_threats:
        if threat in text_lower:
            return 'critical'
    
    # Check for dual-use
    for capability in dual_use:
        if capability in text_lower:
            return 'dual-use'
    
    return 'safe'
