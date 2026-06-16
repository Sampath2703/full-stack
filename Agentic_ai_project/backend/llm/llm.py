import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def llm_analyze(threat_data):

    prompt = f"""
    You are a SOC AI Analyst.

    Threat Summary:
    {threat_data}

    Provide:
    - Security summary
    - Risk explanation
    - Action steps
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "analysis": response.choices[0].message.content
    }