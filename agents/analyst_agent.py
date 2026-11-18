
import math


def analyze_message(message, confidence_threshold=50.0):
    """
    Analyze a negotiation message using the trained BiLSTM model.

    Returns the predicted intent, confidence, interpretation,
    and any rule-based warnings.
    """

    # Validate the input message.
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Message must be a non-empty string.")

    if (
        isinstance(confidence_threshold, bool)
        or not isinstance(confidence_threshold, (int, float))
        or not math.isfinite(confidence_threshold)
        or not 0 <= confidence_threshold <= 100
    ):
        raise ValueError("Confidence threshold must be between 0 and 100.")

    # Interpret the model's intent labels.
    interpretations = {
        "agree": "The person appears to agree with the proposal.",
        "counter-price": "The person is suggesting a different price.",
        "disagree": "The person appears to disagree with the proposal.",
        "inform": "The person is providing information.",
        "init-price": "The person is introducing an initial price.",
        "inquiry": "The person is asking a question.",
        "insist": "The person is strongly maintaining their position.",
        "intro": "The person is starting the conversation.",
        "vague-price": "The person is mentioning a price unclearly."
    }

    # Import the trained model only when analysis is requested.
    # This prevents model-loading errors from stopping other imports.
    try:
        from models.intent_predictor import predict_intent

        predicted_intent, confidence_score = predict_intent(message)

    except Exception as error:
        return {
            "success": False,
            "predicted_intent": None,
            "confidence_score": None,
            "interpretation": "Intent prediction is currently unavailable.",
            "warnings": [
                f"Could not use the trained intent model: {error}"
            ]
        }

    # Validate the model's output.
    if predicted_intent not in interpretations:
        raise ValueError(
            f"The model returned an unknown intent: {predicted_intent}"
        )

    if (
        isinstance(confidence_score, bool)
        or not isinstance(confidence_score, (int, float))
        or not math.isfinite(confidence_score)
        or not 0 <= confidence_score <= 100
    ):
        raise ValueError("The model returned an invalid confidence score.")

    # Interpret the prediction and generate rule-based warnings.
    warnings = []

    if confidence_score < confidence_threshold:
        warnings.append(
            "Low prediction confidence. Treat the predicted intent cautiously."
        )

    if predicted_intent == "disagree":
        warnings.append(
            "The person disagrees with the current proposal."
        )

    elif predicted_intent == "insist":
        warnings.append(
            "The person is maintaining a firm negotiation position."
        )

    elif predicted_intent == "vague-price":
        warnings.append(
            "The price is unclear. Further clarification may be needed."
        )

    return {
        "success": True,
        "predicted_intent": predicted_intent,
        "confidence_score": round(float(confidence_score), 2),
        "interpretation": interpretations[predicted_intent],
        "warnings": warnings
    }


if __name__ == "__main__":

    test_message = "Can you reduce the price to 3000?"

    result = analyze_message(test_message)

    print("DEALWEAVER AI - Analyst Agent")
    print("--------------------------------")
    print("Message:", test_message)

    for key, value in result.items():
        print(f"{key}: {value}")
