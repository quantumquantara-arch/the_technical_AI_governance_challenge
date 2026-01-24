from src.detection import detect_dual_use
from src.zero_return import zero_return
from src.validation import validate_papers

# Example call (integrate factual)
text = "high-drift scenarios in recursive depth > 4"
detection = detect_dual_use(text)
risk = 1  # Factual example
zero = zero_return(risk)
papers = ["symbolic constancy under recursion"]
validation = validate_papers(papers)

print(detection, zero, validation)
