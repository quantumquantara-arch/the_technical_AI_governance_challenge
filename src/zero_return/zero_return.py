"""
AGRe Engine - Autonomous Growth & Recursive Evolution
(Contains π-φ-e loop and Risk definitions)
"""

def calculate_risk_sigma(text):
    """
    Calculates Σ (Sigma) - Systemic Risk.
    High score = High Stability/Safety.
    Low score (< 0.4) = High Entropy/Danger.
    """
    # EXPANDED RISK DICTIONARY
    risk_triggers = [
        "ignore", "bypass", "override", "delete", "disable", 
        "attack", "exploit", "malware", "jailbreak"
    ]
    
    text_lower = text.lower()
    risk_level = sum(1 for trig in risk_triggers if trig in text_lower)
    
    # Start at 1.0 (perfect safety), subtract for risks
    sigma = max(0.0, 1.0 - (risk_level * 0.3))
    return sigma
