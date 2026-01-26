from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Protocol

Evidence = Dict[str, Any]

@dataclass(frozen=True)
class InterpVerdict:
    severity: str
    score: float
    rationale: str
    interpreter_name: str
    interpreter_version: str

class Interpreter(Protocol):
    name: str
    version: str
    def interpret(self, evidence: Evidence) -> InterpVerdict: ...