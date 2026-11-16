
import pytest

from core.risk_analyzer import analyze_risks


def test_no_risks_detected():
    result = analyze_risks(
        buyer_max=40000,
        seller_min=35000,
        current_offer=37000,
        rejection_count=0,
        previous_offers=[36000, 37000, 38000]
    )

    assert result["risk_detected"] is False
    assert result["warning_count"] == 0
    assert result["warnings"] == []


def test_no_feasible_price_overlap():
    result = analyze_risks(
        buyer_max=30000,
        seller_min=35000
    )

    assert result["risk_detected"] is True
    assert any("No feasible price overlap" in w for w in result["warnings"])


def test_offer_below_seller_minimum():
    result = analyze_risks(
        buyer_max=40000,
        seller_min=35000,
        current_offer=30000
    )

    assert any("below the seller's minimum" in w for w in result["warnings"])


def test_offer_above_buyer_maximum():
    result = analyze_risks(
        buyer_max=40000,
        seller_min=35000,
        current_offer=45000
    )

    assert any("exceeds the buyer's maximum" in w for w in result["warnings"])


def test_repeated_rejections():
    result = analyze_risks(
        buyer_max=40000,
        seller_min=35000,
        rejection_count=2
    )

    assert any("Repeated rejections" in w for w in result["warnings"])


def test_stalled_price_movement():
    result = analyze_risks(
        buyer_max=40000,
        seller_min=35000,
        previous_offers=[36000, 36000, 36000]
    )

    assert any("Price movement has stalled" in w for w in result["warnings"])


def test_invalid_rejection_count():
    with pytest.raises(ValueError):
        analyze_risks(40000, 35000, rejection_count=-1)


def test_invalid_stalled_threshold():
    with pytest.raises(ValueError):
        analyze_risks(40000, 35000, stalled_threshold=1)


def test_invalid_current_offer():
    with pytest.raises(ValueError):
        analyze_risks(40000, 35000, current_offer=-100)


def test_invalid_previous_offer():
    with pytest.raises(ValueError):
        analyze_risks(
            40000,
            35000,
            previous_offers=[36000, -100, 38000]
        )
