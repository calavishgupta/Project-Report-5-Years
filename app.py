import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard
from guest_form import guest_form

# --- Session Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.email = None

# --- Sidebar Navigation ---
st.sidebar.title("🔐 Access Control")

# Guest login button
if not st.session_state.logged_in:
    if st.sidebar.button("🚪 Continue as Guest"):
        st.session_state.logged_in = True
        st.session_state.role = "guest"
        st.session_state.username = "Guest"
        st.session_state.email = None
        st.experimental_rerun()

# --- Show Login Page ---
if not st.session_state.logged_in:
    login()

# --- Authenticated View ---
else:
    st.sidebar.markdown(f"👋 Welcome, **{st.session_state.username}** ({st.session_state.role})")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    # Routing based on user role
    role = st.session_state.get("role")

    if role == "admin":
        admin_dashboard()
    elif role == "user":
        user_dashboard()
    elif role == "guest":
        guest_form()
    else:
        st.error("🚫 Invalid role. Please log in again.")
