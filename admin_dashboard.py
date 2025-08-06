import streamlit as st
import pandas as pd
import os

def admin_dashboard():
    st.title("📊 Admin Dashboard – View All Project Reports")

    try:
        df = pd.read_csv("submissions.csv")
    except FileNotFoundError:
        st.warning("No submissions found yet.")
        return

    if df.empty:
        st.info("No reports submitted yet.")
        return

    st.dataframe(df)

    st.markdown("### 📥 Download Submitted Reports")
    for idx, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([2, 3, 3, 2])
        with col1:
            st.write(f"{idx+1}.")
        with col2:
            st.write(f"**{row['submitted_by']}**")
        with col3:
            st.write(row["timestamp"])
        with col4:
            if os.path.exists(row["file_path"]):
                with open(row["file_path"], "rb") as f:
                    st.download_button(
                        label="📥 Download",
                        data=f,
                        file_name=os.path.basename(row["file_path"]),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error("File missing")
