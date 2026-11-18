
from core import negotiation_support as ns


def test_all_four_modules_work_together(monkeypatch):
    monkeypatch.setattr(
        ns, "check_feasibility",
        lambda **kwargs: {
            "feasible": True,
            "no_feasible_deal": False,
            "mediator_suggestion": 3500.0,
            "proposed_price_feasible": True,
            "reason": "Feasible price range."
        }
    )

    monkeypatch.setattr(
        ns, "analyze_message",
        lambda **kwargs: {
            "success": True,
            "predicted_intent": "counter-price",
            "confidence_score": 85.0,
            "interpretation": "Suggesting another price.",
            "warnings": []
        }
    )

    monkeypatch.setattr(
        ns, "analyze_risks",
        lambda **kwargs: {
            "risk_detected": False,
            "warning_count": 0,
            "warnings": []
        }
    )

    monkeypatch.setattr(
        ns, "generate_response",
        lambda **kwargs: {
            "success": True,
            "response": "Would you consider the suggested price?",
            "source": "ollama"
        }
    )

    result = ns.analyze_negotiation(
        message="I can offer another price.",
        buyer_max=4000,
        seller_min=3000,
        current_offer=3500
    )

    assert result["success"] is True
    assert result["mediator"]["suggestion"] == 3500.0
    assert result["analyst"]["predicted_intent"] == "counter-price"
    assert result["risks"]["risk_detected"] is False
    assert result["ai_response"]["source"] == "ollama"


def test_private_price_limits_are_not_returned(monkeypatch):
    monkeypatch.setattr(
        ns, "check_feasibility",
        lambda **kwargs: {
            "feasible": True,
            "no_feasible_deal": False,
            "mediator_suggestion": 3500.0,
            "proposed_price_feasible": True,
            "reason": "Feasible."
        }
    )

    monkeypatch.setattr(
        ns, "analyze_message",
        lambda **kwargs: {
            "success": True,
            "predicted_intent": "agree",
            "confidence_score": 90.0,
            "interpretation": "Agreement.",
            "warnings": []
        }
    )

    monkeypatch.setattr(
        ns, "analyze_risks",
        lambda **kwargs: {
            "risk_detected": False,
            "warning_count": 0,
            "warnings": []
        }
    )

    monkeypatch.setattr(
        ns, "generate_response",
        lambda **kwargs: {
            "success": True,
            "response": "Thank you.",
            "source": "fallback"
        }
    )

    result = ns.analyze_negotiation(
        message="That works.",
        buyer_max=4000,
        seller_min=3000
    )

    assert "buyer_max" not in str(result)
    assert "seller_min" not in str(result)


def test_ai_is_skipped_if_analyst_fails(monkeypatch):
    monkeypatch.setattr(
        ns, "check_feasibility",
        lambda **kwargs: {
            "feasible": True,
            "no_feasible_deal": False,
            "mediator_suggestion": 3500.0,
            "proposed_price_feasible": None,
            "reason": "Feasible."
        }
    )

    monkeypatch.setattr(
        ns, "analyze_message",
        lambda **kwargs: {
            "success": False,
            "predicted_intent": None,
            "confidence_score": None,
            "interpretation": "Unavailable.",
            "warnings": ["Model unavailable."]
        }
    )

    monkeypatch.setattr(
        ns, "analyze_risks",
        lambda **kwargs: {
            "risk_detected": False,
            "warning_count": 0,
            "warnings": []
        }
    )

    def should_not_run(**kwargs):
        raise AssertionError("Gen AI should not run without intent analysis.")

    monkeypatch.setattr(ns, "generate_response", should_not_run)

    result = ns.analyze_negotiation(
        message="Hello.",
        buyer_max=4000,
        seller_min=3000
    )

    assert result["success"] is False
    assert result["ai_response"]["success"] is False
    assert result["ai_response"]["response"] is None
