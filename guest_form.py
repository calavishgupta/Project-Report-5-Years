import streamlit as st
from report_form import show_report_form

def guest_form():
    st.title("🚀 Guest Submission – Project Report")
    st.warning("Note: As a guest, you will not be able to track your submissions later.")
    show_report_form(user_role="guest")
