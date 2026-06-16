import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key = "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"
)

def llm_analyze(threat_data):
    threats = threat_data.get("threats", [])
    total = threat_data.get("total_threats", 0)


    prompt = f"""
You are a SOC (Security Operations Center) AI assistant.

    Analyze this security data:
    Total Threats: {total}
    Threat Details: {threats}

    Give:
    1. Summary of attack
    2. Risk explanation
    3. Action plan for security team

"""
    

    response = client.chat.completions.create(
        model = "llama3-70b-8192",
        message = [{
            "role":"user",
            "content":prompt
        }]
    )

    return{
        "analysis": response.choice[0].message.content
    }