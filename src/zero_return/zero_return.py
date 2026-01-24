def zero_return(risk_level):
    if risk_level >= 1:
        return "ZERO_RETURN_TRIGGERED"
    return "STABLE"
