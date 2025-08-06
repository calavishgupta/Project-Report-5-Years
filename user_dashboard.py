import streamlit as st
import pandas as pd
import os
from report_form import show_report_form

def user_dashboard():
    st.title("👤 User Dashboard – Submit and Track Your Reports")

    # --- New Report Submission ---
    st.header("📝 Fill a New Project Report")
    show_report_form(user_role="user")

    st.divider()

    # --- Past Submissions ---
    st.subheader("📜 Your Submitted Reports")

    try:
        df = pd.read_csv("submissions.csv")
    except FileNotFoundError:
        st.info("ℹ️ No reports found yet.")
        return

    if df.empty or "email" not in df.columns:
        st.warning("⚠️ Submission file found, but no valid data.")
        return

    user_email = st.session_state.get("email", "").lower()
    user_data = df[df["email"].str.lower() == user_email]

    if user_data.empty:
        st.info("📭 You haven't submitted any reports yet.")
        return

    # Sort by latest
    user_data = user_data.sort_values(by="timestamp", ascending=False)

    st.dataframe(user_data[["submitted_by", "timestamp"]], use_container_width=True)

    st.markdown("### 📥 Download Your Reports")
    for idx, row in user_data.iterrows():
        with st.expander(f"{idx+1}. Submitted on {row['timestamp']}"):
            file_path = row.get("file_path", "")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Report",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error("❌ File not found.")
