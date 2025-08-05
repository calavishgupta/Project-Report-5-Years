import streamlit as st
from openpyxl import load_workbook
from io import BytesIO

st.set_page_config(page_title="Project Report Generator", layout="wide")
st.title("📊 Automated Project Report Generator")

# --- INPUT SECTION ---
st.header("Step 1: Basic Details")
firm_name = st.text_input("Firm Name").upper()
firm_address = st.text_input("Firm Address").upper()
nature_of_business = st.text_input("Nature of Business").upper()
proprietor_name = st.text_input("Proprietor Name").upper()
proprietor_address = st.text_input("Address of Proprietor").upper()
building_status = st.selectbox("Building Rented/Owned", ["RENTED", "OWNED"])
area_sqft = st.text_input("Area in sq. ft").upper()
rent_rs = ""
if building_status == "RENTED":
    rent_rs = st.text_input("Rent in Rs.").upper()

# --- ADDITIONAL INPUTS ---
st.header("Step 2: Financial Parameters")
margin_percent = st.number_input("Margin Percentage", min_value=0.0, max_value=100.0, step=0.1)
subsidy_percent = st.number_input("Subsidy Percentage", min_value=0.0, max_value=100.0, step=0.1)
term_loan_interest = st.number_input("Term Loan Interest Rate", min_value=0.0, max_value=100.0, step=0.1)
cc_interest = st.number_input("CC Interest Rate", min_value=0.0, max_value=100.0, step=0.1)

# Convert percentages to decimal fractions for Excel (e.g., 5% → 0.05)
margin_decimal = margin_percent / 100
subsidy_decimal = subsidy_percent / 100
tli_decimal = term_loan_interest / 100
cci_decimal = cc_interest / 100

# --- BUTTON TO GENERATE REPORT ---
if st.button("Generate Project Report"):
    template_path = r"C:\\Users\\lavis\\OneDrive\\Desktop\\New folder\\Project Report Format.xlsx"
    wb = load_workbook(template_path)

    if "Basic Details" in wb.sheetnames:
        sheet = wb["Basic Details"]
        sheet["C3"] = firm_name
        sheet["C4"] = firm_address
        sheet["C5"] = nature_of_business
        sheet["C6"] = proprietor_name
        sheet["C7"] = proprietor_address
        sheet["C8"] = building_status.capitalize()
        sheet["C9"] = area_sqft
        sheet["C10"] = rent_rs if building_status == "RENTED" else ""
        sheet["C11"] = margin_decimal
        sheet["C12"] = subsidy_decimal
        sheet["C13"] = tli_decimal
        sheet["C14"] = cci_decimal

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    st.success("✅ Project report is ready.")
    st.download_button(
        label="📥 Download Filled Project Report",
        data=output,
        file_name="Project Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
