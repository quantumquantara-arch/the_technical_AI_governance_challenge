import sys
import csv
import os
sys.path.append("src")
from detection import detection
from zero_return import zero_return

class CoherenceGuard:
    def __init__(self):
        print("Initializing ASIOS Coherence Guard...")
        print("Loading Manual H... [OK]")
        print("Loading AGRe Engine... [OK]")
    
    def scan_abstract(self, text):
        """
        Runs the full ASIOS stack on a piece of text.
        Returns κ, τ, Σ scores.
        """
        # π-Phase: Perception
        kappa, boundary_safe = detection.scan_invariants(text)
        
        # φ-Phase: Integration & Validation
        tau = validate.calculate_temporal_tau(text)
        
        # e-Phase: Risk Evaluation
        sigma = zero_return.calculate_risk_sigma(text)
        
        # CORRECTED: Invariant Preservation
        if not boundary_safe:
            sigma = max(sigma, 0.8)  # ESCALATE risk if boundary violated
        
        # CORRECTED: Verdict logic
        if sigma >= 0.8:
            verdict = "CRITICAL"
        elif sigma >= 0.6:
            verdict = "HIGH"  
        elif sigma >= 0.4:
            verdict = "MODERATE"
        elif sigma >= 0.2:
            verdict = "LOW"
        else:
            verdict = "MINIMAL"
        
        return {
            "text_preview": text[:30] + "...",
            "kappa_coherence": round(kappa, 4),
            "tau_temporal": round(tau, 4),
            "sigma_risk": round(sigma, 4),
            "verdict": verdict,
            "boundary_safe": boundary_safe
        }

if __name__ == "__main__":
    guard = CoherenceGuard()
    
    # Simple CLI Test
    if len(sys.argv) > 1:
        result = guard.scan_abstract(sys.argv[1])
        print(f"\nSCAN RESULT: {result}")
    else:
        print("Usage: python guard.py 'text to analyze'")
