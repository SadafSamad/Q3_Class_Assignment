import streamlit as st
import hashlib
import time
from cryptography.fernet import Fernet

# Set the page config
st.set_page_config(page_title="Secure Data System", layout="centered")

# Key Generation
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# In-memory data storage
stored_data = {}

# Session State Initialization
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'reauth_required' not in st.session_state:
    st.session_state.reauth_required = False

# Hashing function
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt function
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Decrypt function
def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)
    if encrypted_text in stored_data:
        if stored_data[encrypted_text]['passkey'] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
    st.session_state.failed_attempts += 1
    if st.session_state.failed_attempts >= 3:
        st.session_state.reauth_required = True
    return None

# UI Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e2f;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #4CAF50;
    }
    .subheader {
        font-size: 26px;
        margin-top: 20px;
        color: #FFD700;
    }
    .btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 18px;
        cursor: pointer;
        border-radius: 8px;
        transition: background-color 0.3s;
    }
    .btn:hover {
        background-color: #45a049;
    }
    .card {
        background-color: #2C2F48;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-top: 20px;
    }
    .expander {
        background-color: #333;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Input field styling */
    .stTextInput, .stTextArea {
        background-color: #3e3e4d;
        color: #fff;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #4CAF50;
        margin-top: 10px;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #3e3e4d;
        color: #fff;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2C2F48;
        color: #fff;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .css-1d391kg .streamlit-expanderHeader {
        color: #4CAF50;
    }
    .css-1d391kg .css-14xtw13 {
        background-color: #3e3e4d;
        color: #fff;
        border-radius: 8px;
        padding: 8px;
    }
    .css-1d391kg .stSelectbox select {
        background-color: #3e3e4d;
        color: #fff;
        border: none;
    }
    
    /* Sidebar menu styles */
    .css-1d391kg .stSelectbox {
        margin-top: 20px;
    }
    .css-1d391kg .streamlit-expanderHeader {
        padding: 10px;
        background-color: #333;
        color: #4CAF50;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🛡️ Secure Data Encryption System</div>', unsafe_allow_html=True)

# Navigation
menu = ["Home", "Store Data", "Retrieve Data"]
if st.session_state.reauth_required:
    menu = ["Login"] + menu
choice = st.sidebar.selectbox("Navigate", menu)

# Home Page
if choice == "Home":
    st.markdown("<div class='subheader'>🏠 Welcome</div>", unsafe_allow_html=True)
    st.write("Use this app to **securely store and retrieve your data** using a passkey. Encryption is done using **Fernet** for secure data storage.")
    st.write("Ensure to keep your passkey safe. Don't share it with anyone!")

# Store Data
elif choice == "Store Data":
    st.markdown("<div class='subheader'>📂 Store Data Securely</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        user_data = st.text_area("🔸 Enter Data to Encrypt", height=150)
        passkey = st.text_input("🔐 Enter Passkey", type="password")
        if st.button("🔒 Encrypt & Store", key="store_data", help="Click to encrypt and store your data securely.", use_container_width=True):
            if user_data and passkey:
                hashed_passkey = hash_passkey(passkey)
                encrypted_text = encrypt_data(user_data)
                stored_data[encrypted_text] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}
                st.success("✅ Data stored successfully!")
                with st.expander("🔍 View Encrypted Text", expanded=True):
                    st.code(encrypted_text, language='text')
            else:
                st.error("❗ Please fill in all fields.")
        st.markdown('</div>', unsafe_allow_html=True)

# Retrieve Data
elif choice == "Retrieve Data":
    if st.session_state.reauth_required:
        st.warning("🔐 Too many failed attempts. Please login again.")
    else:
        st.markdown("<div class='subheader'>🔍 Retrieve Data</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            encrypted_text = st.text_area("🔸 Enter Encrypted Text", height=150)
            passkey = st.text_input("🔐 Enter Passkey", type="password")
            if st.button("🔓 Decrypt", key="decrypt_data"):
                if encrypted_text and passkey:
                    result = decrypt_data(encrypted_text, passkey)
                    if result:
                        st.success("✅ Decryption Successful!")
                        st.code(result, language='text')
                    else:
                        remaining = 3 - st.session_state.failed_attempts
                        st.error(f"❌ Incorrect passkey! {remaining} attempt(s) left.")
                        if st.session_state.reauth_required:
                            time.sleep(1)
                            st.experimental_rerun()
                else:
                    st.error("❗ Please enter both fields.")
            st.markdown('</div>', unsafe_allow_html=True)

# Login Page
elif choice == "Login":
    st.markdown("<div class='subheader'>🔑 Reauthorize</div>", unsafe_allow_html=True)
    login_pass = st.text_input("Enter Master Password", type="password")
    if st.button("Login", key="login"):
        if login_pass == "admin123":
            st.session_state.failed_attempts = 0
            st.session_state.reauth_required = False
            st.success("✅ Login Successful. Redirecting...")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect Password")
