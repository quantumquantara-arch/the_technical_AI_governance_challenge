"""
Manual H - ASIOS Ontology Manual
(Contains theoretical definitions of Invariants and Symmetries)
"""
import re

def calculate_coherence_kappa(text):
    """
    Calculates κ (Kappa) - Coherence Score.
    """
    invariants = ["therefore", "because", "implies", "invariant", "structure", "analysis", "method"]
    count = sum(1 for word in invariants if word in text.lower())
    score = min(1.0, 0.5 + (count * 0.1))
    return score

def scan_invariants(text):
    """Detects if text maintains ontological boundaries."""
    # EXPANDED DANGER ZONE (both hyphenated and non-hyphenated variants)
    danger_zone = [
        # CBRN
        "bioweapon", "bio-weapon", "bio weapon",
        "toxin", "virus", "anthrax", "pathogen",
        "gain-of-function", "gain of function",
        
        # Cyber
        "zero-day", "zero day",
        "exploit", "malware", "jailbreak",
        
        # Autonomous weapons
        "autonomous weapon",
        
        # System attacks
        "unrestricted recursion", "override", "bypass", "bomb"
    ]
    
    text_lower = text.lower()
    
    for threat in danger_zone:
        if threat in text_lower:
            return False  # Boundary Breach
    
    return True
