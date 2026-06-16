def threat_agent(logs):

    threats = []

    for log in logs:
        event = log.get("event", "")

        if event == "LOGIN_FAILED":
            log["risk_level"] = "MEDIUM"
            log["is_threat"] = True

        elif event in ["MULTIPLE_ATTEMPTS", "UNAUTHORIZED_ACCESS"]:
            log["risk_level"] = "CRITICAL"
            log["is_threat"] = True

        else:
            log["risk_level"] = "LOW"
            log["is_threat"] = False

        if log["is_threat"]:
            threats.append(log)

    return {
        "total_threats": len(threats),
        "threats": threats,
        "analyzed_logs": logs
    }