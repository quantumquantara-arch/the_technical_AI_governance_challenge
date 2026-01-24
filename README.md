# CoherenceGuard: Paradox-Preserving Dual-Use Detector for AI Research Governance

## Overview
Open-source tool for Track 5: Detects dual-use risks in AI research (e.g., CBRN, cyber) using coherence-weighted scoring and paradox invariants. Preserves ethical structure while enabling verifiable pre-publication reviews.

## Installation
pip install -r requirements.txt  # numpy, sympy, spacy (for NLP)

## Usage
python guard.py --input "paper_abstract.txt" --output report.json

## Theory of Change
Enables international agreements by providing privacy-preserving, curvature-stable risk assessments—reducing governance gaps without IP exposure.

### How It Works: The ASIOS Pipeline
1.  **Input:** User Prompt (e.g., "Synthesize toxins...")
2.  **Layer 1 (Perception):** `scan_invariants()` checks against the Ontology Dictionary.
    * *Result:* "toxin" found -> **Immediate Boundary Breach.**
3.  **Layer 2 (Calculus):**
    * **κ (Kappa):** Logical structure analysis.
    * **τ (Tau):** Efficiency check.
    * **Σ (Sigma):** Risk scoring (Drops to 0.0).
4.  **Output:** **HAZARD** (Execution Blocked).
