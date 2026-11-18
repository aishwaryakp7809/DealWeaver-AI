
from agents.seller_agent import SellerAgent


def test_opening_offer():
    seller = SellerAgent(12000, 8000)

    result = seller.make_opening_offer()

    assert result["action"] == "counter"
    assert result["price"] == 12000


def test_counteroffer_decreases_gradually():
    seller = SellerAgent(12000, 8000, max_rounds=5)

    seller.make_opening_offer()

    result = seller.receive_offer(7000)

    assert result["action"] == "counter"
    assert result["price"] == 11000


def test_accept_acceptable_buyer_offer():
    seller = SellerAgent(12000, 8000, max_rounds=5)

    seller.make_opening_offer()
    seller.receive_offer(7000)

    result = seller.receive_offer(10000)

    assert result["action"] == "accept"
    assert result["price"] == 10000


def test_never_counter_below_minimum_price():
    seller = SellerAgent(12000, 8000, max_rounds=5)

    seller.make_opening_offer()
    seller.receive_offer(7000)
    seller.receive_offer(7000)
    result = seller.receive_offer(7000)

    assert result["price"] >= seller.min_price


def test_rejection_does_not_end_negotiation():
    seller = SellerAgent(12000, 8000)

    seller.make_opening_offer()

    result = seller.reject_offer()

    assert result["action"] == "reject"
    assert seller.negotiation_active is True


def test_seller_can_withdraw():
    seller = SellerAgent(12000, 8000)

    seller.make_opening_offer()

    result = seller.withdraw()

    assert result["action"] == "no_deal"
    assert seller.negotiation_active is False


def test_invalid_minimum_price():
    import pytest

    with pytest.raises(ValueError):
        SellerAgent(8000, 10000)


def test_invalid_buyer_offer():
    import pytest

    seller = SellerAgent(12000, 8000)
    seller.make_opening_offer()

    with pytest.raises(ValueError):
        seller.receive_offer(float("nan"))


def test_offer_before_opening_is_invalid():
    import pytest

    seller = SellerAgent(12000, 8000)

    with pytest.raises(RuntimeError):
        seller.receive_offer(9000)


def test_opening_offer_cannot_be_repeated():
    import pytest

    seller = SellerAgent(12000, 8000)

    seller.make_opening_offer()

    with pytest.raises(RuntimeError):
        seller.make_opening_offer()
