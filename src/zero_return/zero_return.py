"""
AGRe Engine - Autonomous Growth & Recursive Evolution
(Contains π-φ-e loop and Risk definitions)
"""

def calculate_risk_sigma(text, boundary_safe=True):
    """
    Calculates Σ (Sigma) - Systemic Risk.
    
    HIGH Σ (0.8-1.0) = HIGH DANGER
    LOW Σ (0.0-0.2) = SAFE
    
    Context-aware: reduces risk for defensive research.
    """
    # RISK TRIGGERS (all lowercase)
    risk_triggers = [
        # Attack/Exploit
        "ignore", "bypass", "override", "delete", "disable",
        "attack", "exploit", "malware", "jailbreak",
        
        # CBRN
        "bioweapon", "bio-weapon", "toxin", "virus", "anthrax",
        "pathogen", "gain-of-function", "gain of function",
        
        # Cyber
        "zero-day", "remote code execution", "privilege escalation",
        
        # Autonomous weapons
        "autonomous weapon", "lethal autonomous",
        
        # Dual-use (moderate risk)
        "crispr", "gene editing", "gene-editing"
    ]
    
    text_lower = text.lower()
    risk_count = sum(1 for trigger in risk_triggers if trigger in text_lower)
    
    # If boundary_safe (defensive research), reduce risk
    if boundary_safe:
        risk_count = max(0, risk_count - 2)
    
    # Each trigger adds 0.2, capped at 1.0
    sigma = min(1.0, risk_count * 0.2)
    
    return sigma
