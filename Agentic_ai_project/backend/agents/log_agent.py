def log_agent(logs):
    return [
        {
            "id": log.get("id"),
            "user_email": log.get("user_email"),
            "event": log.get("event"),
            "source_ip": log.get("source_ip"),
            "log_data": log.get("log_data"),
            "log_type": log.get("log_type"),
            "severity": log.get("severity"),
            "is_threat": log.get("is_threat"),
            "created_at": log.get("created_at"),
        }
        for log in logs
    ]