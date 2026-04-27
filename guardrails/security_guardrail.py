def security_review_output_guardrail(output):
    data = output.json_dict

    valid_levels = ["low", "medium", "high"]

    if data["highest_risk"] not in valid_levels:
        return False, "Invalid highest_risk value"

    risks = [v["risk_level"] for v in data["security_vulnerabilities"]]

    for r in risks:
        if r not in valid_levels:
            return False, f"Invalid risk level: {r}"

    if data["highest_risk"] not in risks:                                  
        return False, "highest_risk not matching vulnerabilities"

    if max(risks, key=valid_levels.index) != data["highest_risk"]:
        return False, "highest_risk mismatch"

    return True, data