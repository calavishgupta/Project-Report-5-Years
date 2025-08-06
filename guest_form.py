import streamlit as st
from report_form import show_report_form

def guest_form():
    st.title("🚀 Guest Submission – Project Report")
    st.info("🔒 Note: As a guest, your submission is anonymous and cannot be tracked later.")
    
    # Call shared form logic with role flag
    show_report_form(user_role="guest")
