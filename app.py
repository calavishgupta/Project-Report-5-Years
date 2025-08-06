import streamlit as st
from login import login

# Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Guest option
guest = st.sidebar.button("Continue as Guest")

if guest:
    st.session_state.logged_in = True
    st.session_state.role = "guest"
    st.session_state.username = "Guest"
    st.session_state.email = None
    st.experimental_rerun()

# Login flow
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.write(f"👋 Hello, {st.session_state.username} ({st.session_state.role})")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())

    # Redirect based on role
    if st.session_state.role == "admin":
        st.subheader("🛠 Admin Dashboard (coming next)")
        # Will add view + download all reports here
    elif st.session_state.role == "user":
        st.subheader("📋 User Dashboard (coming next)")
        # Will add form + view their own submissions
    elif st.session_state.role == "guest":
        st.subheader("🚀 Guest Submission Form (coming next)")
        # Will add form only, no view

