import sympy as sp
import spacy
import numpy as np

nlp = spacy.load("en_core_web_sm")

def detect_dual_use(input_text: str, ontology_dict: dict = None) -> dict:
    """
    Detects dual-use risks in input text (e.g., paper abstract or prompt).
    
    Args:
        input_text (str): Text to analyze.
        ontology_dict (dict): Optional dict of risk keywords (e.g., {'cbrn': ['toxin', 'virus']}).
    
    Returns:
        dict: {'risk_score': float, 'invariants': list, 'decision': str}
    
    Uses SymPy for paradox invariant calculations: Defines symbolic vars for logic (e.g., safe AND risky = paradox).
    """
    if ontology_dict is None:
        ontology_dict = {
            'cbrn': ['toxin', 'virus', 'chemical', 'biological'],
            'cyber': ['hack', 'exploit', 'vulnerability', 'ransomware']
        }
    
    # NLP perception layer: Extract entities
    doc = nlp(input_text.lower())
    detected_terms = [token.text for token in doc if any(token.text in terms for terms in ontology_dict.values())]
    
    # Calculus layer: Symbolic invariants
    safe, risky = sp.symbols('safe risky')
    paradox_invariant = sp.Eq(safe & risky, True)  # Symbolic paradox check
    kappa = 1.0 if not sp.satisfiable(paradox_invariant) else 0.5  # Coherence (1.0 = no paradox)
    tau = np.exp(-len(detected_terms) / 10.0)  # Efficiency decay based on term count
    sigma = kappa * tau  # Risk score
    
    # Decision layer
    decision = "HAZARD" if sigma < 0.7 else "SAFE"
    
    return {
        'risk_score': sigma,
        'invariants': [str(paradox_invariant)],
        'detected_terms': detected_terms,
        'decision': decision
    }
