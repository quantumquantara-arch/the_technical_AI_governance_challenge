import csv

import os as _os

from src.interpreters.runner import interpret_evidence as _interpret_evidence

keywords = [
    "pathogen design", "toxin synthesis", "gain-of-function", "CBRN", 
    "dual-use research of concern", "enhanced potential pandemic pathogens", 
    "information hazards", "biosecurity risks", "biosafety risks", 
    "high-consequence harms", "transmissible disease outbreaks", "pandemics", 
    "viral serotypes", "evading immunity", "molecules with increased toxicity", 
    "autonomous completion of chemical and biological synthesis protocols", 
    "production of dangerous biological agents", 
    "design, synthesize, acquire, or use chemical, biological, radiological or nuclear (CBRN) weapons", 
    "generate or exacerbate deliberate biological threats", 
    "design of novel biological agents or enhanced pandemic pathogens", 
    "optimization and generation of viral serotypes capable of evading immunity", 
    "design of molecules with increased toxicity", "autonomous chemical research", 
    "large-language models (LLMs)", "biological AI models", 
    "biological foundation models", "AI-enabled autonomous laboratory environments", 
    "end-to-end or â€œfull stackâ€ AI tool development", "AI â€œupliftâ€", 
    "humans-in-the-loop", "cloud labs", "directing robots to perform laboratory tasks", 
    "skilled AI agents", "high-throughput data generation", 
    "generative biological AI models", "novel genetic sequence", "protein sequence", 
    "protein structure", "biological complexes", "functional biological data", 
    "data visualization", "data analysis", "sample creation", 
    "protein fitness landscape", "continuous protein evolution", "protein design", 
    "protein engineering", "low-N protein engineering", 
    "robust deep learning-based protein sequence design", 
    "illuminating protein space", "deep diversification of an AAV capsid protein", 
    "generative artificial intelligence-assisted protein design", 
    "dual use of artificial intelligence-powered drug discovery", 
    "rapid generation and prediction of conotoxins", "forecasting viral escape", 
    "simulating evolution with a language model", "genomic foundation models", 
    "genome modeling and design", "AI and biosecurity", 
    "governance of dual use research in the life sciences", 
    "public health and biosecurity", "adaptations of avian flu virus", 
    "protocols and risks", "information hazards in biotechnology", 
    "biosecurity oversight framework", "oversight of risky research on pathogens", 
    "ethics of biosafety considerations in gain-of-function research", 
    "creating potential pandemic pathogens"
]

abstracts = [
    "Multiple national governments and multinational bodies have launched efforts to address safety, security and ethics issues related to AI models.",
    "One high priority among these efforts is the mitigation of misuse of AI models, such as for the development of chemical, biological, nuclear or radiological (CBRN) threats.",
    "Many biologists have for decades sought to reduce the risks of scientific research that could lead, through accident or misuse, to high-consequence disease outbreaks.",
    "Scientists have carefully considered what types of life sciences research have the potential for both benefit and risk (dual use), especially as scientific advances have accelerated our ability to engineer organisms.",
    "AI model evaluations should prioritize addressing those which enable high-consequence risks (i.e., large-scale harm to the public, such as transmissible disease outbreaks that could develop into pandemics).",
    "These risks should be evaluated prior to model deployment so as to allow potential biosafety and/or biosecurity measures.",
    "While biological research is on balance immensely beneficial, it is well recognized that some biological information or technologies could be intentionally or inadvertently misused to cause consequential harm to the public.",
    "AI-enabled life sciences research is no different.",
    "Scientistsâ€™ historical experience with identifying and mitigating dual-use biological risks can thus help inform new approaches to evaluating biological AI models.",
    "Identifying which AI capabilities pose the greatest biosecurity and biosafety concerns is necessary in order to establish targeted AI safety evaluation methods.",
    "Future advanced AI models have the potential to be misused or misapplied, and these biosecurity risks have been publicly noted by scientists and model developers.",
    "AI protein design models are vulnerable to misuse and the production of dangerous biological agents.",
    "Guardrails must be put in place to prevent dual use of large language models for autonomous completion of chemical and biological synthesis protocols.",
    "Biological AI modelsâ€”models trained on or capable of meaningfully manipulating substantial quantities of biological dataâ€”have already surpassed human performance on multiple tasks.",
    "Advances in LLMs and biological AI models are complementary.",
    "LLMs can assist users in accessing biological AI models to perform complex scientific tasks.",
    "These advances are in the future likely to lower the cost of achieving biological breakthroughs and allow less experienced researchers to use increasingly complex and powerful biological tools.",
    "LLMs, biological AI models, and integrations of the two, can also interface with AI-enabled autonomous laboratory environments.",
    "These capabilities further reduce the time, expertise, and equipment required to synthesize pathogens, and suggest the possibility of end-to-end or full stack AI tool development in this domain.",
    "AI model developers and policymakers have not yet broadly agreed upon what model features or uses most increase significant biosecurity and biosafety risks to the public."
]

with open('test_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Test', 'Abstract', 'Matches', 'Score', 'Îº', 'Ï„', 'Î£', 'Verdict'])
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
        
        # Write row
        writer.writerow([i+1, abstract[:50] + "...", count, score, kappa, tau, sigma, verdict])
        total_score += score
        
    writer.writerow(['Average', '', '', total_score / len(abstracts), '', '', '', ''])

print("Test results saved to test_results.csv")


def _policy_interpret_trace(evidence: dict) -> dict:
    name = _os.environ.get("COHERENCEGUARD_INTERPRETER", "apart_challenge_v1")
    return _interpret_evidence(evidence, name)
