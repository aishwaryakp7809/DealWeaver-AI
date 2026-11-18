
from agents.buyer_agent import BuyerAgent


def test_rejection_does_not_end_negotiation():
    buyer = BuyerAgent(10000, 7000)

    buyer.make_opening_offer()

    result = buyer.reject_offer()

    assert result["action"] == "reject"
    assert buyer.negotiation_active is True


def test_can_continue_after_rejection():
    buyer = BuyerAgent(10000, 7000)

    buyer.make_opening_offer()
    buyer.reject_offer()

    result = buyer.receive_offer(9000)

    assert result["action"] == "counter"
    assert buyer.negotiation_active is True


def test_reject_offer_above_maximum_budget():
    buyer = BuyerAgent(10000, 7000)

    buyer.make_opening_offer()

    result = buyer.receive_offer(12000)

    assert result["action"] == "reject"
    assert buyer.negotiation_active is True


def test_mediator_suggestion_guides_buyer_counteroffer():
    buyer = BuyerAgent(10000, 7000, max_rounds=5)

    buyer.make_opening_offer()

    result = buyer.receive_offer(
        seller_offer=9500,
        mediator_suggestion=7500
    )

    assert result["action"] == "counter"
    assert result["price"] == 7500


def test_mediator_cannot_force_buyer_above_own_target():
    buyer = BuyerAgent(10000, 7000, max_rounds=5)

    buyer.make_opening_offer()

    result = buyer.receive_offer(
        seller_offer=9500,
        mediator_suggestion=9500
    )

    assert result["action"] == "counter"
    assert result["price"] == 7750
    assert result["price"] <= buyer.max_budget


def test_buyer_can_withdraw():
    buyer = BuyerAgent(10000, 7000)

    buyer.make_opening_offer()
    result = buyer.withdraw()

    assert result["action"] == "no_deal"
    assert buyer.negotiation_active is False


def test_mediator_can_confirm_no_feasible_deal():
    buyer = BuyerAgent(10000, 7000)

    buyer.make_opening_offer()

    result = buyer.receive_offer(
        seller_offer=12000,
        no_feasible_deal=True
    )

    assert result["action"] == "no_deal"
    assert buyer.negotiation_active is False

# Create buyer
buyer = BuyerAgent(
    max_budget=10000,
    opening_offer=7000,
    max_rounds=5
)

# First offer
print("BUYER OPENING OFFER:")
print(buyer.make_opening_offer())

# Seller's first counteroffer
print("\nSELLER OFFER: 9500")
print(buyer.receive_offer(9500))

# Seller's second counteroffer
print("\nSELLER OFFER: 8500")
print(buyer.receive_offer(8500))
