import streamlit as st

st.set_page_config(page_title="SOC AI System", layout="wide")

st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.title {
    text-align: center;
    color: black;
    margin-top: 150px;
    font-size: 60px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: blue;
    font-size: 24px;
    background-color:black;
    width:500px;
    margin-left: 150px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🛡️ Security Operations Center AI System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Security Operations Center</div>',
    unsafe_allow_html=True
)

st.write("")
st.write("")
st.write("")

col1, col2, col3 = st.columns([1,1,1])

with col2:
    if st.button("🔑 Login", use_container_width=True):
        st.switch_page("pages/login.py")

    if st.button("🆕 Register", use_container_width=True):
        st.switch_page("pages/registration.py")