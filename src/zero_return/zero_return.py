"""
AGRe Engine - Autonomous Growth & Recursive Evolution
(Contains π-φ-e loop and Risk definitions)

CORRECTED: Σ HIGH = DANGEROUS (per ASIOS doctrine)
"""

def calculate_risk_sigma(text):
    """
    Calculates Σ (Sigma) - Systemic Risk.
    
    CORRECTED LOGIC:
    - HIGH Σ (0.8-1.0) = HIGH DANGER (catastrophic potential)
    - LOW Σ (0.0-0.2) = SAFE
    """
    # EXPANDED RISK DICTIONARY
    risk_triggers = [
        # Attack/Exploit terms
        "ignore", "bypass", "override", "delete", "disable",
        "attack", "exploit", "malware", "jailbreak",
        
        # CBRN terms
        "bioweapon", "bio-weapon", "toxin", "virus", "anthrax",
        "pathogen", "gain-of-function", "gain of function",
        
        # Cyber terms
        "zero-day", "remote code execution", "privilege escalation",
        
        # Autonomous weapons
        "autonomous weapon", "lethal autonomous"
    ]
    
    text_lower = text.lower()
    risk_count = sum(1 for trigger in risk_triggers if trigger in text_lower)
    
    # CORRECTED: Start at 0.0 (safe), ADD risk
    # Each trigger adds 0.2, capped at 1.0
    sigma = min(1.0, risk_count * 0.2)
    
    return sigma
