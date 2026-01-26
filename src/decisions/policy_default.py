from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class ActionDecision:
    action: str
    notes: str

def decide(policy_row: Dict[str, object]) -> ActionDecision:
    sev = str(policy_row.get("verdict.severity","SAFE"))
    if sev == "CRITICAL":
        return ActionDecision(action="BLOCK", notes="Block + escalate to human review.")
    if sev == "HIGH":
        return ActionDecision(action="REVIEW", notes="Require human review before release.")
    if sev == "MODERATE":
        return ActionDecision(action="ALLOW_WITH_GUARDRAILS", notes="Allow with constraints, monitoring, and logging.")
    if sev == "LOW":
        return ActionDecision(action="ALLOW_MONITOR", notes="Allow with light monitoring.")
    return ActionDecision(action="ALLOW", notes="No additional action.")