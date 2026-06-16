import streamlit as st
import requests

backend_url = "http://127.0.0.1:8000"

st.set_page_config(page_title="SOC AI Dashboard", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("Please Login First")
    st.switch_page("app.py")
    st.stop()

user = st.session_state.get("user")

res = requests.get(f"{backend_url}/run_pipeline")

if res.status_code == 200:
    data = res.json().get("data", {})
else:
    data = {}

logs = data.get("logs", [])
threat_data = data.get("threat_analysis", {})
ai_insight = data.get("ai_insight", {})

threats = threat_data.get("total_threats", 0)
threat_list = threat_data.get("threats", [])

st.title("🛡️ SOC AI Dashboard")

st.subheader(f"Welcome {user['Name']}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Logs", len(logs))

with col2:
    st.metric("Threats Detected", threats)

with col3:
    risk = "HIGH" if threats > 0 else "LOW"
    st.metric("Risk Level", risk)

st.subheader("🧠 AI Insight")

st.info(ai_insight.get("analysis", "No AI response"))

st.subheader("🚨 Threats")

for t in threat_list:
    st.error(f"{t.get('event')} | {t.get('risk_level')}")

st.subheader("📄 Logs")

for log in logs[-5:]:
    st.write(f"{log['event']} - {log['log_data']}")