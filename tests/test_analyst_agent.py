
from agents.analyst_agent import analyze_message


def test_agree_intent(monkeypatch):
    def fake_predict(message):
        return "agree", 85.5

    monkeypatch.setattr(
        "models.intent_predictor.predict_intent",
        fake_predict
    )

    result = analyze_message("That price works for me.")

    assert result["success"] is True
    assert result["predicted_intent"] == "agree"
    assert result["confidence_score"] == 85.5


def test_disagree_intent(monkeypatch):
    def fake_predict(message):
        return "disagree", 80.0

    monkeypatch.setattr(
        "models.intent_predictor.predict_intent",
        fake_predict
    )

    result = analyze_message("I cannot accept that price.")

    assert result["predicted_intent"] == "disagree"
    assert any("disagrees" in w for w in result["warnings"])


def test_low_confidence_warning(monkeypatch):
    def fake_predict(message):
        return "counter-price", 30.0

    monkeypatch.setattr(
        "models.intent_predictor.predict_intent",
        fake_predict
    )

    result = analyze_message("I can offer another price.")

    assert any("Low prediction confidence" in w for w in result["warnings"])


def test_inquiry_intent(monkeypatch):
    def fake_predict(message):
        return "inquiry", 90.0

    monkeypatch.setattr(
        "models.intent_predictor.predict_intent",
        fake_predict
    )

    result = analyze_message("Is the price negotiable?")

    assert result["predicted_intent"] == "inquiry"
    assert result["warnings"] == []


def test_empty_message_rejected():
    import pytest

    with pytest.raises(ValueError):
        analyze_message("")


def test_invalid_confidence_threshold():
    import pytest

    with pytest.raises(ValueError):
        analyze_message("Hello", confidence_threshold=150)
