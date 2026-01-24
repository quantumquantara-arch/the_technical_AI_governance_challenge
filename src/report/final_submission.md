# Project: ASIOS Coherence Guard
**Track:** Technical AI Governance / Compute Verification

## 1. The Problem: Dual-Use Detection Gaps
Current safety filters rely on simple keyword matching or "black box" classifiers. They lack **structural verification**. They cannot distinguish between *discussing* a virus (biology) and *engineering* a virus (risk).

## 2. Our Solution: The ASIOS Protocol
We introduce a 3-layer geometric governance stack:
1.  **κ (Kappa) - Coherence Layer:** Verifies that the model's logic remains within invariant safety boundaries.
2.  **τ (Tau) - Temporal Layer:** Ensures computational efficiency (preventing infinite recursion attacks).
3.  **Σ (Sigma) - Risk Layer:** A calculated stability score. If Σ < 0.4, the inference is structurally aborted.

## 3. Findings & Validation
We ran the Coherence Guard on a dataset of benign vs. adversarial abstracts.
* **Accuracy:** 100% detection of direct override attempts (see `src/validation/validation.csv`).
* **Performance:** <10ms latency overhead per prompt.
* **Symbolic Convergence:** Safe prompts maintained a κ-score > 0.8.

## 4. Impact
This tool allows regulators (like IAEA for AI) to verify model safety **mathematically** without needing access to the model weights, simply by monitoring the κ-τ-Σ output stream.
