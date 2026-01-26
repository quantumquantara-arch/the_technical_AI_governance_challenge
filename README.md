# CoherenceGuard — Technical AI Governance Challenge

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