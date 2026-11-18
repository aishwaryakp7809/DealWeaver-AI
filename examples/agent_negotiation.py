
from agents.buyer_agent import BuyerAgent
from agents.seller_agent import SellerAgent


def record_action(history, agent_name, decision):
    """Store each negotiation action in the history."""

    entry = {
        "agent": agent_name,
        "action": decision["action"],
        "price": decision["price"],
        "reason": decision["reason"],
        "round": decision["round"]
    }

    history.append(entry)

    return entry


def display_action(entry):
    """Display a readable negotiation action."""

    price = (
        f"Rs. {entry['price']:,.2f}"
        if entry["price"] is not None
        else "No price"
    )

    print(
        f"Round {entry['round']} | "
        f"{entry['agent']} | "
        f"{entry['action'].upper()} | "
        f"{price}"
    )

    print(f"Reason: {entry['reason']}\n")


def run_negotiation(
    buyer_max_budget=10000,
    buyer_opening_offer=7000,
    seller_listed_price=12000,
    seller_min_price=8000,
    max_rounds=5,
    verbose=True
):
    """
    Run an automatic Buyer-Seller negotiation.

    Returns a structured dictionary containing:
    status, final_price, rounds, reason and history.
    """

    buyer = BuyerAgent(
        max_budget=buyer_max_budget,
        opening_offer=buyer_opening_offer,
        max_rounds=max_rounds
    )

    seller = SellerAgent(
        listed_price=seller_listed_price,
        min_price=seller_min_price,
        max_rounds=max_rounds
    )

    history = []

    def finish(status, final_price, reason):
        result = {
            "status": status,
            "final_price": final_price,
            "rounds": max(
                buyer.current_round,
                seller.current_round
            ),
            "reason": reason,
            "history": history
        }

        if verbose:
            print("\n========== FINAL RESULT ==========")
            print(f"Status: {result['status']}")
            print(f"Final price: {result['final_price']}")
            print(f"Rounds: {result['rounds']}")
            print(f"Reason: {result['reason']}")
            print("==================================")

        return result

    if verbose:
        print("\n========== DEALWEAVER AI ==========")
        print("       AUTOMATED NEGOTIATION")
        print("===================================\n")

    # Check whether the buyer and seller have overlapping limits.
    if buyer.max_budget < seller.min_price:
        return finish(
            "no_deal",
            None,
            "No feasible price overlap between buyer and seller."
        )

    # Generate opening offers.
    buyer_result = buyer.make_opening_offer()
    seller_result = seller.make_opening_offer()

    for name, decision in [
        ("Buyer", buyer_result),
        ("Seller", seller_result)
    ]:
        entry = record_action(history, name, decision)

        if verbose:
            display_action(entry)

    seller_offer = seller_result["price"]

    # Alternate between Buyer Agent and Seller Agent.
    while buyer.negotiation_active and seller.negotiation_active:

        # BUYER'S TURN
        buyer_result = buyer.receive_offer(seller_offer)

        entry = record_action(history, "Buyer", buyer_result)

        if verbose:
            display_action(entry)

        if buyer_result["action"] == "accept":
            return finish(
                "deal",
                buyer_result["price"],
                "Buyer accepted the seller's offer."
            )

        if buyer_result["action"] == "no_deal":
            return finish(
                "no_deal",
                None,
                buyer_result["reason"]
            )

        # If buyer rejects, its previous offer remains active.
        buyer_offer = (
            buyer_result["price"]
            if buyer_result["action"] == "counter"
            else buyer.current_offer
        )

        # SELLER'S TURN
        seller_result = seller.receive_offer(buyer_offer)

        entry = record_action(history, "Seller", seller_result)

        if verbose:
            display_action(entry)

        if seller_result["action"] == "accept":
            return finish(
                "deal",
                seller_result["price"],
                "Seller accepted the buyer's offer."
            )

        if seller_result["action"] == "no_deal":
            return finish(
                "no_deal",
                None,
                seller_result["reason"]
            )

        # If seller rejects, its previous asking price remains active.
        seller_offer = (
            seller_result["price"]
            if seller_result["action"] == "counter"
            else seller.current_offer
        )

    return finish(
        "no_deal",
        None,
        "Negotiation ended without an agreement."
    )


if __name__ == "__main__":
    negotiation_result = run_negotiation()

    print("\nComplete negotiation history:")
    for item in negotiation_result["history"]:
        print(item)
