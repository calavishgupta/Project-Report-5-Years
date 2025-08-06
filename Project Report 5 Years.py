import streamlit as st
from openpyxl import load_workbook
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

# Convert to decimal
margin_decimal = margin_percent / 100
subsidy_decimal = subsidy_percent / 100
tli_decimal = term_loan_interest / 100
cci_decimal = cc_interest / 100

# --- P&M ENTRY SECTION ---
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

# --- ASSET VALUES SECTION ---
st.header("Step 4: Other Fixed Assets")
furniture_value = st.number_input("Furniture & Fixture Value (₹)", min_value=0.0, step=100.0)
electrical_value = st.number_input("Electrical Equipments Value (₹)", min_value=0.0, step=100.0)

# --- TOTALS ---
st.header("💰 Summary")
grand_total = total_pm_value + furniture_value + electrical_value
st.write(f"**Total Plant & Machinery Value:** ₹{total_pm_value:,.2f}")
st.write(f"**Total Furniture & Fixture Value:** ₹{furniture_value:,.2f}")
st.write(f"**Total Electrical Equipments Value:** ₹{electrical_value:,.2f}")
st.subheader(f"**➡️ Grand Total: ₹{grand_total:,.2f}**")

# --- GENERATE & EMAIL REPORT ---
if st.button("📤 Generate & Email Project Report"):
    try:
        template_path = "Project Report Format.xlsx"
        wb = load_workbook(template_path)

        if "Basic Details" in wb.sheetnames:
            sheet = wb["Basic Details"]
            # Basic Details
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

            # P&M entries
            for idx, item in enumerate(item_data):
                row = 19 + idx
                sheet[f"B{row}"] = item["serial"]
                sheet[f"C{row}"] = item["name"]
                sheet[f"D{row}"] = item["qty"]
                sheet[f"E{row}"] = item["rate"]

            # Assets
            sheet["F37"] = furniture_value
            sheet["F40"] = electrical_value

            # 🔒 Hide the sheet before saving
            sheet.sheet_state = "hidden"

        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            wb.save(tmp.name)
            tmp_path = tmp.name

        # Email
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
