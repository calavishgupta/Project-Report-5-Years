import streamlit as st
import pandas as pd
import os

def admin_dashboard():
    st.title("📊 Admin Dashboard – View All Project Reports")

    # Load submissions
    try:
        df = pd.read_csv("submissions.csv")
    except FileNotFoundError:
        st.warning("⚠️ No submissions found yet.")
        return

    if df.empty or "submitted_by" not in df.columns:
        st.info("ℹ️ No valid report submissions yet.")
        return

    # Sort by timestamp descending
    df = df.sort_values(by="timestamp", ascending=False)

    # Display table
    st.subheader("📋 Submitted Reports")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 📥 Download Each Report")

    for idx, row in df.iterrows():
        with st.expander(f"{idx+1}. {row['submitted_by']} ({row['timestamp']})"):
            file_path = row.get("file_path", "")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    file_name = os.path.basename(file_path)
                    st.download_button(
                        label="📥 Download Report",
                        data=f,
                        file_name=file_name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error("❌ File not found.")
