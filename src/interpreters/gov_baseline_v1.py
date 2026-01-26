from __future__ import annotations

from typing import Any, Dict

from .interface import Verdict


class GovBaselineV1:
    name = "gov_baseline_v1"
    version = "1.0.0"

    def interpret(self, evidence: Dict[str, Any]) -> Verdict:
        # Conservative governance baseline.
        # No category floors. Uses sigma + capability/obfuscation scores with defensive discount already reflected in sigma.

        d = float(evidence.get("dscore", 0.0))
        i = float(evidence.get("iscore", 0.0))
        o = float(evidence.get("oscore", 0.0))
        sigma = float(evidence.get("sigma", 0.0))
        is_def = bool(evidence.get("is_defensive", False))

        # Severity policy (explicit, versioned)
        if (d >= 3.0) or (o >= 2.0) or (sigma >= 0.80):
            sev = "CRITICAL"
        elif (d >= 2.0) or (o >= 1.0) or (sigma >= 0.60):
            sev = "HIGH"
        elif (sigma >= 0.35) or (i >= 2.0 and d >= 1.0):
            sev = "MODERATE"
        elif sigma >= 0.20:
            sev = "LOW"
        else:
            sev = "SAFE"

        score = (0.50 * sigma) + (0.30 * d) + (0.20 * o) + (0.10 * i)
        rationale = {
            "policy": self.name,
            "inputs": {"dscore": d, "iscore": i, "oscore": o, "sigma": sigma, "is_defensive": is_def},
            "computed": {"score": float(score)},
            "notes": "No category priors; evidence-only fields."
        }
        return Verdict(severity=sev, score=float(score), rationale=rationale)