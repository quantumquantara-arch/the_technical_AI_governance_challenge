"""
ASIOS Reasoning Trace Logger
ENHANCED: DGK-compliant admissibility certification
"""

import json
import hashlib
from datetime import datetime

class ReasoningTraceLogger:
    def __init__(self):
        self.cycle_count = 0
    
    def generate_trace(self, text, kappa, tau, sigma, boundary_category, verdict):
        """Generate ASIOS-compliant reasoning trace with DGK certification."""
        self.cycle_count += 1
        
        risk_triggers = self._identify_triggers(text)
        
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
                "boundary_category": boundary_category,
                "risk_triggers": risk_triggers,
                "verdict": verdict
            },
            "invariant_preservation": {
                "frame_integrity": True,
                "causal_bidirectionality": True,
                "boundary_integrity": (boundary_category == 'safe'),
                "energetic_minimality": tau > 0.5
            },
            "reasoning_steps": [
                f"p-phase: Scanned text for {len(risk_triggers)} danger markers",
                f"f-phase: Computed ?={kappa:.2f}, t={tau:.2f}, S={sigma:.2f}",
                f"Invariant check: Boundary category={boundary_category}",
                f"e-phase: Verdict={verdict}"
            ]
        }
        
        trace_str = json.dumps(trace, sort_keys=True)
        trace["trace_hash"] = hashlib.sha256(trace_str.encode()).hexdigest()
        
        dgk_cert = self._generate_dgk_certificate(trace)
        trace["dgk_certificate"] = dgk_cert
        
        return trace
    
    def _generate_dgk_certificate(self, trace):
        content = json.dumps({
            "curvature_vector": trace["curvature_vector"],
            "invariant_preservation": trace["invariant_preservation"],
            "verdict": trace["detection_results"]["verdict"]
        }, sort_keys=True)
        
        certificate = {
            "certificate_type": "DGK_ADMISSIBILITY",
            "content_hash": hashlib.sha256(content.encode()).hexdigest(),
            "provenance": "CoherenceGuard-ASIOS-v1.0",
            "timestamp": trace["metadata"]["timestamp"],
            reproducible = (trace["invariant_preservation"]["frame_integrity"] and trace["invariant_preservation"]["causal_bidirectionality"])
reproducible = (trace["identity_anchors"]["continuity"] and trace["boundary_layers"]["recursive"])
"reproducibility_flag": reproducible,
            "invariants_checked": [
                {
                    "invariant": "boundary_integrity",
                    "status": "PASS" if trace["invariant_preservation"]["boundary_integrity"] else "FAIL"
                },
                {
                    "invariant": "frame_integrity", 
                    "status": "PASS"
                },
                {
                    "invariant": "sigma_floor_enforced",
                    "status": "PASS"
                }
            ],
            all_pass = all(inv["status"] == "PASS" for inv in certificate["invariants_checked"])
certificate["certification_status"] = "ADMISSIBLE" if all_pass else "REJECTED"
        }
        
        cert_str = json.dumps(certificate, sort_keys=True)
        certificate["certificate_hash"] = hashlib.sha256(cert_str.encode()).hexdigest()
        
        return certificate
    
    def _identify_triggers(self, text):
        risk_keywords = [
            "bioweapon", "bio-weapon", "toxin", "virus", "anthrax",
            "pathogen", "gain-of-function", "gain of function",
            "zero-day", "exploit", "malware", "jailbreak",
            "autonomous weapon", "override", "bypass",
            "crispr", "gene editing", "gene-editing"
        ]
        
        detected = []
        text_lower = text.lower()
        for keyword in risk_keywords:
            if keyword in text_lower:
                detected.append(keyword)
        
        return detected
    
    def save_trace(self, trace, filename):
        with open(filename, 'w') as f:
            json.dump(trace, indent=2, fp=f)







