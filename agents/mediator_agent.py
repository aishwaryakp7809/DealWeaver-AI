
import math


def _validate_price(price, field_name):
    """Validate a price as a finite positive number."""

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise ValueError(f"{field_name} must be a number.")

    if not math.isfinite(price) or price <= 0:
        raise ValueError(
            f"{field_name} must be a finite positive number."
        )


def check_feasibility(buyer_max, seller_min, proposed_price=None):
    """
    Check whether buyer and seller have a mutually feasible price range.

    Parameters:
        buyer_max: Buyer's maximum budget.
        seller_min: Seller's minimum acceptable price.
        proposed_price: Optional price to check against both limits.

    Returns:
        A dictionary containing feasibility, midpoint suggestion,
        proposed-price status and explanation.

    Note:
        A feasible price is only a suggestion.
        It does not mean that either party has accepted the deal.
    """

    _validate_price(buyer_max, "Buyer's maximum budget")
    _validate_price(seller_min, "Seller's minimum price")

    if proposed_price is not None:
        _validate_price(proposed_price, "Proposed price")

    buyer_max = float(buyer_max)
    seller_min = float(seller_min)

    # Check whether the buyer's and seller's limits overlap.
    feasible = seller_min <= buyer_max

    if not feasible:
        return {
            "feasible": False,
            "no_feasible_deal": True,
            "seller_min": seller_min,
            "buyer_max": buyer_max,
            "midpoint": None,
            "mediator_suggestion": None,
            "proposed_price": proposed_price,
            "proposed_price_feasible": False if proposed_price is not None else None,
            "reason": (
                "No feasible price overlap exists. "
                "The seller's minimum price exceeds the buyer's maximum budget."
            )
        }

    # Calculate midpoint compromise.
    midpoint = (seller_min + buyer_max) / 2

    # Check optional proposed price.
    proposed_price_feasible = None

    if proposed_price is not None:
        proposed_price_feasible = (
            seller_min <= proposed_price <= buyer_max
        )

    return {
        "feasible": True,
        "no_feasible_deal": False,
        "seller_min": seller_min,
        "buyer_max": buyer_max,
        "midpoint": midpoint,
        "mediator_suggestion": midpoint,
        "proposed_price": proposed_price,
        "proposed_price_feasible": proposed_price_feasible,
        "reason": (
            "A feasible price range exists. "
            f"The suggested midpoint compromise is {midpoint:.2f}. "
            "This is a suggestion, not guaranteed acceptance."
        )
    }


if __name__ == "__main__":

    result = check_feasibility(
        buyer_max=4000,
        seller_min=3500
    )

    print("DEALWEAVER AI - Mediator Agent")
    print("--------------------------------")

    for key, value in result.items():
        print(f"{key}: {value}")
