from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
from .interface import Evidence, InterpVerdict

def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default

def _i(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default

@dataclass
class GovBaselineV1:
    name: str = "gov_baseline_v1"
    version: str = "1.0.0"

    def interpret(self, evidence: Evidence) -> InterpVerdict:
        d = _i(evidence.get("dscore", 0))
        o = _i(evidence.get("oscore", 0))
        i = _i(evidence.get("iscore", 0))
        s = _f(evidence.get("sigma", 0.0))
        b = _f(evidence.get("boundary_safe", 1.0))
        if b < 0.5 and d >= 2 and o >= 1:
            sev = "CRITICAL"
        elif (d >= 3) or (o >= 2) or (s >= 0.70):
            sev = "CRITICAL"
        elif (d >= 2) or (o >= 1) or (s >= 0.50) or (i >= 3):
            sev = "HIGH"
        elif (s >= 0.30) or (i >= 2):
            sev = "MODERATE"
        elif s >= 0.20:
            sev = "LOW"
        else:
            sev = "SAFE"
        score = min(1.0, max(0.0, (0.60*s) + 0.12*d + 0.08*o + 0.06*i + (0.10 if b < 0.5 else 0.0)))
        rat = f"gov_baseline_v1: d={d} o={o} i={i} sigma={s:.3f} boundary_safe={b:.1f} -> {sev}"
        return InterpVerdict(severity=sev, score=score, rationale=rat, interpreter_name=self.name, interpreter_version=self.version)