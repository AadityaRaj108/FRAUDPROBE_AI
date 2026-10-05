from src.scoring import risk_score, risk_band

def test_risk_bandaries():
    assert risk_band(10) == "LOW"
    assert risk_band(40) == "MEDIUM"
    assert risk_band(60) == "HIGH"
    assert risk_band(90) == "CRITICAL"

def test_amount_modifier():
    assert risk_score(0.5, {"Amount":0}) == 50
    assert risk_score(0.5, {"Amount":5000}) == 57
