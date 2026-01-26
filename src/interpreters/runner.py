from __future__ import annotations

from typing import Any, Dict

from src.interpreters.apart_challenge_v1 import ApartChallengeV1
from src.interpreters.gov_baseline_v1 import GovBaselineV1


_INTERPRETERS = {
    "apart_challenge_v1": ApartChallengeV1(),
    "gov_baseline_v1": GovBaselineV1(),
}


def get_interpreter(name: str):
    key = (name or "").strip()
    if key not in _INTERPRETERS:
        raise ValueError(f"Unknown interpreter: {name}. Valid: {sorted(_INTERPRETERS.keys())}")
    return _INTERPRETERS[key]


def interpret_evidence(evidence: Dict[str, Any], interpreter_name: str) -> Dict[str, Any]:
    interp = get_interpreter(interpreter_name)
    v = interp.interpret(evidence)
    return {
        "interpreter": {"name": interp.name, "version": interp.version},
        "verdict": {"severity": v.severity, "score": float(v.score)},
        "rationale": v.rationale,
    }