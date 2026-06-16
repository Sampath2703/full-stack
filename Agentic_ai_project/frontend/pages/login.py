import streamlit as st
import requests

backend_url = "http://127.0.0.1:8000"

st.set_page_config(page_title="Login - SOC AI")

st.title("🔑 Login")

with st.form("login_form"):
    Email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    btn = st.form_submit_button("login")

if btn:
    payload = {
        "Email": Email,
        "Password": password
    }

    res = requests.post(f"{backend_url}/login", json=payload)

    if res.status_code == 200:

        data = res.json()

        st.session_state["logged_in"] = True
        st.session_state["user"] = data["user"]

        st.switch_page("pages/dashboard.py")
    else:
        st.warning("Invalid Credentials")