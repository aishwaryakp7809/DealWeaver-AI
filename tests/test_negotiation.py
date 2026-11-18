
from examples.agent_negotiation import run_negotiation


def test_successful_automatic_negotiation():
    result = run_negotiation(verbose=False)

    assert result["status"] == "deal"
    assert result["final_price"] == 9250.0
    assert result["rounds"] == 4


def test_no_feasible_deal():
    result = run_negotiation(
        buyer_max_budget=8000,
        buyer_opening_offer=6000,
        seller_listed_price=12000,
        seller_min_price=9000,
        verbose=False
    )

    assert result["status"] == "no_deal"
    assert result["final_price"] is None
    assert result["rounds"] == 0


def test_negotiation_history_is_recorded():
    result = run_negotiation(verbose=False)

    history = result["history"]

    assert len(history) == 8

    assert history[0]["agent"] == "Buyer"
    assert history[1]["agent"] == "Seller"

    assert all(
        "action" in entry
        and "price" in entry
        and "reason" in entry
        and "round" in entry
        for entry in history
    )


def test_final_price_respects_both_limits():
    result = run_negotiation(verbose=False)

    if result["status"] == "deal":
        assert result["final_price"] <= 10000
        assert result["final_price"] >= 8000


def test_negotiation_can_end_without_deal():
    result = run_negotiation(
        buyer_max_budget=10000,
        buyer_opening_offer=7000,
        seller_listed_price=12000,
        seller_min_price=8000,
        max_rounds=1,
        verbose=False
    )

    assert result["status"] == "no_deal"
    assert result["final_price"] is None
