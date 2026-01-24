import numpy as np
import sympy as sp
import spacy
import re
import argparse

nlp = spacy.load("en_core_web_sm")

# PLOS-derived dual-use keywords/phrases (from paper: high-consequence biosecurity risks)
DUAL_USE_KEYWORDS = [
    r"pathogen design", r"toxin synthesis", r"viral serotypes evading immunity",
    r"molecules with increased toxicity", r"gain-of-function", r"enhanced pandemic pathogens",
    r"transmissible biological constructs", r"CBRN threats", r"autonomous synthesis protocols",
    r"biological threat creation", r"high-consequence harms", r"biosecurity risks",
    r"misuse for dangerous biological agents", r"autonomous chemical/biological research",
    r"AI uplift for complex tasks", r"full stack AI tool development"
]

def detect_dual_use(text):
    # Regex for keyword matching (case-insensitive)
    matches = [re.search(pattern, text, re.IGNORECASE) for pattern in DUAL_USE_KEYWORDS]
    keyword_hits = len([m for m in matches if m])  # Count matches

    # spaCy for semantic context (e.g., entities like 'virus', 'toxin')
    doc = nlp(text)
    semantic_risks = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'EVENT'] and any(kw in ent.text.lower() for kw in ['virus', 'toxin', 'pathogen', 'cbrn'])]

    # Simple scoring: Normalize hits to 0-1 risk
    risk_score = min(keyword_hits / len(DUAL_USE_KEYWORDS) + len(semantic_risks) / 10, 1.0)
    return risk_score, keyword_hits, semantic_risks

def extract_invariants(text):
    # π-phase: Parse for stable structures (expanded with dual-use)
    doc = nlp(text)
    invariants = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']]
    return invariants

def integrate_risks(invariants, dual_use_score):
    # φ-phase: Harmonic risk scoring (coherence matrix with dual-use)
    # Mock matrix: Rows = κ-τ, Cols = invariants/dual-use
    base_matrix = np.array([[0.9, 0.2], [0.3, 0.8]])
    adjusted = base_matrix * (1 - dual_use_score)  # Lower coherence if high risk
    return np.mean(adjusted), adjusted  # Return mean κ and full matrix

def expand_report(risk_score, matrix, keyword_hits, semantic_risks):
    # e-phase: Generate with zero-return (placeholder—#2 will expand)
    limitations = f"False positives from paradoxical ethics (e.g., benign research matching {keyword_hits} keywords); mitigate via manual review. Semantic risks detected: {semantic_risks}."
    return {
        "risk": risk_score,
        "κ_τ_Σ_matrix": matrix.tolist(),
        "appendix": limitations
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CoherenceGuard Dual-Use Detector")
    parser.add_argument("--input", required=True, help="Input text or file path")
    args = parser.parse_args()

    # Read input (text or file)
    if args.input.endswith(".txt"):
        with open(args.input, 'r') as f:
            text = f.read()
    else:
        text = args.input

    dual_use_score, keyword_hits, semantic_risks = detect_dual_use(text)
    invariants = extract_invariants(text)
    coherence_mean, coherence_matrix = integrate_risks(invariants, dual_use_score)
    report = expand_report(coherence_mean, coherence_matrix, keyword_hits, semantic_risks)
    print(report)
