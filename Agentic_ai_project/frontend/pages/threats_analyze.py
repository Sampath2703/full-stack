def threat_anayze(logs):
    analyze_logs = []
    threats = []


    for log in logs:
        event = log.get("event", "")

        if event == "LOGIN_SUCCESS":
            log["risk_level"] = "LOW"
            log["is_threat"] = False

        elif event == "LOGIN_FAILED":
            log["risk_level"] = "MEDIUM"
            log["is_threat"] = True

        elif event == "MULTIPLE_FAILED_ATTEMPTS":
            log["risk_level"] = "HIGH"
            log["is_threat"] = True

        elif event == "UNAUTHORIZED_ACCESS":
            log["risk_level"] = "CRITICAL"
            log["is_threat"] = True

        else:
            log["risk_level"] = "LOW"
            log["is_threat"] = False

        analyze_logs.append(log)

        if log["is_threat"]:
            threats.append(logs)

    return{
        "analyze_logs": analyze_logs,
        "threats":threats,
        "total_threats":len(threats)

    }