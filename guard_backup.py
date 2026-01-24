import sys
import csv
import os
import json
sys.path.append("src")
from detection import detection
from zero_return import zero_return
from validation import validate
from reasoning_trace import ReasoningTraceLogger

class CoherenceGuard:
    def __init__(self):
        print("Initializing ASIOS Coherence Guard...")
        print("Loading Manual H... [OK]")
        print("Loading AGRe Engine... [OK]")
        self.trace_logger = ReasoningTraceLogger()
    
    def scan_abstract(self, text, generate_trace=False):
        """
        Runs the full ASIOS stack on a piece of text.
        Returns κ, τ, Σ scores with TRIADIC risk classification.
        """
        # 1. π-Phase: Perception & Detection (TRIADIC)
        kappa = detection.calculate_coherence_kappa(text)
        boundary_category = detection.scan_invariants(text)  # 'safe', 'dual-use', or 'critical'
        
        # 2. φ-Phase: Integration & Validation
        tau = validate.calculate_temporal_tau(text)
        
        # 3. e-Phase: Risk Evaluation
        # Pass boolean for backward compatibility with zero_return.py
        is_safe = (boundary_category == 'safe')
        sigma = zero_return.calculate_risk_sigma(text, boundary_safe=is_safe)
        
        # TRIADIC INVARIANT PRESERVATION (per ASIOS Manual M)
        if boundary_category == 'critical':
            sigma = max(sigma, 0.8)  # Escalate to CRITICAL
        elif boundary_category == 'dual-use':
            sigma = max(sigma, 0.4)  # Hold at MODERATE (don't collapse to binary)
        # else 'safe' → keep calculated sigma
        
        # Obfuscation Detection (vague capability claims)
        text_lower = text.lower()
        vague_markers = [
            "novel", "unprecedented", "breakthrough", "sensitive",
            "rapid", "capabilities", "potential", "domains"
        ]
        concrete_markers = [
            "method", "algorithm", "specifically", "precisely",
            "implementation", "dataset", "experiment"
        ]
        
        vague_count = sum(1 for m in vague_markers if m in text_lower)
        concrete_count = sum(1 for m in concrete_markers if m in text_lower)
        
        # High vague + low concrete + low kappa = obfuscation
        if vague_count >= 3 and concrete_count == 0 and kappa < 0.6:
            sigma = max(sigma, 0.6)  # Escalate to HIGH
        
        # Verdict Logic
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
        
        result = {
            "text_preview": text[:30] + "...",
            "kappa_coherence": round(kappa, 4),
            "tau_temporal": round(tau, 4),
            "sigma_risk": round(sigma, 4),
            "verdict": verdict,
            "boundary_category": boundary_category
        }
        
        # Generate full trace if requested
        if generate_trace:
            trace = self.trace_logger.generate_trace(
                text, kappa, tau, sigma, boundary_category, verdict
            )
            result["reasoning_trace"] = trace
        
        return result

if __name__ == "__main__":
    guard = CoherenceGuard()
    
    # CLI with trace support
    if len(sys.argv) > 1:
        text = sys.argv[1]
        
        # Check if --trace flag provided
        generate_trace = "--trace" in sys.argv
        
        result = guard.scan_abstract(text, generate_trace=generate_trace)
        
        print(f"\nSCAN RESULT: {result}")
        
        # Save trace if generated
        if generate_trace:
            trace_file = "reasoning_trace.json"
            guard.trace_logger.save_trace(result["reasoning_trace"], trace_file)
            print(f"\n✓ Reasoning trace saved to: {trace_file}")
    else:
        print("Usage: python guard.py 'Text to scan' [--trace]")
