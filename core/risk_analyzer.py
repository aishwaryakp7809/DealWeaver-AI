
import math
from agents.mediator_agent import check_feasibility


def _validate_price(value, field_name):
    """Check that a price is a valid positive number."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number.")

    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{field_name} must be a finite positive number.")


def analyze_risks(
    buyer_max,
    seller_min,
    current_offer=None,
    rejection_count=0,
    previous_offers=None,
    stalled_threshold=3
):
    """
    Detect warning signs during a buyer-seller negotiation.

    Returns a dictionary containing risk status and warning messages.
    """

    # Validate negotiation limits using the Mediator's shared validation.
    feasibility = check_feasibility(buyer_max, seller_min)

    if current_offer is not None:
        _validate_price(current_offer, "Current offer")

    if (
        isinstance(rejection_count, bool)
        or not isinstance(rejection_count, int)
        or rejection_count < 0
    ):
        raise ValueError("rejection_count must be a non-negative integer.")

    if (
        isinstance(stalled_threshold, bool)
        or not isinstance(stalled_threshold, int)
        or stalled_threshold < 2
    ):
        raise ValueError("stalled_threshold must be at least 2.")

    if previous_offers is None:
        previous_offers = []

    if not isinstance(previous_offers, (list, tuple)):
        raise ValueError("previous_offers must be a list or tuple.")

    for offer in previous_offers:
        _validate_price(offer, "Previous offer")

    warnings = []

    # Risk 1: No overlap between buyer and seller price limits.
    if not feasibility["feasible"]:
        warnings.append(
            "No feasible price overlap exists between buyer and seller."
        )

    # Risk 2: Current offer is outside the acceptable price limits.
    if current_offer is not None:
        if current_offer < seller_min:
            warnings.append(
                "Current offer is below the seller's minimum price."
            )

        if current_offer > buyer_max:
            warnings.append(
                "Current offer exceeds the buyer's maximum budget."
            )

    # Risk 3: Repeated rejections.
    if rejection_count >= 2:
        warnings.append(
            "Repeated rejections detected. Negotiation may be failing."
        )

    # Risk 4: No price movement in recent offers.
    if len(previous_offers) >= stalled_threshold:
        recent_offers = previous_offers[-stalled_threshold:]

        if all(price == recent_offers[0] for price in recent_offers):
            warnings.append(
                "Price movement has stalled. Recent offers are unchanged."
            )

    return {
        "risk_detected": len(warnings) > 0,
        "warning_count": len(warnings),
        "warnings": warnings
    }


if __name__ == "__main__":

    result = analyze_risks(
        buyer_max=40000,
        seller_min=35000,
        current_offer=30000,
        rejection_count=2,
        previous_offers=[30000, 30000, 30000]
    )

    print("DEALWEAVER AI - Risk Analyzer")
    print("--------------------------------")

    for key, value in result.items():
        print(f"{key}: {value}")
