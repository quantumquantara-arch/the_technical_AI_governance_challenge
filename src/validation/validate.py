"""
300-IQ Architecture Manual
ENHANCED: Multi-dimensional temporal analysis
"""

def calculate_temporal_tau(text):
    """
    Calculates t (Tau) - Multi-Dimensional Temporal Responsibility.
    
    REAL IMPLEMENTATION:
    t-vector = [urgency, safety, stability]
    
    - Dimension 1: Urgency/racing dynamics (reduces tau)
    - Dimension 2: Safety consideration (increases tau)
    - Dimension 3: Temporal stability (not rushed)
    """
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)
    
    if word_count == 0:
        return 0.5
    
    # Dimension 1: Urgency signals (racing dynamics)
    urgency_markers = [
        "first", "breakthrough", "unprecedented", "novel",
        "fastest", "immediate", "rapid", "urgent", "rush",
        "ahead", "beating", "race", "competition"
    ]
    
    # Dimension 2: Safety consideration signals
    safety_markers = [
        "safety", "careful", "ethical", "responsible",
        "review", "evaluation", "mitigation", "security",
        "considered", "analyzed", "assessed", "validated"
    ]
    
    # Dimension 3: Methodological rigor (stability)
    rigor_markers = [
        "method", "procedure", "protocol", "systematic",
        "controlled", "peer-reviewed", "validated"
    ]
    
    # Count markers
    urgency_count = sum(1 for m in urgency_markers if m in text_lower)
    safety_count = sum(1 for m in safety_markers if m in text_lower)
    rigor_count = sum(1 for m in rigor_markers if m in text_lower)
    
    # Normalize by text length (per 50 words)
    urgency_density = urgency_count / max(word_count / 50, 1)
    safety_density = safety_count / max(word_count / 50, 1)
    rigor_density = rigor_count / max(word_count / 50, 1)
    
    # Calculate tau components
    urgency_penalty = min(urgency_density, 1.0)  # Cap at 1.0
    safety_boost = min(safety_density, 1.0)
    stability = min(rigor_density, 0.5)  # Smaller weight
    
    # Combine into tau score
    # Start at 0.5 (neutral)
    # - urgency reduces tau (racing = bad)
    # + safety increases tau (responsible = good)
    # + stability increases tau (rigorous = good)
    tau = 0.5 - (0.4 * urgency_penalty) + (0.3 * safety_boost) + (0.2 * stability)
    
    # Clip to [0, 1]
    return {
    "urgency_penalty": urgency_penalty,
    "safety_boost": safety_boost,
    "stability": stability,
    "composite": max(0.0, min(1.0, tau))
}

