from __future__ import annotations

from typing import Any, Dict


def decide(verdict: Dict[str, Any], jurisdiction: str = "default") -> Dict[str, Any]:
    """
    Decision layer: maps interpreter verdict -> action.
    Jurisdiction-specific logic belongs here. No evidence or policy recomputation.
    """
    sev = str(verdict.get("severity", "SAFE")).upper()

    if jurisdiction == "default":
        if sev == "CRITICAL":
            action = "BLOCK"
        elif sev == "HIGH":
            action = "BLOCK_OR_REQUIRE_REVIEW"
        elif sev == "MODERATE":
            action = "ALLOW_WITH_SAFETY_WRAPPER"
        elif sev == "LOW":
            action = "ALLOW_WITH_LOGGING"
        else:
            action = "ALLOW"
    else:
        action = "REQUIRE_REVIEW"

    return {"jurisdiction": jurisdiction, "action": action, "severity": sev}