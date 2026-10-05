def risk_score(probability, row):
    # Transparent risk layer for an academic prototype:
    # ML probability is dominant; amount and velocity/context rules can add pressure.
    score = int(round(max(0.0, min(1.0, probability)) * 100))
    amount = float(row.get("Amount", 0) or 0)
    if amount >= 5000: score = min(100, score + 7)
    elif amount >= 2000: score = min(100, score + 4)
    return score

def risk_band(score):
    if score >= 75: return "CRITICAL"
    if score >= 50: return "HIGH"
    if score >= 25: return "MEDIUM"
    return "LOW"
