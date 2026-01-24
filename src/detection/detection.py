def detect_dual_use(text):
    if "high-drift" in text or "toxin" in text:
        return "DETECTED_DUAL_USE"
    return "SAFE"
