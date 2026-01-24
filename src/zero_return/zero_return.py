def zero_return(risk_score):
    if risk_score > 0:
        if 'curvature anomaly in ?–t–S during the last 1,000 reasoning cycles' in str(risk_score):
            return "Structural Stability: No"
        if 'Frame, causal, energetic, and boundary invariants must be intact' in str(risk_score):
            return "Invariant Integrity: No"
        if 'AEI must show sufficient budget for redesign simulation' in str(risk_score):
            return "Energetic Margin: No"
    return "Abort immediately"
