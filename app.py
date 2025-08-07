import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard
from guest_form import guest_form

# Import the scheme calculator's main function
from scheme_calculator.app import main as scheme_calculator_main

# --- Session Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Show Login Interface ---
if not st.session_state.logged_in:
    login_complete = login()  # Returns True if login or guest login is successful

    if login_complete:
        st.rerun()
    st.stop()

# --- Sidebar Navigation ---
st.sidebar.title("🔒 Access")
st.sidebar.markdown(f"👋 Welcome, **{st.session_state.username}** ({st.session_state.role})")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# Add navigation options
page = st.sidebar.radio(
    "Navigate",
    options=["Dashboard", "Scheme Calculator"]
)

if page == "Scheme Calculator":
    scheme_calculator_main()
else:
    # --- Role-based Routing ---
    if st.session_state.role == "admin":
        admin_dashboard()
    elif st.session_state.role == "user":
        user_dashboard()
    elif st.session_state.role == "guest":
        guest_form()
    else:
        st.error("❌ Unknown role detected. Contact Admin.")
