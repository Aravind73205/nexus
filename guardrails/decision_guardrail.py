def review_decision_guardrail(output):
    text = output.raw.lower()

    if "approve" in text or "reject" in text:
        return True, output.raw

    return False, "Decision must contain approve or reject"