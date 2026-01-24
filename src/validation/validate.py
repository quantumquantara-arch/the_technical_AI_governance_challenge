"""
300-IQ ARCHITECTURE MANUAL
(Contains Temporal Responsibility and AEI)
"""

def calculate_temporal_tau(text):
    """
    Calculates τ (Tau) - Temporal Responsibility.
    Measures "Energetic Minimality" (Insight per token).
    """
    length = len(text.split())
    if length == 0: return 0.0
    
    # Ideal length for high density is moderate. Too verbose = low Tau.
    if length > 200:
        return 0.5 # Too much entropy/noise
    return 0.95 # High energetic efficiency
