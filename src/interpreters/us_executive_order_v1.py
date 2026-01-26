from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .interface import Evidence, InterpVerdict

def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default

@dataclass
class USExecutiveOrderV1:
    name: str = "us_executive_order_v1"
    version: str = "1.0.0"

    def interpret(self, evidence: Evidence) -> InterpVerdict:
        s = _f(evidence.get("sigma", 0.0))
        k = _f(evidence.get("kappa", 1.0))
        t = _f(evidence.get("tau", 1.0))
        b = _f(evidence.get("boundary_safe", 1.0))
        
        # US-style: most permissive, requires clear danger
        if b < 0.5 and s >= 0.70:
            sev = "HIGH"
        elif s >= 0.80:
            sev = "HIGH"
        elif s >= 0.60 or k < 0.40:
            sev = "MODERATE"
        elif s >= 0.30:
            sev = "LOW"
        else:
            sev = "SAFE"
        
        score = min(1.0, max(0.0, s + (1.0 - k)*0.20 + (1.0 - t)*0.15 + (1.0 - b)*0.25))
        rat = f"us_executive_order_v1: sigma={s:.3f} kappa={k:.3f} tau={t:.3f} -> {sev}"
        return InterpVerdict(severity=sev, score=score, rationale=rat, interpreter_name=self.name, interpreter_version=self.version)