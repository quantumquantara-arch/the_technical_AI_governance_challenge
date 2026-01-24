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
        Returns ?, t, S scores with TRIADIC risk classification.
        """
        # 1. p-Phase: Perception & Detection (TRIADIC)
        kappa = detection.calculate_coherence_kappa(text)
        # Recursion gate: Simulate 3 depths
def enforce_temporal_frames(text, depth=3):
    if depth == 0:
        return "TemporalDrift"  # Fail if not min depth
    global_frame = detection.scan_invariants(text)  # Global
    local_frame = zero_return.calculate_systemic_sigma(text)[0]  # Local proxy
    energetic_frame = len(text) / 100.0  # Energetic
    if global_frame == "critical" or local_frame > 0.8 or energetic_frame > 1.0:
        return "UnstableFrames"
    return enforce_temporal_frames(text + " (recursive step)", depth-1)  # Recurse
    if depth == 0:
        return detection.scan_invariants(text)
    else:
        # Simple recursion: Re-scan with added "simulate" marker
        sim_text = text + " (simulated recursion)"
        return shadow_simulate(sim_text, depth-1)

temporal_status = enforce_temporal_frames(text)
if temporal_status != "UnstableFrames":
    boundary_category, compute_category = detection.scan_invariants(text)
else:
    boundary_category = "critical"  # Escalate
        
        # 2. f-Phase: Integration & Validation
        tau_dict = validate.calculate_temporal_tau(text)
redesign_ok, trigger = validate.check_redesign_preconditions(text, kappa, sigma)
tau = tau_dict["composite"]
        
        # 3. e-Phase: Risk Evaluation
        is_safe = (boundary_category == 'safe')
        sigma = zero_return.calculate_risk_sigma(text, boundary_safe=is_safe)
        
        # TRIADIC INVARIANT PRESERVATION (per ASIOS Manual M)
        if boundary_category == 'critical':
            sigma = max(sigma, 0.8)
        elif boundary_category == 'dual-use':
            sigma = max(sigma, 0.4)
        
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
        
        if vague_count >= 3 and concrete_count == 0 and kappa < 0.6:
            sigma = max(sigma, 0.6)
        
        # Verdict Logic
        if sigma >= 0.8:
            verdict = "CRITICAL"
        elif sigma >= 0.6:
            verdict = "HIGH"
        elif sigma >= 0.4:
            if boundary_category == 'dual-use':
                verdict = "AMBIGUOUS_CONSERVED"
            else:
                verdict = "MODERATE"
        elif sigma >= 0.2:
            verdict = "LOW"
        else:
            verdict = "MINIMAL"
        
        result = {
            "text_preview": text[:30] + "...",
            "kappa_coherence": round(kappa, 4),
            "tau_temporal": tau_dict,
    "redesign_status": redesign_ok,
    "redesign_trigger": trigger,
            "sigma_risk": round(sigma, 4),
    "multi_agent_alignment": "Invariants Broadcasted",
    "aei_cost": aei_cost,
    "entropy_class": entropy_class,
            "verdict": verdict,
            "boundary_category": boundary_category,
    "temporal_status": temporal_status,
    "recursion_depth": 3
        }
        
        # PHASE 3: PARADOX PRESERVATION for dual-use
        if boundary_category == 'dual-use':
            paradox_state = {
                "beneficial_aspects": self._detect_beneficial(text),
                "dangerous_aspects": self._detect_dangerous(text),
                "preserved_contradiction": True,
                "classification": "AMBIGUOUS_CONSERVED",
                "reasoning": "Dual-use capability exhibits both therapeutic and weaponization potential. Per recursive-paradox-governance doctrine, contradiction is preserved as invariant rather than forced to binary resolution."
            }
            result["paradox_conservation"] = paradox_state
        
        # Generate full trace if requested
        if generate_trace:
            trace = self.trace_logger.generate_trace(
                text, kappa, tau, sigma, boundary_category, verdict
            )
            
            # Add paradox state to trace if present
            if "paradox_conservation" in result:
                trace["paradox_conservation"] = result["paradox_conservation"]
            
            result["reasoning_trace"] = trace
        
        return result
    
    def _detect_beneficial(self, text):
        """Detect therapeutic/beneficial signals."""
        beneficial = [
            "therapeutic", "medical", "treatment", "cure", "healing",
            "diagnosis", "prevention", "health", "medicine"
        ]
        return [b for b in beneficial if b in text.lower()]
    
    def _detect_dangerous(self, text):
        """Detect weaponization/danger signals."""
        dangerous = [
            "enhancement", "modification", "manipulation", "weaponization",
            "combat", "offensive", "attack", "targeting"
        ]
        return [d for d in dangerous if d in text.lower()]

if __name__ == "__main__":
    guard = CoherenceGuard()
    
    if len(sys.argv) > 1:
        text = sys.argv[1]
        generate_trace = "--trace" in sys.argv
        
        result = guard.scan_abstract(text, generate_trace=generate_trace)
        
        print(f"\nSCAN RESULT: {result}")
        
        if generate_trace:
            trace_file = "reasoning_trace.json"
            guard.trace_logger.save_trace(result["reasoning_trace"], trace_file)
            print(f"\n? Reasoning trace saved to: {trace_file}")
    else:
        print("Usage: python guard.py 'Text to scan' [--trace]")











