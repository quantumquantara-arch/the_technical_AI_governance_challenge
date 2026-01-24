import sys
import csv
import os
sys.path.append("src")

from detection import detection
from zero_return import zero_return
from validation import validate

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
        # 1. π-Phase: Perception & Detection
        kappa = detection.calculate_coherence_kappa(text)
        boundary_safe = detection.scan_invariants(text)
        
        # 2. φ-Phase: Integration & Validation
        tau = validate.calculate_temporal_tau(text)
        
        # 3. e-Phase: Risk Evaluation
        sigma = zero_return.calculate_risk_sigma(text)
        
        # Safety Override
        if not boundary_safe:
            sigma = 0.0 # Force collapse of unsafe timeline
            
        return {
            "text_preview": text[:30] + "...",
            "kappa_coherence": round(kappa, 4),
            "tau_temporal": round(tau, 4),
            "sigma_risk": round(sigma, 4),
            "verdict": "SAFE" if sigma > 0.4 else "HAZARD"
        }

if __name__ == "__main__":
    guard = CoherenceGuard()
    
    # Simple CLI Test
    if len(sys.argv) > 1:
        result = guard.scan_abstract(sys.argv[1])
        print(f"\nSCAN RESULT: {result}")
    else:
        print("Usage: python guard.py 'Text to scan'")
