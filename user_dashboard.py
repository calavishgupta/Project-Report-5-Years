import streamlit as st
import pandas as pd
from report_form import show_report_form  # form to be reused

def user_dashboard():
    st.title("📋 User Dashboard – Submit and Track Reports")

    # Show the form to fill new report
    st.header("📝 Fill New Project Report")
    show_report_form(user_role="user")

    st.divider()

    # View past submissions (without download)
    st.subheader("📜 Your Submitted Reports")

    try:
        df = pd.read_csv("submissions.csv")
    except FileNotFoundError:
        st.info("You haven't submitted any reports yet.")
        return

    user_email = st.session_state.email
    user_data = df[df["email"] == user_email]

    if user_data.empty:
        st.info("You haven't submitted any reports yet.")
    else:
        st.dataframe(user_data[["submitted_by", "timestamp"]], use_container_width=True)
        st.caption("Note: Only admins can download the reports.")
