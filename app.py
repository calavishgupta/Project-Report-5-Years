import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard
from guest_form import guest_form

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login Flow ---
if not st.session_state.logged_in:
    login()
else:
    # Sidebar for navigation
    st.sidebar.title("🔐 Access")
    
    st.sidebar.markdown(f"👋 Welcome, **{st.session_state.username}** ({st.session_state.role})")

    # Guest option should only appear BEFORE login
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    # Role-based Routing
    if st.session_state.role == "admin":
        admin_dashboard()
    elif st.session_state.role == "user":
        user_dashboard()
    elif st.session_state.role == "guest":
        guest_form()

# Guest Login Option – shown only when not logged in
if not st.session_state.logged_in:
    if st.sidebar.button("🚪 Continue as Guest"):
        st.session_state.logged_in = True
        st.session_state.role = "guest"
        st.session_state.username = "Guest"
        st.session_state.email = None
        st.experimental_rerun()
