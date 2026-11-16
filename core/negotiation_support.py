
from agents.mediator_agent import check_feasibility
from agents.analyst_agent import analyze_message
from core.risk_analyzer import analyze_risks
from genai.response_generator import generate_response


def analyze_negotiation(
    message,
    buyer_max,
    seller_min,
    current_offer=None,
    rejection_count=0,
    previous_offers=None,
    stalled_threshold=3,
    confidence_threshold=50.0
):
    """
    Coordinate all four Member 3 modules.

    Returns a structured result for the application UI.
    Private buyer and seller limits are never included
    in the returned result.
    """

    # 1. MEDIATOR AGENT: Check price feasibility.
    mediator_result = check_feasibility(
        buyer_max=buyer_max,
        seller_min=seller_min,
        proposed_price=current_offer
    )

    mediator_suggestion = mediator_result["mediator_suggestion"]

    # 2. ANALYST AGENT: Predict the message's intent.
    analyst_result = analyze_message(
        message=message,
        confidence_threshold=confidence_threshold
    )

    # 3. RISK ANALYZER: Detect negotiation risks.
    risk_result = analyze_risks(
        buyer_max=buyer_max,
        seller_min=seller_min,
        current_offer=current_offer,
        rejection_count=rejection_count,
        previous_offers=previous_offers,
        stalled_threshold=stalled_threshold
    )

    # 4. GEN AI: Generate a response if intent analysis succeeded.
    if analyst_result["success"]:
        ai_result = generate_response(
            message=message,
            predicted_intent=analyst_result["predicted_intent"],
            mediator_suggestion=mediator_suggestion
        )
    else:
        ai_result = {
            "success": False,
            "response": None,
            "source": None
        }

    # Return only information needed by the application.
    # Do not expose buyer_max or seller_min.
    return {
        "success": analyst_result["success"] and ai_result["success"],

        "mediator": {
            "feasible": mediator_result["feasible"],
            "no_feasible_deal": mediator_result["no_feasible_deal"],
            "suggestion": mediator_suggestion,
            "proposed_price_feasible":
                mediator_result["proposed_price_feasible"],
            "reason": mediator_result["reason"]
        },

        "analyst": analyst_result,

        "risks": risk_result,

        "ai_response": ai_result
    }


if __name__ == "__main__":

    result = analyze_negotiation(
        message="Your price is too high. I can offer 3500.",
        buyer_max=4000,
        seller_min=3000,
        current_offer=3500,
        rejection_count=0,
        previous_offers=[3200, 3400, 3500]
    )

    print("DEALWEAVER AI - INTEGRATED NEGOTIATION SUPPORT")
    print("------------------------------------------------")

    for section, details in result.items():
        print(f"\n{section.upper()}:")

        if isinstance(details, dict):
            for key, value in details.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {details}")
