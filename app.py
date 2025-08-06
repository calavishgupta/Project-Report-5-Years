st.session_state.clear()

import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard
from guest_form import guest_form  # ✅ Step 4 Guest Form

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Sidebar for Navigation ---
st.sidebar.title("🔐 Access")

# Guest Login Option
guest = st.sidebar.button("🚪 Continue as Guest")

if guest:
    st.session_state.logged_in = True
    st.session_state.role = "guest"
    st.session_state.username = "Guest"
    st.session_state.email = None
    st.experimental_rerun()

# --- Login Flow ---
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.markdown(f"👋 Welcome, **{st.session_state.username}** ({st.session_state.role})")
    
    # Logout
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    # --- Role-based Routing ---
    if st.session_state.role == "admin":
        admin_dashboard()

    elif st.session_state.role == "user":
        user_dashboard()

    elif st.session_state.role == "guest":
        guest_form()
