
import math


class SellerAgent:
    """
    DEALWEAVER AI - Seller Agent

    Represents the seller during price negotiations.

    Responsibilities:
    - Make the opening asking price.
    - Evaluate buyer offers.
    - Generate counteroffers.
    - Never accept below the seller's minimum price.
    - Track negotiation rounds.
    """

    def __init__(self, listed_price, min_price, max_rounds=5):

        self._validate_price(listed_price, "Listed price")
        self._validate_price(min_price, "Minimum price")

        if min_price > listed_price:
            raise ValueError(
                "Minimum price cannot exceed listed price."
            )

        if isinstance(max_rounds, bool) or not isinstance(max_rounds, int):
            raise ValueError("Maximum rounds must be an integer.")

        if max_rounds < 1:
            raise ValueError("Maximum rounds must be at least 1.")

        self.listed_price = float(listed_price)
        self.min_price = float(min_price)
        self.max_rounds = max_rounds

        self.current_offer = self.listed_price
        self.current_round = 0

        self.started = False
        self.negotiation_active = True

    @staticmethod
    def _validate_price(price, field_name):
        """Validate that a price is a finite positive number."""

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError(f"{field_name} must be a number.")

        if not math.isfinite(price) or price <= 0:
            raise ValueError(
                f"{field_name} must be a finite positive number."
            )

    def make_opening_offer(self):
        """Generate the seller's initial asking price."""

        if self.started:
            raise RuntimeError("Opening offer has already been made.")

        if not self.negotiation_active:
            return self._decision(
                "no_deal", None,
                "Negotiation is no longer active."
            )

        self.started = True
        self.current_round = 1

        return self._decision(
            "counter",
            self.listed_price,
            "Seller is making the opening asking price."
        )

    def receive_offer(self, buyer_offer):
        """Evaluate the buyer's offer and decide what to do."""

        self._validate_price(buyer_offer, "Buyer offer")

        if not self.negotiation_active:
            return self._decision(
                "no_deal", None,
                "Negotiation is no longer active."
            )

        if not self.started:
            raise RuntimeError(
                "Make the opening offer before receiving a buyer offer."
            )

        buyer_offer = float(buyer_offer)
        self.current_round += 1

        # Accept if buyer's offer meets the seller's
        # previous asking price.
        if buyer_offer >= self.current_offer:
            self.negotiation_active = False

            return self._decision(
                "accept",
                buyer_offer,
                "Buyer's offer meets or exceeds the seller's asking price."
            )

        # Calculate the seller's gradual concession target.
        if self.max_rounds == 1:
            progress = 1.0
        else:
            progress = min(
                (self.current_round - 1) / (self.max_rounds - 1),
                1.0
            )

        target_price = (
            self.listed_price
            - (self.listed_price - self.min_price) * progress
        )

        target_price = max(target_price, self.min_price)

        # Accept if buyer's offer is within the
        # seller's acceptable range for this round.
        if buyer_offer >= target_price:
            self.negotiation_active = False

            return self._decision(
                "accept",
                buyer_offer,
                "Buyer's offer meets the seller's acceptable target."
            )

        # Stop if maximum negotiation rounds are reached.
        if self.current_round >= self.max_rounds:
            self.negotiation_active = False

            return self._decision(
                "no_deal",
                None,
                "Maximum negotiation rounds reached."
            )

        # Reject an offer below the seller's minimum price
        # if no better counteroffer can be made.
        if target_price >= self.current_offer:
            return self._decision(
                "reject",
                None,
                "Seller cannot reduce the price further."
            )

        # Generate the next counteroffer.
        next_offer = min(self.current_offer, target_price)

        # Never go below the seller's minimum price.
        next_offer = max(next_offer, self.min_price)

        self.current_offer = next_offer

        return self._decision(
            "counter",
            next_offer,
            "Seller is reducing the price within acceptable limits."
        )

    def reject_offer(self, reason="Seller rejected the current offer."):
        """Reject the current offer without ending negotiation."""

        if not self.negotiation_active:
            return self._decision(
                "no_deal", None,
                "Negotiation is no longer active."
            )

        return self._decision("reject", None, reason)

    def withdraw(self):
        """Seller voluntarily ends the negotiation."""

        self.negotiation_active = False

        return self._decision(
            "no_deal", None,
            "Seller withdrew from the negotiation."
        )

    def _decision(self, action, price, reason):
        """Return a standardized decision dictionary."""

        return {
            "action": action,
            "price": price,
            "reason": reason,
            "round": self.current_round
        }
