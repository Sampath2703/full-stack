import streamlit as st
import requests


backend_url = "http://127.0.0.1:8000"

st.set_page_config(page_title="Register - SOC AI")

st.title("🆕 Create Account")

with st.form("register_form"):
    Name= st.text_input("Name")
    Email=st.text_input("Email")
    password = st.text_input("Password", type="password")

    btn = st.form_submit_button("Register")

    if btn:
        payload = {
            "Name":Name,
            "Email":Email,
            "Password":password
        }
        res=requests.post(f"{backend_url}/register", json=payload)


        if res.status_code == 200:
            st.write(res.json())