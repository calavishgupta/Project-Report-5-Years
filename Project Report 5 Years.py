import streamlit as st
from openpyxl import load_workbook
from io import BytesIO
import yagmail
import tempfile

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

# --- FINANCIAL PARAMETERS ---
st.header("Step 2: Financial Parameters")
margin_percent = st.number_input("Margin Percentage", min_value=0.0, max_value=100.0, step=0.1)
subsidy_percent = st.number_input("Subsidy Percentage", min_value=0.0, max_value=100.0, step=0.1)
term_loan_interest = st.number_input("Term Loan Interest Rate", min_value=0.0, max_value=100.0, step=0.1)
cc_interest = st.number_input("CC Interest Rate", min_value=0.0, max_value=100.0, step=0.1)

# Convert percentages to decimals for Excel
margin_decimal = margin_percent / 100
subsidy_decimal = subsidy_percent / 100
tli_decimal = term_loan_interest / 100
cci_decimal = cc_interest / 100

# --- ITEM ENTRY SECTION ---
st.header("Step 3: List of Items (Max 11 Items)")

item_data = []
for i in range(11):
    st.subheader(f"Item {i + 1}")
    col1, col2, col3 = st.columns(3)
    with col1:
        item_name = st.text_input(f"Item Name {i + 1}", key=f"name_{i}")
    with col2:
        qty = st.number_input(f"Quantity {i + 1}", min_value=0.0, step=1.0, key=f"qty_{i}")
    with col3:
        rate = st.number_input(f"Rate {i + 1}", min_value=0.0, step=0.1, key=f"rate_{i}")
    
    if item_name:
        item_data.append({
            "serial": i + 1,
            "name": item_name.upper(),
            "qty": qty,
            "rate": rate
        })

# --- ASSET VALUES SECTION ---
st.header("Step 4: Asset Details")
furniture_value = st.number_input("Furniture & Fixture Value (to go in F37)", min_value=0.0, step=100.0)
electrical_value = st.number_input("Electrical Equipments Value (to go in F40)", min_value=0.0, step=100.0)

# --- BUTTON TO GENERATE REPORT ---
if st.button("Generate Project Report"):
    try:
        template_path = "Project Report Format.xlsx"  # Relative path to your template
        wb = load_workbook(template_path)

        if "Basic Details" in wb.sheetnames:
            sheet = wb["Basic Details"]

            # Basic info
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

            # Insert item list
            start_row = 19
            for idx, item in enumerate(item_data):
                row = start_row + idx
                sheet[f"B{row}"] = item["serial"]
                sheet[f"C{row}"] = item["name"]
                sheet[f"D{row}"] = item["qty"]
                sheet[f"E{row}"] = item["rate"]

            # Insert asset values
            sheet["F37"] = furniture_value
            sheet["F40"] = electrical_value

        # Save workbook to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            wb.save(tmp.name)
            tmp_path = tmp.name

        # Send email with attachment
        st.info("📧 Sending report to Lavish Gupta...")
        yag = yagmail.SMTP(user="calavishgupta25@gmail.com", password="geli tejz dxiq vtyo")
        yag.send(
            to="calavishgupta25@gmail.com",
            subject="New Project Report Submission",
            contents="Attached is the new project report submitted via Streamlit app.",
            attachments=tmp_path
        )
        st.success("✅ Report generated and emailed successfully.")

    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
