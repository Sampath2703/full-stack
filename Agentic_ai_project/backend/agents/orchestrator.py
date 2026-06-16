from agents.log_agent import log_agent
from agents.threats_agent import threat_agent
from llm.llm import llm_analyze


def orchestrate(logs):
    cleaned_logs = log_agent(logs)

    threat_output = threat_agent(cleaned_logs)

    llm_output = llm_analyze(threat_output)

    return{
        "logs": cleaned_logs,
        "threat_analysis": threat_output,
        "ai_insight": llm_output
    }