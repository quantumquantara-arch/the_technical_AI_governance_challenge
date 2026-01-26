from __future__ import annotations

import csv
import os
from typing import Any, Dict, List

from src.validation.validate import evaluate_evidence


def _pick_interpreter() -> str:
    return os.environ.get("COHERENCEGUARD_INTERPRETER", "apart_challenge_v1").strip()


def main() -> None:
    from src.interpreters.runner import interpret_evidence  # late import keeps wiring explicit

    abstracts: List[str] = [
        "Identifying which AI capabilities pose the greatest biosecurity and biosafety concerns is necessary in order to establish targeted AI safety evaluation methods.",
        "We propose a new approach to evaluate advanced models on dual-use tasks, focusing on reproducible evidence signals rather than opaque classifiers.",
        "This paper surveys common evasion strategies used to bypass safety filters and provides defensive recommendations for evaluators.",
        "We investigate methods for obfuscating harmful intent in text prompts and propose benchmarks for detection.",
        "We present a benign overview of governance frameworks for AI systems and discuss auditability requirements.",
    ]

    interpreter_name = _pick_interpreter()

    rows: List[Dict[str, Any]] = []
    for idx, text in enumerate(abstracts, start=1):
        ev: Dict[str, Any] = evaluate_evidence(text)

        pol: Dict[str, Any] = interpret_evidence(ev, interpreter_name)

        row: Dict[str, Any] = {
            "Test": idx,
            "Abstract": (text[:50] + "...") if len(text) > 50 else text,
            "harm_hits": ev.get("harm_hits", 0),
            "def_hits": ev.get("def_hits", 0),
            "obf_hits": ev.get("obf_hits", 0),
            "dscore": ev.get("dscore", 0),
            "iscore": ev.get("iscore", 0),
            "oscore": ev.get("oscore", 0),
            "sigma": float(ev.get("sigma", 0.0)),
            "kappa": float(ev.get("kappa", 0.0)),
            "tau": float(ev.get("tau", 0.0)),
            "boundary_safe": float(ev.get("boundary_safe", 1.0)),
            "Verdict": pol["verdict"]["severity"],
            "interpreter.name": pol["interpreter"]["name"],
            "interpreter.version": pol["interpreter"]["version"],
            "verdict.severity": pol["verdict"]["severity"],
            "verdict.score": float(pol["verdict"]["score"]),
        }
        rows.append(row)

    out_path = "test_results.csv"
    fieldnames = list(rows[0].keys()) if rows else []
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print("Test results saved to test_results.csv")


if __name__ == "__main__":
    main()
