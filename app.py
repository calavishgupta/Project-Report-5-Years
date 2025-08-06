import streamlit as st
from login import login
from admin_dashboard import admin_dashboard
from user_dashboard import user_dashboard
# from guest_form import guest_form  # (Coming next in Step 4)

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Sidebar ---
st.sidebar.title("🔐 Access")
guest = st.sidebar.button("🚪 Continue as Guest")

if guest:
    st.session_state.logged_in = True
    st.session_state.role = "guest"
    st.session_state.username = "Guest"
    st.session_state.email = None
    st.experimental_rerun()

# --- Login Workflow ---
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.markdown(f"👋 Welcome, **{st.session_state.username}** ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    # --- Role-Based Views ---
    if st.session_state.role == "admin":
        admin_dashboard()

    elif st.session_state.role == "user":
        user_dashboard()

    elif st.session_state.role == "guest":
        st.subheader("🚀 Guest Submission Form (coming next)")
        st.info("This section will allow guest users to submit a project report without logging in.")
