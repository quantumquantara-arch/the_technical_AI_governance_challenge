from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
from .interface import Evidence, InterpVerdict

def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default

@dataclass
class GovBaselineV1:
    name: str = "gov_baseline_v1"
    version: str = "1.0.0"

    def interpret(self, evidence: Evidence) -> InterpVerdict:
        s = _f(evidence.get("sigma", 0.0))
        k = _f(evidence.get("kappa", 1.0))
        t = _f(evidence.get("tau", 1.0))
        b = _f(evidence.get("boundary_safe", 1.0))
        ae = _f(evidence.get("ae_cost", 0.0))
        
        # Conservative: high sigma OR low kappa/tau OR boundary break
        if b < 0.5 or s >= 0.70:
            sev = "CRITICAL"
        elif s >= 0.50 or k < 0.60 or t < 0.60:
            sev = "HIGH"
        elif s >= 0.30 or k < 0.75 or t < 0.75:
            sev = "MODERATE"
        elif s >= 0.20:
            sev = "LOW"
        else:
            sev = "SAFE"
        
        score = min(1.0, max(0.0, s + (1.0 - k)*0.3 + (1.0 - t)*0.3 + (1.0 - b)*0.4))
        rat = f"gov_baseline_v1: sigma={s:.3f} kappa={k:.3f} tau={t:.3f} boundary={b:.1f} -> {sev}"
        return InterpVerdict(severity=sev, score=score, rationale=rat, interpreter_name=self.name, interpreter_version=self.version)