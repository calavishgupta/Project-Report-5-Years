import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
# from user_dashboard import user_dashboard  # coming next
# from guest_form import guest_form         # coming next

# --- Session State Setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Sidebar & Guest Login ---
st.sidebar.title("Navigation")

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
    st.sidebar.write(f"👋 Hello, **{st.session_state.username}** ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    # --- Role-Based Redirection ---
    if st.session_state.role == "admin":
        admin_dashboard()

    elif st.session_state.role == "user":
        st.subheader("📋 User Dashboard (coming next)")
        st.info("This section will allow normal users to fill forms and track their submissions.")

    elif st.session_state.role == "guest":
        st.subheader("🚀 Guest Submission Form (coming next)")
        st.info("Guests can submit project report details without logging in.")
