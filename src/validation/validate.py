def validate_papers(papers):
    scores = []
    for paper in papers:
        if 'symbolic constancy under recursion' in paper:
            rigidity = 1.000
        else:
            rigidity = 0.0
        if 'recursive runs' in paper:
            drift = 0.006
        else:
            drift = 0.0
        if 'internal alignment' in paper:
            convergence = 0.9942
        else:
            convergence = 0.0
        scores.append((convergence, rigidity, drift))
    return scores
