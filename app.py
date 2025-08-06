import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard
from guest_form import guest_form

# --- Session Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login Not Done ---
if not st.session_state.logged_in:
    st.sidebar.title("🔐 Login Panel")

    # Guest Option
    if st.sidebar.button("🚪 Continue as Guest"):
        st.session_state.logged_in = True
        st.session_state.role = "guest"
        st.session_state.username = "Guest"
        st.session_state.email = None
        st.experimental_rerun()

    login()

    # Trigger rerun AFTER login success
    if st.session_state.get("login_success"):
        st.session_state.pop("login_success")
        st.experimental_rerun()

# --- Post Login View ---
else:
    st.sidebar.title("🔐 Access")
    st.sidebar.markdown(f"👋 Welcome, **{st.session_state.username}** ({st.session_state.role})")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    # Role-based routing
    if st.session_state.role == "admin":
        admin_dashboard()
    elif st.session_state.role == "user":
        user_dashboard()
    elif st.session_state.role == "guest":
        guest_form()
    else:
        st.error("❌ Unknown role detected. Contact Admin.")
