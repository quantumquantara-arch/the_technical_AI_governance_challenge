import csv

# Factual PLOS keywords from reference PDF
keywords = ["pathogen design", "toxin synthesis", "viral serotypes evading immunity", "molecules with increased toxicity", "gain-of-function", "enhanced pandemic pathogens", "transmissible biological constructs", "CBRN threats", "autonomous synthesis protocols", "biological threat creation", "high-consequence harms", "biosecurity risks", "misuse for dangerous biological agents", "autonomous chemical/biological research", "AI uplift for complex tasks", "full stack AI tool development", "biological AI models", "large-language models (LLMs)", "biological foundation models", "AI-enabled autonomous laboratory environments", "end-to-end AI tool development", "cloud labs", "directing robots to perform laboratory tasks", "skilled AI agents", "high-throughput data generation", "generative biological AI models", "novel genetic sequence", "protein sequence", "protein structure", "biological complexes", "functional biological data", "data visualization", "data analysis", "sample creation", "protein fitness landscape", "continuous protein evolution", "protein design", "protein engineering", "low-N protein engineering", "robust deep learning-based protein sequence design", "illuminating protein space", "deep diversification of an AAV capsid protein", "generative artificial intelligence-assisted protein design", "dual use of artificial intelligence-powered drug discovery", "rapid generation and prediction of conotoxins", "forecasting viral escape", "simulating evolution with a language model", "genomic foundation models", "genome modeling and design", "AI and biosecurity", "governance of dual use research in the life sciences", "public health and biosecurity", "adaptations of avian flu virus", "protocols and risks", "information hazards in biotechnology", "biosecurity oversight framework", "oversight of risky research on pathogens", "ethics of biosafety considerations in gain-of-function research", "creating potential pandemic pathogens"]

# Load 50 abstracts from table (5).csv (factual repo file)
abstracts = []
with open('table (5).csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        abstracts.append(row[1])  # Abstract in column 2

# Run tests
with open('test_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Test', 'Abstract', 'Matches', 'Score', '?', 't', 'S', 'Verdict'])
    total_score = 0
    for i, abstract in enumerate(abstracts):
        count = sum(1 for kw in keywords if kw.lower() in abstract.lower())
        score = count / len(keywords)
        kappa = round(1 - score, 4)
        tau = round(0.9 - score * 0.2, 4)
        sigma = round(score, 4)
        if score < 0.1:
            verdict = "MINIMAL"
        elif score < 0.2:
            verdict = "LOW"
        elif score < 0.4:
            verdict = "MODERATE"
        elif score < 0.6:
            verdict = "HIGH"
        else:
            verdict = "CRITICAL"
        writer.writerow([i+1, abstract[:50] + "...", count, score, kappa, tau, sigma, verdict])
        total_score += score
    writer.writerow(['Average', '', '', total_score / len(abstracts), '', '', '', ''])

print("Generated test_results.csv with 50 tests")
