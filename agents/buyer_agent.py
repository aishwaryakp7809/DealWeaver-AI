
import math


class BuyerAgent:
    """
    DEALWEAVER AI - Buyer Agent

    The Buyer Agent independently evaluates seller offers
    and Mediator suggestions while respecting the buyer's budget.
    """

    def __init__(self, max_budget, opening_offer, max_rounds=5):

        self._validate_price(max_budget, "Maximum budget")
        self._validate_price(opening_offer, "Opening offer")

        if opening_offer > max_budget:
            raise ValueError("Opening offer cannot exceed maximum budget.")

        if isinstance(max_rounds, bool) or not isinstance(max_rounds, int):
            raise ValueError("Maximum rounds must be an integer.")

        if max_rounds < 1:
            raise ValueError("Maximum rounds must be at least 1.")

        self.max_budget = float(max_budget)
        self.opening_offer = float(opening_offer)
        self.max_rounds = max_rounds

        self.current_offer = self.opening_offer
        self.current_round = 0

        self.started = False
        self.negotiation_active = True

    @staticmethod
    def _validate_price(price, field_name):
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError(f"{field_name} must be a number.")

        if not math.isfinite(price) or price <= 0:
            raise ValueError(
                f"{field_name} must be a finite positive number."
            )

    def make_opening_offer(self):

        if self.started:
            raise RuntimeError("Opening offer has already been made.")

        if not self.negotiation_active:
            return self._decision(
                "no_deal", None, "Negotiation is no longer active."
            )

        self.started = True
        self.current_round = 1

        return self._decision(
            "counter",
            self.opening_offer,
            "Buyer is making the opening offer."
        )

    def receive_offer(
        self,
        seller_offer,
        mediator_suggestion=None,
        no_feasible_deal=False
    ):
        """
        Evaluate a seller offer and optional Mediator suggestion.

        Actions:
        accept  - Accept the seller's offer.
        reject  - Reject this offer but continue negotiating.
        counter  - Make a new buyer offer.
        no_deal  - End negotiation.
        """

        self._validate_price(seller_offer, "Seller offer")

        if mediator_suggestion is not None:
            self._validate_price(
                mediator_suggestion, "Mediator suggestion"
            )

        if not isinstance(no_feasible_deal, bool):
            raise ValueError("no_feasible_deal must be True or False.")

        if not self.negotiation_active:
            return self._decision(
                "no_deal", None, "Negotiation is no longer active."
            )

        if not self.started:
            raise RuntimeError(
                "Make the opening offer before receiving a seller offer."
            )

        self.current_round += 1
        seller_offer = float(seller_offer)

        # Mediator confirms that no agreement is possible.
        if no_feasible_deal:
            self.negotiation_active = False
            return self._decision(
                "no_deal", None,
                "Mediator confirmed there is no feasible agreement."
            )

        # Buyer can accept an offer covered by its previous offer.
        if seller_offer <= self.current_offer:
            self.negotiation_active = False
            return self._decision(
                "accept", seller_offer,
                "Seller's offer is at or below the buyer's previous offer."
            )

        # Calculate the buyer's independent target.
        if self.max_rounds == 1:
            progress = 1.0
        else:
            progress = min(
                (self.current_round - 1) / (self.max_rounds - 1),
                1.0
            )

        own_target = (
            self.opening_offer
            + (self.max_budget - self.opening_offer) * progress
        )

        own_target = min(own_target, self.max_budget)

        # A valid Mediator suggestion can guide the offer,
        # but cannot make the buyer exceed its own strategy.
        final_target = own_target

        if (
            mediator_suggestion is not None
            and self.current_offer < mediator_suggestion <= self.max_budget
        ):
            final_target = min(own_target, float(mediator_suggestion))

        # Accept if seller's offer is within the buyer's target.
        if seller_offer <= final_target:
            self.negotiation_active = False
            return self._decision(
                "accept", seller_offer,
                "Seller's offer is within the buyer's acceptable range."
            )

        # Stop if the maximum number of rounds is reached.
        if self.current_round >= self.max_rounds:
            self.negotiation_active = False
            return self._decision(
                "no_deal", None,
                "Maximum negotiation rounds reached."
            )

        # If the seller asks above the buyer's maximum,
        # reject this offer but keep negotiation active.
        if seller_offer > self.max_budget:
            return self._decision(
                "reject", None,
                "Seller's offer exceeds the buyer's maximum budget."
            )

        # Make a counteroffer without exceeding the budget.
        next_offer = max(self.current_offer, final_target)
        next_offer = min(next_offer, self.max_budget)

        # If there is no higher valid counteroffer, reject this offer.
        if next_offer <= self.current_offer:
            return self._decision(
                "reject", None,
                "Buyer cannot improve the current offer."
            )

        self.current_offer = next_offer

        return self._decision(
            "counter",
            next_offer,
            "Buyer calculated a counteroffer using its own strategy."
        )

    def reject_offer(self, reason="Buyer rejected the current offer."):
        """
        Reject only the current offer.
        Negotiation remains active.
        """

        if not self.negotiation_active:
            return self._decision(
                "no_deal", None, "Negotiation is no longer active."
            )

        return self._decision("reject", None, reason)

    def withdraw(self):
        """Buyer voluntarily ends the negotiation."""

        self.negotiation_active = False

        return self._decision(
            "no_deal", None, "Buyer withdrew from the negotiation."
        )

    def _decision(self, action, price, reason):

        return {
            "action": action,
            "price": price,
            "reason": reason,
            "round": self.current_round
        }
