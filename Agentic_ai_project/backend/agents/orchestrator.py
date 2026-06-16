from agents.log_agent import log_agent
from agents.threats_agent import threat_agent
from llm.llm import llm_analyze


def orchestrate(logs):

    cleaned_logs = log_agent(logs)

    threat_data = threat_agent(cleaned_logs)

    ai_output = llm_analyze(threat_data)

    return {
        "logs": cleaned_logs,
        "threat_analysis": threat_data,
        "ai_insight": ai_output
    }