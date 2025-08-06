import streamlit as st
import pandas as pd

def login():
    st.title("🔐 Login to Project Report System")

    # Load users from CSV
    users_df = pd.read_csv("users.csv")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        user_row = users_df[users_df["username"] == username]

        if not user_row.empty:
            stored_password = user_row.iloc[0]["password"]
            role = user_row.iloc[0]["role"]
            email = user_row.iloc[0]["email"]

            if password == stored_password:
                st.success(f"✅ Logged in as {username} ({role})")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.email = email
                st.experimental_rerun()
            else:
                st.error("❌ Incorrect password")
        else:
            st.error("❌ Username not found")
