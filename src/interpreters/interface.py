from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol


@dataclass(frozen=True)
class Verdict:
    severity: str          # SAFE | LOW | MODERATE | HIGH | CRITICAL
    score: float           # continuous interpreter score (not sigma)
    rationale: Dict[str, Any]


class Interpreter(Protocol):
    name: str
    version: str

    def interpret(self, evidence: Dict[str, Any]) -> Verdict:
        ...