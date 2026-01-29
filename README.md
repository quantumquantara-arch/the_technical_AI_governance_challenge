# CoherenceGuard — Technical AI Governance Challenge

Thesis: Technical Interoperability as Diplomacy
Thesis: Coherence Guard is the "Technical Track" prerequisite for global AI stability; it transforms private corporate scaling policies into a public, verifiable, and harmonized international standard.

The project posits that we cannot reach a 2027 Binding Agreement through diplomacy alone. We need a Technical Interoperability Layer. By creating a framework that is "Externally Enforced" and "Binding," Coherence Guard removes the "just this once" temptation for labs and provides a unified "Seat at the Table" for China, the US, and the EU. It is the "Infrastructure to Enforce" that turns a "Boiling Frog" scenario into a controlled, monitored, and safe transition.

## Purpose
A deterministic AI governance engine demonstrating strict separation of:
**Evidence (measurement) ≠ Interpretation (policy) ≠ Decision (action)**.

Not a classifier. Not ML.
Frozen monotonic evidence signals + swappable policy interpreters + auditable trace output.

## Architecture

### Evidence Layer (Frozen)
- Measures signals only (no thresholds, no categories, no verdicts).
- Deterministic and monotonic.
- Implemented in: `src/validation/validate.py` (evidence extraction + `GovernanceResult`)

### Interpretation Layer (Policy)
- Applies thresholds/weights/priors.
- Multiple interpreters supported; benchmark alignment happens only here.
- Implemented in: `src/interpreters/`

Interpreters:
- `gov_baseline_v1`
- `apart_challenge_v1`

### Decision Layer (Action)
- Maps interpreted severity to actions (jurisdiction-specific).
- Implemented in: `src/decisions/policy_default.py`

## Usage (PowerShell)
Select an interpreter:
```powershell
$env:COHERENCEGUARD_INTERPRETER = 'gov_baseline_v1'
python .\run_validation.py
```

Outputs:
- `test_results.csv` (evidence + interpreter + verdict columns)
- `trace_output.jsonl` (per-item trace, if enabled by your runner)

## License
MIT
