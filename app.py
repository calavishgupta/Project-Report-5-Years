import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard
from guest_form import guest_form

# --- Session Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "login_success" not in st.session_state:
    st.session_state.login_success = False

# --- Redirect on Login Success ---
if st.session_state.login_success:
    st.session_state.login_success = False  # reset flag
    st.rerun()  # this is safe here as it's outside widget callbacks

# --- Show Login Interface ---
if not st.session_state.logged_in:
    st.sidebar.title("🔐 Login Panel")

    if st.sidebar.button("🚪 Continue as Guest"):
        st.session_state.logged_in = True
        st.session_state.role = "guest"
        st.session_state.username = "Guest"
        st.session_state.email = None
        st.session_state.login_success = True  # trigger rerun
        st.stop()

    login()
    st.stop()

# --- Post Login Interface ---
st.sidebar.title("🔐 Access")
st.sidebar.markdown(f"👋 Welcome, **{st.session_state.username}** ({st.session_state.role})")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# --- Role-based Routing ---
if st.session_state.role == "admin":
    admin_dashboard()
elif st.session_state.role == "user":
    user_dashboard()
elif st.session_state.role == "guest":
    guest_form()
else:
    st.error("❌ Unknown role detected. Contact Admin.")
