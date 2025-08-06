import streamlit as st
import pandas as pd
import os

def login():
    st.title("🔐 Login to Project Report System")

    # Safely load users
    try:
        if not os.path.exists("users.csv"):
            st.error("⚠️ 'users.csv' not found. Please upload the user database.")
            return

        users_df = pd.read_csv("users.csv")
    except Exception as e:
        st.error(f"⚠️ Error reading users.csv: {e}")
        return

    # Basic checks
    required_columns = {"username", "password", "email", "role"}
    if not required_columns.issubset(users_df.columns):
        st.error("⚠️ Invalid 'users.csv'. Required columns: username, password, email, role")
        return

    username = st.text_input("👤 Username").strip().lower()
    password = st.text_input("🔑 Password", type="password")
    login_btn = st.button("🔓 Login")

    if login_btn:
        user_row = users_df[users_df["username"].str.lower() == username]

        if not user_row.empty:
            stored_password = str(user_row.iloc[0]["password"])
            role = user_row.iloc[0]["role"].lower()
            email = user_row.iloc[0]["email"]

            if password == stored_password:
                st.success(f"✅ Welcome, {username.title()} ({role.capitalize()})")

                # Set session
                st.session_state.logged_in = True
                st.session_state.username = username.title()
                st.session_state.role = role
                st.session_state.email = email
                st.experimental_rerun()
            else:
                st.error("❌ Incorrect password.")
        else:
            st.error("❌ Username not found.")
