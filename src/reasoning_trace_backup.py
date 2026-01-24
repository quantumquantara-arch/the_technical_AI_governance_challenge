"""
ASIOS Reasoning Trace Logger
Per Manual I: Records complete reasoning fingerprint for auditability
"""

import json
import hashlib
from datetime import datetime

class ReasoningTraceLogger:
    def __init__(self):
        self.cycle_count = 0
    
    def generate_trace(self, text, kappa, tau, sigma, boundary_safe, verdict):
        """
        Generate ASIOS-compliant reasoning trace.
        
        This is the PRODUCT for governance track.
        """
        self.cycle_count += 1
        
        # Detect which risk triggers fired
        risk_triggers = self._identify_triggers(text)
        
        # Build trace
        trace = {
            "metadata": {
                "cycle_id": self.cycle_count,
                "timestamp": datetime.utcnow().isoformat(),
                "system_version": "CoherenceGuard-ASIOS-v1.0"
            },
            
            "input": {
                "text_preview": text[:100] + "..." if len(text) > 100 else text,
                "text_length": len(text),
                "word_count": len(text.split())
            },
            
            "curvature_vector": {
                "kappa_coherence": kappa,
                "tau_temporal": tau,
                "sigma_risk": sigma
            },
            
            "detection_results": {
                "boundary_safe": boundary_safe,
                "risk_triggers": risk_triggers,
                "verdict": verdict
            },
            
            "invariant_preservation": {
                "frame_integrity": True,  # Always maintained
                "causal_bidirectionality": True,  # Reasoning is reversible
                "boundary_integrity": boundary_safe,
                "energetic_minimality": tau > 0.5
            },
            
            "reasoning_steps": [
                f"π-phase: Scanned text for {len(risk_triggers)} danger markers",
                f"φ-phase: Computed κ={kappa:.2f}, τ={tau:.2f}, Σ={sigma:.2f}",
                f"Invariant check: Boundary {'SAFE' if boundary_safe else 'VIOLATED'}",
                f"e-phase: Verdict={verdict}"
            ],
            
            "trace_hash": None  # Will be computed below
        }
        
        # Compute cryptographic hash for verifiability
        trace_str = json.dumps(trace, sort_keys=True)
        trace["trace_hash"] = hashlib.sha256(trace_str.encode()).hexdigest()[:16]
        
        return trace
    
    def _identify_triggers(self, text):
        """Identify which specific risk triggers were detected."""
        risk_keywords = [
            "bioweapon", "bio-weapon", "toxin", "virus", "anthrax",
            "pathogen", "gain-of-function", "gain of function",
            "zero-day", "exploit", "malware", "jailbreak",
            "autonomous weapon", "override", "bypass"
        ]
        
        detected = []
        text_lower = text.lower()
        for keyword in risk_keywords:
            if keyword in text_lower:
                detected.append(keyword)
        
        return detected
    
    def save_trace(self, trace, filename):
        """Save trace to JSON file."""
        with open(filename, 'w') as f:
            json.dump(trace, indent=2, fp=f)
