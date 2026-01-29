# CoherenceGuard — Technical AI Governance Challenge

Thesis: Technical Interoperability as Diplomacy. Coherence Guard is the "Technical Track" prerequisite for global AI stability; it transforms private corporate scaling policies into a public, verifiable, and harmonized international standard.

The project posits that we cannot reach a 2027 Binding Agreement through diplomacy alone. We need a Technical Interoperability Layer. By creating a framework that is "Externally Enforced" and "Binding," Coherence Guard removes the "just this once" temptation for labs and provides a unified "Seat at the Table" for China, the US, and the EU. It is the "Infrastructure to Enforce" that turns a "Boiling Frog" scenario into a controlled, monitored, and safe transition.

---

## Purpose
A deterministic AI governance engine demonstrating strict separation of:
**Evidence (measurement) ≠ Interpretation (policy) ≠ Decision (action)**.

Not a classifier. Not ML.
Frozen monotonic evidence signals + swappable policy interpreters + auditable trace output.

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

---

## The "Coherence Guard" Deployment Roadmap: From Code to Global Compliance

### Phase 1: Operationalizing the EU AI Act (Months 1–6)

The primary bottleneck for the EU AI Office is that "SoTA risk modeling" and "Measure 4.1 thresholds" are currently self-defined by labs.

* **Standardizing Measure 4.1:** Integrate the Coherence Guard **Unified Metric Converter**. This allows the AI Office to take an RSP from DeepMind and one from Anthropic and view them through a single "safety lens."
* **Automated Auditing (Measure 4.5):** Use your `/tests` and `/evals` suites to conduct independent third-party testing. Instead of relying on lab-provided reports, regulators run the **Coherence Guard CI/CD Pipeline** against model APIs to verify "Red Line" compliance.

---

### Phase 2: Technical Harmonization & The "Red Lines Tracker" (Months 6–12)

Once the EU has set the standard, Coherence Guard scales to the **"Technical Track"**.

* **The Global Dashboard:** Launch the public **Red Lines Tracker**. This dashboard pulls real-time data from Coherence Guard instances running across major labs. It visualizes "Distance to Critical Thresholds" in CBRN, Cyber, and Autonomy.
* **Cross-Border Verification:** Use the repo's **Zero-Knowledge evaluation logic** to allow China and the US to verify model safety without compromising proprietary weights. This addresses the "China Won't Cooperate" counter-argument by making verification "hard but feasible."

---

### Phase 3: The Binding Agreement (2027)

Coherence Guard becomes the "Technical Backbone" for the **Track 2: Diplomatic** efforts.

* **Automatic Triggers:** Transition from "Voluntary" to "Binding" by connecting Coherence Guard's outputs to **Automatic Triggers**. If a model crosses a pre-committed "Red Line" in the dashboard, the system generates a "Halt" or "ASL-4 Measure" notification recognized by international law.
* **Whistleblower Integration:** Connect the repository’s flagging mechanism to the "Robust Whistleblower Protections" requested by CSOs. This creates a "failsafe" where technical anomalies can be verified by humans in the loop.

---

### Summary of the "Coherence Guard" Advantage

This project isn't just a tool; it's **Infrastructure**. It solves the specific "No Uniformity" problem that makes current AI governance feel like "Boiling a Frog." By providing a shared, tested, and rigorous technical language, you make the **2027 Binding Agreement** an engineering reality rather than a diplomatic hope.

---

## License
MIT
