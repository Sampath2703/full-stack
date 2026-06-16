def threat_agent(logs):

    analyze_logs = []
    threats = []

    for log in logs:
        event = log.get("event", "")
        user = log.get("user_eamil", "")



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

        # 📊 Add enrichment (SOC intelligence style)
        log["alert_message"] = f"{event} detected for {user}"

        analyze_logs.append(log)

        if log["is_threat"]:
            threats.append(log)

    return {
        "total_logs": len(logs),
        "total_threats": len(threats),
        "threats": threats,
        "analyzed_logs": analyze_logs
    }