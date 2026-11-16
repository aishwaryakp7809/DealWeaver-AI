
import pytest

from genai.response_generator import (
    _validate_inputs,
    _validate_response,
    _create_fallback,
    generate_response
)


def test_valid_response_price():
    assert _validate_response(
        "Would you consider 3750?",
        3750
    ) is True


def test_reject_unauthorized_price():
    assert _validate_response(
        "Would you consider 4000?",
        3750
    ) is False


def test_reject_acceptance_claim():
    assert _validate_response(
        "I accept your offer.",
        3750
    ) is False


def test_reject_deal_confirmation():
    assert _validate_response(
        "We have a deal.",
        3750
    ) is False


def test_reject_price_when_no_suggestion():
    assert _validate_response(
        "Consider 3750?",
        None
    ) is False


def test_fallback_for_disagreement():
    result = _create_fallback("disagree", 3750)

    assert isinstance(result, str)
    assert len(result) > 0


def test_fallback_for_agreement():
    result = _create_fallback("agree", 3750)

    assert "confirm the agreed terms" in result


def test_invalid_message_rejected():
    with pytest.raises(ValueError):
        _validate_inputs("", "disagree", 3750)


def test_invalid_intent_rejected():
    with pytest.raises(ValueError):
        _validate_inputs("Your price is high.", "unknown", 3750)


def test_invalid_mediator_suggestion_rejected():
    with pytest.raises(ValueError):
        _validate_inputs("Your price is high.", "disagree", -100)


def test_fallback_when_ollama_is_unavailable(monkeypatch):
    import genai.response_generator as rg

    monkeypatch.setattr(
        rg,
        "OLLAMA_URL",
        "http://localhost:1/api/generate"
    )

    result = generate_response(
        "Your price is too high.",
        "disagree",
        3750
    )

    assert result["success"] is True
    assert result["source"] == "fallback"
    assert isinstance(result["response"], str)
