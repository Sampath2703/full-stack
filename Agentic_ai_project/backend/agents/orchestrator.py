from agents.log_agent import log_agent
from agents.threats_agent import threat_agent
from llm.llm import llm_analyze


def orchestrate(logs):

    logs = log_agent(logs)
    threat_data = threat_agent(logs)
    ai = llm_analyze(threat_data)

    return {
        "logs": logs,
        "threat_analysis": threat_data,
        "ai_insight": ai
    }