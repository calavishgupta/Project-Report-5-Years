import streamlit as st
import pandas as pd

def login():
    st.title("🔐 Login to Project Report System")

    try:
        users_df = pd.read_csv("users.csv")
    except FileNotFoundError:
        st.error("❌ users.csv file not found.")
        return

    users_df["username"] = users_df["username"].str.lower()

    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        user_row = users_df[users_df["username"] == username]

        if not user_row.empty:
            stored_password = str(user_row.iloc[0]["password"]).strip()
            role = user_row.iloc[0]["role"].lower()
            email = user_row.iloc[0]["email"]

            if password.strip() == stored_password:
                st.success(f"✅ Logged in as {username} ({role})")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.email = email
                st.session_state.login_success = True  # tell app.py to rerun
            else:
                st.error("❌ Incorrect password")
        else:
            st.error("❌ Username not found")
