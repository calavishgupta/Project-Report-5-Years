import streamlit as st
from openpyxl import load_workbook
import yagmail
import tempfile
import os
from datetime import datetime
import pandas as pd

def show_report_form(user_role="guest"):
    entered_by = st.text_input("Your Name").strip().title()
    if not entered_by:
        st.stop()

    st.header("Step 1: Basic Details")
    firm_name = st.text_input("Firm Name").upper()
    firm_address = st.text_input("Firm Address").upper()
    nature_of_business = st.text_input("Nature of Business").upper()
    building_status = st.selectbox("Building Rented/Owned", ["RENTED", "OWNED"])
    area_sqft = st.number_input("Area in sq. ft", min_value=0.0, step=1.0)
    rent_rs = st.number_input("Rent in Rs.", min_value=0.0, step=100.0) if building_status == "RENTED" else 0.0

    st.header("Step 2: Financial Parameters")
    margin = st.number_input("Margin %", min_value=0.0, max_value=100.0) / 100
    subsidy = st.number_input("Subsidy %", min_value=0.0, max_value=100.0) / 100
    term_loan = st.number_input("Term Loan Interest %", min_value=0.0, max_value=100.0) / 100
    cc_rate = st.number_input("CC Interest %", min_value=0.0, max_value=100.0) / 100

    st.header("Step 3: Plant & Machinery")
    if 'item_count' not in st.session_state:
        st.session_state.item_count = 1

    def add_item():
        if st.session_state.item_count < 11:
            st.session_state.item_count += 1

    item_data = []
    total_pm_value = 0

    for i in range(st.session_state.item_count):
        st.markdown(f"**Item {i+1}**")
        cols = st.columns(3)
        with cols[0]:
            item_name = st.text_input(f"Item Name {i+1}", key=f"name_{i}").upper()
        with cols[1]:
            qty = st.number_input(f"Qty {i+1}", min_value=0.0, step=1.0, key=f"qty_{i}")
        with cols[2]:
            rate = st.number_input(f"Rate {i+1}", min_value=0.0, step=0.1, key=f"rate_{i}")

        if item_name:
            total = qty * rate
            total_pm_value += total
            item_data.append({
                "serial": i + 1,
                "name": item_name,
                "qty": qty,
                "rate": rate
            })

    if st.session_state.item_count < 11:
        st.button("➕ Add More Items", on_click=add_item)

    st.header("Step 4: Other Fixed Assets")
    furniture_value = st.number_input("Furniture & Fixture Value (₹)", min_value=0.0, step=100.0)
    electrical_value = st.number_input("Electrical Equipments Value (₹)", min_value=0.0, step=100.0)

    st.header("💰 Summary")
    grand_total = total_pm_value + furniture_value + electrical_value
    st.write(f"**Total Plant & Machinery Value:** ₹{total_pm_value:,.2f}")
    st.write(f"**Total Furniture & Fixture Value:** ₹{furniture_value:,.2f}")
    st.write(f"**Total Electrical Equipments Value:** ₹{electrical_value:,.2f}")
    st.subheader(f"**➡️ Grand Total: ₹{grand_total:,.2f}**")

    if st.button("📤 Submit & Generate Report"):
        try:
            template_path = "Project Report Format.xlsx"
            wb = load_workbook(template_path)
            sheet = wb["Basic Details"]

            # Basic info
            sheet["C3"] = firm_name
            sheet["C4"] = firm_address
            sheet["C5"] = nature_of_business
            sheet["C8"] = building_status
            sheet["C9"] = area_sqft
            sheet["C10"] = rent_rs
            sheet["C11"] = margin
            sheet["C12"] = subsidy
            sheet["C13"] = term_loan
            sheet["C14"] = cc_rate

            # P&M entries
            for idx, item in enumerate(item_data):
                row = 19 + idx
                sheet[f"B{row}"] = item["serial"]
                sheet[f"C{row}"] = item["name"]
                sheet[f"D{row}"] = item["qty"]
                sheet[f"E{row}"] = item["rate"]

            # Other fixed assets
            sheet["F37"] = furniture_value
            sheet["F40"] = electrical_value

            # Hide sheet
            sheet.sheet_state = "hidden"

            # Save file
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/tmp/report_{entered_by.replace(' ', '_')}_{now}.xlsx"
            wb.save(filename)

            # Email
            yag = yagmail.SMTP(user="calavishgupta25@gmail.com", password="geli tejz dxiq vtyo")
            subject = f"{entered_by} - Project Report"
            yag.send(
                to="calavishgupta25@gmail.com",
                subject=subject,
                contents="Project report is attached.",
                attachments=filename
            )

            st.success("✅ Report generated and emailed successfully.")

            # Log
            new_row = pd.DataFrame([{
                "submitted_by": entered_by,
                "email": st.session_state.email if user_role != "guest" else "guest",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_path": filename
            }])

            if os.path.exists("submissions.csv"):
                existing = pd.read_csv("submissions.csv")
                combined = pd.concat([existing, new_row], ignore_index=True)
            else:
                combined = new_row

            combined.to_csv("submissions.csv", index=False)

        except Exception as e:
            st.error(f"❌ Failed to generate or send report: {e}")
