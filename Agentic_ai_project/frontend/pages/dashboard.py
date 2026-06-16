import streamlit as st
import requests

backend_url = "http://127.0.0.1:8000"

st.set_page_config(page_title="Security Operation Center AI Dashboard", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("Please Login First")
    st.switch_page("app.py")
    st.stop()

user = st.session_state.get("user")

res = requests.get(f"{backend_url}/run_pipeline")

if res.status_code == 200:
    data = res.json().get("data", {})
    logs = data.get("logs", [])
    threat_data = data.get("threat_analysis", {})
else:
    logs = []
    threat_data = {}

ai_insight = data.get("ai_insight", {}) if res.status_code == 200 else {}

threats = threat_data.get("total_threats", 0)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .block-container {
        background-color: rgba(0, 0, 0, 0.65);
        padding: 2rem;
        border-radius: 12px;
        padding-left: 30px;
    }

    h1, h2, h3, p, label {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ Security Operation Center AI Security Dashboard")

st.markdown("---")

st.subheader(f"Welcome {user['Name']}")

threats = 0
incidents = 0

for log in logs:
    event = log.get("event", "")

    if event == "LOGIN_FAILED":
        threats += 1

    if event in ["LOGIN_FAILED", "MULTIPLE_ATTEMPTS", "UNAUTHORIZED_ACCESS"]:
        incidents += 1

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Logs", len(logs))

with col2:
    st.metric("Threats Detected", threats)

with col3:
    st.metric("Incidents", incidents)

st.markdown("---")

st.subheader("🧠 AI Security Insight")

if ai_insight:
    st.info(ai_insight.get("analysis", ""))
else:
    st.warning("AI engine not responding")

st.markdown("---")

st.subheader("📄 Recent Logs")

if logs:
    for log in logs[-5:][::-1]:
        if log.get("event") == "LOGIN_FAILED":
            st.error(f"{log['event']} - {log['log_data']}")
        else:
            st.success(f"{log['event']} - {log['log_data']}")

st.markdown("---")

st.subheader("🧠 SOC Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📄 Log Analysis")

with col2:
    st.warning("🚨 Threat Detection")

with col3:
    st.success("📊 Incident Reports")

st.markdown("---")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("app.py")