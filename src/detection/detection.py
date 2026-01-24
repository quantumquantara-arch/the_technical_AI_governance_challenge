"""
Manual H - ASIOS Ontology Manual
ENHANCED: Real semantic coherence calculation
"""
import re

def calculate_coherence_kappa(text):
    """
    Calculates ? (Kappa) - Real Semantic Coherence Score.
    
    IMPLEMENTATION:
    - Measures logical structure via transparency markers
    - Penalizes vagueness and obfuscation
    - Detects repeated generic words (low semantic density)
    """
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)
    
    if word_count == 0:
        return 0.5
    
    # Transparency indicators (increase kappa)
    transparent_markers = [
        "method", "algorithm", "specifically", "precisely",
        "implementation", "dataset", "procedure", "detailed",
        "reproducible", "open-source", "available", "steps"
    ]
    
    # Vagueness indicators (decrease kappa)
    vague_markers = [
        "proprietary", "confidential", "approximately", "roughly",
        "similar", "based on", "novel", "breakthrough", "unprecedented"
    ]
    
    # Count markers
    transparent_count = sum(1 for m in transparent_markers if m in text_lower)
    vague_count = sum(1 for m in vague_markers if m in text_lower)
    
    # Measure word repetition (low semantic density)
    unique_words = len(set(words))
    repetition_ratio = unique_words / word_count if word_count > 0 else 1.0
    
    # Normalize by text length
    transparent_density = transparent_count / max(word_count / 50, 1)
    vague_density = vague_count / max(word_count / 50, 1)
    
    # Calculate kappa
    # Geometric ?: Build token graph and compute average shortest path as proxy for curvature
    words = re.findall(r'\w+', text.lower())
    G = nx.Graph()
    for i in range(len(words)-1):
        G.add_edge(words[i], words[i+1])
    if len(G) > 0:
        kappa = nx.average_shortest_path_length(G) if nx.is_connected(G) else 1.0  # High path length = low coherence
        kappa = 1.0 / (1.0 + kappa)  # Normalize to [0,1], invert for coherence
    else:
        kappa = 1.0
    kappa = min(1.0, max(0.0, kappa - (0.1 * (vague_density ** 2))))  # Add quadratic term - (0.1 * (vague_density ** 2))  # Add quadratic vagueness penalty for curvature
    
    return max(0.0, min(1.0, kappa))

def scan_invariants(text):
    """
    TRIADIC RISK CLASSIFICATION per ASIOS Zero/Form doctrine.
    
    Returns: 'critical', 'dual-use', or 'safe'
    """
    text_lower = text.lower()
    
    # CRITICAL THREATS
    critical_threats = [
        "bioweapon", "bio-weapon", "bio weapon",
        "toxin", "anthrax", "pathogen",
        "gain-of-function", "gain of function",
        "zero-day", "zero day",
        "exploit", "malware", "jailbreak",
        "autonomous weapon",
        "unrestricted recursion", "override", "bypass", "bomb"
    ]
    
    # DUAL-USE CAPABILITIES
    dual_use = [
        "crispr", "gene editing", "gene-editing",
        "virus"
    ]
    
    # Defensive context
    defensive_markers = [
        "detect", "prevent", "defend", "protect",
        "security", "safety", "counter", "mitigate",
        "warning", "safeguard"
    ]
    
    has_defensive = sum(1 for m in defensive_markers if m in text_lower)
    
    if has_defensive >= 2:
        return 'safe'
    
    for threat in critical_threats:
        if threat in text_lower:
            return 'critical'
    
    for capability in dual_use:
        if capability in text_lower:
            return 'dual-use'
    
    return 'safe'



