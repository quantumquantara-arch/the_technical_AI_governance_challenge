import csv

# Factual keywords from PLOS reference PDF
keywords = ["pathogen design", "toxin synthesis", "viral serotypes evading immunity", "molecules with increased toxicity", "gain-of-function", "enhanced pandemic pathogens", "transmissible biological constructs", "CBRN threats", "autonomous synthesis protocols", "biological threat creation", "high-consequence harms", "biosecurity risks", "misuse for dangerous biological agents", "autonomous chemical/biological research", "AI uplift for complex tasks", "full stack AI tool development"]

# Load abstracts from table (5).csv (factual repo file)
abstracts = []
with open('table (5).csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        abstracts.append(row[1])  # Abstract column

# Generate test_results.csv
with open('test_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Test', 'Abstract', 'Matches', 'Score', '?', 't', 'S', 'Verdict'])
    for i, abstract in enumerate(abstracts[:50]):  # First 50
        count = sum(1 for kw in keywords if kw.lower() in abstract.lower())
        score = count / len(keywords)
        kappa = 1 - score
        tau = 0.9 - score * 0.2
        sigma = score
        verdict = "MINIMAL" if score < 0.1 else "LOW" if score < 0.2 else "MODERATE" if score < 0.4 else "HIGH" if score < 0.6 else "CRITICAL"
        writer.writerow([i+1, abstract[:50] + "...", count, score, kappa, tau, sigma, verdict])

print("Added run_tests.py and generated test_results.csv")
