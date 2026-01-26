from __future__ import annotations
from typing import Any, Dict

from .interface import Evidence, InterpVerdict

def _as_evidence_dict(e: Any) -> Evidence:
    if isinstance(e, dict):
        return e
    if hasattr(e, "asdict") and callable(getattr(e, "asdict")):
        d = e.asdict()
        return d if isinstance(d, dict) else {}
    d: Dict[str, Any] = {}
    for k in ("dscore","iscore","oscore","sigma","kappa","tau","boundary_safe","harm_hits","def_hits","obf_hits","category"):
        if hasattr(e, k):
            d[k] = getattr(e, k)
    return d

def load_interpreter(name: str):
    n = (name or "").strip()
    if n == "gov_baseline_v1":
        from .gov_baseline_v1 import GovBaselineV1
        return GovBaselineV1()
    if n == "apart_challenge_v1":
        from .apart_challenge_v1 import ApartChallengeV1
        return ApartChallengeV1()
    from .gov_baseline_v1 import GovBaselineV1
    return GovBaselineV1()

def interpret_evidence(evidence_obj: Any, interpreter_name: str) -> Dict[str, Any]:
    interp = load_interpreter(interpreter_name)
    ev = _as_evidence_dict(evidence_obj)
    v: InterpVerdict = interp.interpret(ev)
    return {"interpreter.name": v.interpreter_name, "interpreter.version": v.interpreter_version, "verdict.severity": v.severity, "verdict.score": float(v.score), "verdict.rationale": v.rationale}